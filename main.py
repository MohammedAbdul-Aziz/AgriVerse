
import os
import shutil
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from model import predict as model_predict

app = FastAPI()

# Allow all origins for CORS (in a production environment, you should restrict this)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOADS_DIR = "uploads"

# Create the uploads directory if it doesn't exist
os.makedirs(UPLOADS_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "Welcome to the AgriVerse AI Pipeline"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Accepts an image file, saves it, and returns a prediction.
    """
    if not file:
        return {"error": "No file was provided"}

    file_path = os.path.join(UPLOADS_DIR, file.filename)
    
    # Save the uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Get a prediction from our model
    prediction = model_predict(file_path)
    
    return prediction
