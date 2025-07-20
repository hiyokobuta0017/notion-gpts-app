from fastapi import FastAPI
from notion_client import Client
import os

app = FastAPI()

notion = Client(auth=os.environ["NOTION_TOKEN"])

@app.get("/")
def root():
    return {"message": "Hello, Notion-GPTs!"}

@app.get("/notion-database")
def get_database():
    database_id = os.environ["DATABASE_ID"]
    response = notion.databases.query(database_id=database_id)
    return response
