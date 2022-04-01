from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from utils import encodeMessage, decodeMessage
from PIL import Image
import uuid

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://ketu-web.vercel.app",
    "https://vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {
        "ok": "ok"
    }

@app.post("/encrypt")
async def create_upload_file(secret: str = Form(...), file: UploadFile | None = None):
    if not file:
        return {"error": "Whoops, something weird with the file?"}
    else:
        random_id = uuid.uuid4()
        encodeMessage(Image.open(file.file), secret, f"{random_id}.png")
        return {"filename": file.filename, "secret": secret, "url": f"http://localhost:8000/static/{random_id}.png"}
    
@app.post("/decrypt")
async def create_upload_file(file: UploadFile | None = None):
    if not file:
        return {"error": "Whoops, something weird with the file?"}
    else:
        secret = decodeMessage(Image.open(file.file))
        return {"filename": file.filename, "secret": secret}
