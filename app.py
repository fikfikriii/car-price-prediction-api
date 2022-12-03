# Local imports
import datetime
from fastapi import FastAPI, HTTPException
from joblib import load
from pydantic import BaseModel

# Load the model
car_svm = load(open('./models/car_price_precition_model.pkl', 'rb'))

# Load the vectorizer
vectorizer = load(open('./models/car_price_precition_model.pkl', 'rb'))

# Define variables
model_name = "Car price prediction"
version = "v1.0.0"
app = FastAPI()

# Input for data validation
class Input(BaseModel):
    perusahaan: str
    nama_mobil: str
    transmisi: enumerate("Automatic", "Manual")
    odo: int
    tahun: int

    class Config:
        schema_extra = {
            "perusahaan": "Daihatsu",
            "nama_mobil": "Ayla",
            "transmisi": "Automatic",
            "odo": 50000,
            "tahun": 2018,
        }

# Ouput for data validation
class Output(BaseModel):
    prediction: int

# Default root
@app.get("/")
def root():
    return {"message": "Welcome to Car Price Prediction using FastAPI!"}

@app.get('/info')
async def model_info():
    """Return model information, version, how to call"""
    return {
        "name": model_name,
        "version": version
    }

@app.post('/predict', response_model=Output)
async def model_predict(input: Input):
    
    if(not(input)):
        raise HTTPException(status_code=400,
                            detail= "Please provide a valid input.")
    
    prediction = car_svm.predict(vectorizer.transform([input]))
    
    """Predict with input"""
    response = get_model_response(input)
    return response