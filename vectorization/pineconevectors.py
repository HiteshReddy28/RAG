from pinecone import Pinecone
from dotenv import load_dotenv
import os
import glob
import json
from langchain_text_splitters import RecursiveCharacterTextSplitter

import google.generativeai as genai


# splitter = RecursiveCharacterTextSplitter(
#     chunk_size=500,     
#     chunk_overlap=50
# )

# load_dotenv()

# api_key = os.getenv("PINE_CONE_KEY")
# pc = Pinecone(api_key = api_key)
# index = pc.Index("rag")


# api_key = os.getenv("GEMINI_API_KEY")
# genai.configure(api_key=api_key)

# glob_pattern = "../dataextraction/uscis_summary.json"
# file = glob.glob(glob_pattern)




# if file:
#     with open(file[0], "r") as f:
#         data = json.load(f)
#         records = {}   
#         for item in data:
#             print(len(item["summary"]))
#             chunks = splitter.split_text(item["summary"])
#             for i,chunk in enumerate(chunks):
#                 records[f"{item['id']}_chunk_{i}"] = chunk
#         for id_val, text in records.items():
#             index.update(
#                 id=id_val,
#                 set_metadata={"text": text},
#                 namespace="f1rag"
#             )
# # #             for i, chunk in enumerate(chunks):
# # #                 metadata = {
# # #                     "docid": item["id"],
# # #                     "url": item["url"],
# # #                     "notes": item["notes"],
# # #                     "chunk_index": i,
# # #                     "text": chunk   
# # #                 }
# # #                 print(f"{item["id"]}_chuck_{i}")
# # #                 response = genai.embed_content(
# # #     model="models/embedding-001",
# # #     content=chunk
# # # )

# # #                 index.upsert(vectors=[(f"{item['id']}_chunk_{i}", response["embedding"], metadata)], namespace="f1rag")
# # #             print(f"Number of chunks: {len(chunks)}")




load_dotenv()

pinecone_key = os.getenv("PINE_CONE_KEY")
gemini_key = os.getenv("GEMINI_API_KEY")

# ----------------------------
# 2. Initialize Pinecone and Gemini
# ----------------------------
pc = Pinecone(api_key=pinecone_key)
index = pc.Index("rag")  # make sure your Pinecone index name matches

genai.configure(api_key=gemini_key)

# ----------------------------
# 3. Prepare file path and text splitter
# ----------------------------
glob_pattern = "../dataextraction/uscis_summary.json"
files = glob.glob(glob_pattern)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,     
    chunk_overlap=50
)

# ----------------------------
# 4. Process JSON and create embeddings
# ----------------------------
for file_path in files:
    print(f"Processing: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        documents = data.get("documents", [])

    vectors_to_upsert = []

    for doc in documents:
        text = doc.get("summary", "")
        if not text.strip():
            continue

        # Split long summaries into smaller chunks
        chunks = splitter.split_text(text)

        for i, chunk in enumerate(chunks):
            # Generate embedding
            embedding_response = genai.embed_content(
                model="models/embedding-001",
                content=chunk
            )

            embedding = embedding_response["embedding"]

            # Prepare vector
            vector = {
                "id": f"{doc['document_id']}_chunk{i}",
                "values": embedding,
                "metadata": {
                    "url": doc.get("url"),
                    "timestamp": doc.get("timestamp"),
                    "source": doc.get("source"),
                    "chunk": chunk,
                    "original_text_length": doc.get("original_text_length")
                }
            }

            # ✅ Upsert immediately to Pinecone
            index.upsert(vectors=[vector])

            print(f"✅ Upserted: {vector['id']} (len={len(chunk)})")

