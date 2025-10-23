from pinecone import Pinecone
from dotenv import load_dotenv
import os
import json
from typing import Dict, List

def fetch_from_pinecone() -> Dict:
    """Fetch all vectors and metadata from Pinecone index and return as structured data."""
    
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("PINE_CONE_KEY")
    
    if not api_key:
        raise ValueError("PINE_CONE_KEY not found in environment variables")
    
    # Initialize Pinecone
    pc = Pinecone(api_key=api_key)
    index = pc.Index("f1rag")
    
    # Fetch all vectors from the namespace
    try:
        # Get all vectors from the f1rag namespace
        results = index.query(
            namespace="f1rag",
            top_k=10000,  # Adjust if you have more vectors
            include_metadata=True,
            include_values=True,  # Include the actual vectors
            vector=[0] * 768  # Dummy vector to fetch all - adjust dimension if different
        )
        
        # Structure the data
        documents = []
        for match in results.matches:
            doc_data = {
                "id": match.id,
                "score": match.score,
                "metadata": match.metadata,
                "vector": match.values  # Values are already in list format
            }
            documents.append(doc_data)
        
        return {
            "total_documents": len(documents),
            "vector_dimension": len(match.values) if documents and match.values else None,
            "documents": documents
        }
    
    except Exception as e:
        print(f"Error fetching from Pinecone: {e}")
        return {"total_documents": 0, "documents": []}

def main():
    output_file = "pinecone_data.json"
    
    print("Fetching data from Pinecone...")
    data = fetch_from_pinecone()
    
    # Save to JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\nDone! Saved {data['total_documents']} documents to {output_file}")
    
    # Print sample of first document if any exist
    if data["documents"]:
        print("\nSample document structure:")
        print(json.dumps(data["documents"][0], indent=2))

if __name__ == "__main__":
    main()