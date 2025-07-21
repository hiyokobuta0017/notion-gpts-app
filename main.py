from fastapi import FastAPI
from fastapi.responses import JSONResponse
from notion_client import Client
import os
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
notion = Client(auth=NOTION_TOKEN)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, Notion-GPTs!"}

@app.get("/notion-database/{database_id}")
def get_database(database_id: str):
    try:
        response = notion.databases.query(database_id=database_id)
        return response
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
