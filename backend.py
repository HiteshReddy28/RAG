from dotenv import load_dotenv
from pinecone import Pinecone
import os
import google.generativeai as genai
import argparse


load_dotenv()

api_key = os.getenv("PINE_CONE_KEY")
pc = Pinecone(api_key = api_key)
index = pc.Index("rag")

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def query_vector_store(user_query):
    query_vector = genai.embed_content(
    model="models/embedding-001",   # same model as you used before
    content=user_query
)["embedding"]
    results = index.query(
        vector=query_vector,
        top_k = 5,                # number of most relevant chunks to fetch
        include_metadata=True,  # so you also get back your original text
    )
    return results


def format_response(results):
    text = ""
    for match in results["matches"]:         
        text += match["metadata"]["chunk"]   # your stored chunk
    system_prompt = f""" You are a helpful agent for international students use the following information to provide the answer better use the context to answer the question.
    context: {text}
    """
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=system_prompt,
    )
    response = model.generate_content(user_query)
    return response.text


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="User query for RAG.")
    parser.add_argument("query", type=str, help="The user query to search.")
    args = parser.parse_args()
    user_query = args.query
    vectors_for_llm = query_vector_store(user_query)
    # print(vectors_for_llm)
    final_response = format_response(vectors_for_llm)
    print(final_response)
