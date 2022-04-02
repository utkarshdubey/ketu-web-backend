from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from utils import encodeMessage, decodeMessage
from stegano import lsb
from PIL import Image
import uuid
import os

is_prod = os.environ.get("IS_HEROKU", None)

static_url = "https://ketu-web.herokuapp.com/static/" if is_prod else "http://localhost:8000/static/"

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
        image = lsb.hide(Image.open(file.file), secret)
        image.save(f"./static/{random_id}.png")
        # encodeMessage(Image.open(file.file), secret, f"{random_id}.png")
        return {"filename": file.filename, "secret": secret, "url": f"${static_url}{random_id}.png"}
    
@app.post("/decrypt")
async def create_upload_file(file: UploadFile | None = None):
    if not file:
        return {"error": "Whoops, something weird with the file?"}
    else:
        # secret = decodeMessage(Image.open(file.file))
        secret = lsb.reveal(Image.open(file.file))
        return {"filename": file.filename, "secret": secret}
