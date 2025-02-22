from fastapi import FastAPI, HTTPException
from supabase import create_client, Client
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

# Initialize Supabase client
# Replace with your actual Supabase URL and anon key
SUPABASE_URL = "https://hdcoxfhzixmzlnmhjrfj.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhkY294Zmh6aXhtemxubWhqcmZqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzcwNDY4MjcsImV4cCI6MjA1MjYyMjgyN30.DDNGFmb3h3o5uaGsqqQ7zu6kz66lrbEVUqFLBZJQ3wg"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Pydantic model for Note
class Note(BaseModel):
    id: Optional[int]
    folder_name: str
    note_name: str
    note_desc: str

@app.get("/")
async def root():
    return {"message": "Welcome to Notes API"}

@app.get("/notes/")
async def get_all_notes():
    try:
        response = supabase.table('Notes').select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/notes/search/")
async def search_notes(notename: str):
    try:
        response = supabase.table('Notes')\
            .select("*")\
            .ilike('notename', f'%{notename}%')\
            .execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 