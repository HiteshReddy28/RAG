from pinecone import Pinecone
from dotenv import load_dotenv
import os
import glob
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
import google.generativeai as genai


splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,     
    chunk_overlap=50
)

load_dotenv()

api_key = os.getenv("PINE_CONE_KEY")
pc = Pinecone(api_key = api_key)
index = pc.Index("f1rag")


api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

glob_pattern = "../dataextraction/summary.json"
file = glob.glob(glob_pattern)

if file:
    with open(file[0], "r") as f:
        data = json.load(f)
        records = {}   
        for item in data:
            print(len(item["summary"]))
            vector = item["summary"]
            chunks = splitter.split_text(item["summary"])
            for i,chunk in enumerate(chunks):
                records[f"{item['id']}_chunk_{i}"] = chunk
        for id_val, text in records.items():
            index.update(
                id=id_val,
                set_metadata={"text": text},
                namespace="f1rag"
            )
#             for i, chunk in enumerate(chunks):
#                 metadata = {
#                     "docid": item["id"],
#                     "url": item["url"],
#                     "notes": item["notes"],
#                     "chunk_index": i,
#                     "text": chunk   
#                 }
#                 print(f"{item["id"]}_chuck_{i}")
#                 response = genai.embed_content(
#     model="models/embedding-001",
#     content=chunk
# )

#                 index.upsert(vectors=[(f"{item['id']}_chunk_{i}", response["embedding"], metadata)], namespace="f1rag")
#             print(f"Number of chunks: {len(chunks)}")



