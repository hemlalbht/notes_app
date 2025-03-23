import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from starlette.templating import Jinja2Templates

# Load environment variables
load_dotenv()

app = FastAPI()

# Database Connection
MONGO_URL = os.getenv("MONGO_URL")
if not MONGO_URL:
    raise ValueError("⚠️ MONGO_URL is not set in .env file!")

client = AsyncIOMotorClient(MONGO_URL)
db = client.notes_db
notes_collection = db.notes

# Jinja2 Templates
templates = Jinja2Templates(directory="templates")

# Home Page - Display Notes
@app.get("/", response_class=HTMLResponse)
async def read_notes(request: Request):
    notes = await notes_collection.find().to_list(100)
    return templates.TemplateResponse("index.html", {"request": request, "notes": notes})

# Add Note
@app.post("/add")
async def add_note(title: str = Form(...), content: str = Form(...)):
    new_note = {"title": title, "content": content}
    await notes_collection.insert_one(new_note)
    return RedirectResponse(url="/", status_code=303)

# Delete Note
@app.get("/delete/{note_id}")
async def delete_note(note_id: str):
    try:
        await notes_collection.delete_one({"_id": ObjectId(note_id)})
    except Exception:
        return {"error": "Invalid ID format"}
    return RedirectResponse(url="/", status_code=303)
