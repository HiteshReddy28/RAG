from fastapi import FastAPI
import uvicorn

import json
app = FastAPI()

@app.get("/")
def read_root():
    return {"msg":"hello from fastapi"}

@app.get("/summarized")
def read_json():
    with open("./dataextraction/summary.json") as file:
        summary = json.load(file)
    return {"content":f"{summary}"}

if __name__ == "__main__":
        uvicorn.run("backend:app", host="0.0.0.0", port=8000, reload=True)