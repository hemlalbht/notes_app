from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from starlette.templating import Jinja2Templates

app = FastAPI()

# Database Connection
MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
db = client.notes_db
notes_collection = db.notes

templates = Jinja2Templates(directory="templates")

# Home Page
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
    await notes_collection.delete_one({"_id": ObjectId(note_id)})
    return RedirectResponse(url="/", status_code=303)
