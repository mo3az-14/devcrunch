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

# Add new Pydantic models for Summary
class SummaryResponse(BaseModel):
    id: int
    notes_id: int
    folder_name: str
    note_name: str
    summary_text: str

class SummaryCreate(BaseModel):
    note_name: str
    summary_text: str
    model: str

class SummaryUpdate(BaseModel):
    summary_text: str

# Add new endpoints for Summary
@app.get("/summaries/")
async def get_all_summaries():
    try:
        response = supabase.table('Summary')\
            .select("id, notes_id, folder_name, note_name, summary_text")\
            .execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summaries/")
async def create_summary(summary: SummaryCreate):
    try:
        # First, get the note details based on note_name
        note_response = supabase.table('Notes')\
            .select("id, folder_name")\
            .eq('note_name', summary.note_name)\
            .execute()
        
        if not note_response.data:
            raise HTTPException(status_code=404, detail="Note not found")
        
        note = note_response.data[0]
        
        # Create the summary
        response = supabase.table('Summary')\
            .insert({
                'notes_id': note['id'],
                'folder_name': note['folder_name'],
                'note_name': summary.note_name,
                'summary_text': summary.summary_text,
                'model': summary.model
            })\
            .execute()
        
        return response.data[0]
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/summaries/{summary_id}")
async def update_summary(summary_id: int, summary: SummaryUpdate):
    try:
        # Check if summary exists
        check_response = supabase.table('Summary')\
            .select("*")\
            .eq('id', summary_id)\
            .execute()
        
        if not check_response.data:
            raise HTTPException(status_code=404, detail="Summary not found")
        
        # Update the summary
        response = supabase.table('Summary')\
            .update({"summary_text": summary.summary_text})\
            .eq('id', summary_id)\
            .execute()
        
        return response.data[0]
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
