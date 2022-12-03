import pickle
import json
import numpy as np
from fastapi import Body, APIRouter, HTTPException
from config.database import houses_collection
from models.carModel import Car
from schemas.houseSchema import house_serializer, houses_serializer, get_estimated_price
from fastapi import Depends
from auth.authenticate import get_current_user
from models.userModel import User
from models.houseModel import House

global model
with open('./models/home_price_prediction.pickle', 'rb') as f:
    model = pickle.load(f)

house_router = APIRouter(
    tags=['House']
)

@house_router.get("/house")
async def get_house(current_user:User = Depends(get_current_user)):
    house = houses_serializer(houses_collection.find())
    return {"status": "ok", "data": house}

@house_router.get("/house/search-lantai/{nama_perusahaan}")
async def get_house_by_jumlah_lantai(nama_perusahaan: str, current_user:User = Depends(get_current_user)):
    return houses_serializer(houses_collection.find({"perusahaan": nama_perusahaan}))

@house_router.post("/house")
def add_car(house: House, current_user:User = Depends(get_current_user)):
    _id = houses_collection.insert_one(dict(house))
    house = houses_serializer(houses_collection.find({"_id": _id.inserted_id}))
    return {"status": "ok", "data":house}

@house_router.post("/predict")
def predict_house_price(house: House) -> dict:
    if(not(house)):
        raise HTTPException(status_code=400,
                            detail= "Please provide a valid input!")
    lb = house.luas_bangunan
    lt = house.luas_tanah
    kt = house.jumlah_kamar_tidur
    km = house.jumlah_kamar_mandi
    grs = house.jumlah_garasi
    results = int(get_estimated_price(lb, lt, kt, km, grs))
    results_str = str("{:,}".format(results)).replace(',','.')
    return ("Harga rumah diprediksi sebesar Rp " + results_str)