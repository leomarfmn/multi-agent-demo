from pdf2image import convert_from_path
import pytesseract
import os
from qdrant_client import QdrantClient, models
from fastapi import HTTPException
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# Initialize Qdrant client and the embedding model
load_dotenv()
qdrant_api_key = os.getenv("QDRANT_API_KEY")
qdrant_url = os.getenv("QDRANT_URL")
client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
model = SentenceTransformer('all-MiniLM-L6-v2')


def run_ocr(pdf_file):
    # Run OCR on the PDF file and split content into manageable chunks
    try:
        docs = convert_from_path(pdf_file)
        records = []
        id_count = 0

        for page_number, page_data in enumerate(docs):
            text = pytesseract.image_to_string(page_data).encode("utf-8").decode("utf-8")
            
            # Clean up the text and skip empty pages
            text = text.strip()
            if not text:  
                continue
            
            # Split the page text into chunks
            chunks = split_text_into_chunks(text)

            for chunk_text in chunks:
                # Format record for each chunk
                record = {
                    "id": id_count,
                    "text": chunk_text,
                    "page": page_number + 1,
                    "source": pdf_file
                }
                records.append(record)
                id_count += 1
        
        print(f"OCR completed successfully. Created {id_count} records from {len(docs)} pages")
        return records

    except Exception as e:
        print(f"Error running OCR on file: {e}")
        raise HTTPException(status_code=500, detail="OCR processing failed")


def split_text_into_chunks(text, chunk_size=500, chunk_overlap=100):
    # Split text into overlapping chunks

    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        # Calculate end position
        end = start + chunk_size
        
        # Extract the chunk
        if end >= len(text):
            chunk = text[start:].strip()
            if chunk != "":
                chunks.append(chunk)
            break
        else:
            chunk = text[start:end].strip()
            if chunk != "":
                chunks.append(chunk)
            start = start + chunk_size - chunk_overlap
    
    return chunks


def upload_to_qdrant(records):
    # Upload chunks to Qdrant
    try:
        # Delete collection if it exists
        level_collection = "multi_agent_demo_level1"
        if client.collection_exists(collection_name=level_collection):
            client.delete_collection(collection_name=level_collection)
        
        # Create collection (fix the logic here)
        client.create_collection(
            collection_name=level_collection,
            vectors_config=models.VectorParams(
                size=384,
                distance=models.Distance.COSINE
            ),
        )
        
        # Prepare points for upsert
        points = []
        for record in records:
            # Generate embedding for the text
            vector = model.encode(record["text"]).tolist()
            
            # Create point
            point = models.PointStruct(
                id=record["id"],
                vector=vector,
                payload={
                    "text": record["text"],
                    "page": record["page"],
                    "source": record["source"]
                }
            )
            points.append(point)
        
        # Upsert points to collection
        client.upsert(
            collection_name=level_collection,
            points=points
        )
        
        print(f"Uploaded {len(points)} points to Qdrant collection '{level_collection}'")
        return level_collection
    
    except Exception as e:
        print(f"Error uploading to Qdrant: {e}")
        raise HTTPException(status_code=500, detail="Qdrant upload failed")


def similarity_search(question, level_collection):
    # Perform similarity search in Qdrant
    try:
        search_results = client.search(
            collection_name=level_collection,
            query_vector=model.encode(question).tolist(),
            limit=5,
            with_payload=True
        )
        
        results = []
        for result in search_results:
            results.append({
                "text": result.payload["text"],
                "page": result.payload["page"],
                "source": result.payload["source"],
                "score": result.score
            })
        return results
    
    except Exception as e:
        print(f"Error during similarity search: {e}")
        raise HTTPException(status_code=500, detail="Similarity search failed")