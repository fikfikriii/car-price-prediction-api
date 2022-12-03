from fastapi import APIRouter
from config.database import cars_collection
from models.carModel import Car
from schemas.carSchema import car_serializer, cars_serializer
from fastapi import Depends
from auth.authenticate import get_current_user
from models.userModel import User

car_router = APIRouter()

@car_router.get("/cars", tags=["Car"])
async def get_cars(current_user:User = Depends(get_current_user)):
    cars = cars_serializer(cars_collection.find())
    return {"status": "ok", "data": cars}

@car_router.get("/cars/search-nama/{nama_mobil}", tags=["Car"])
async def get_cars_by_name(nama_mobil: str):
    return cars_serializer(cars_collection.find({"nama_mobil": nama_mobil}))

@car_router.get("/cars/search-perusahaan/{nama_perusahaan}", tags=["Car"])
async def get_cars_by_perusahaan(nama_perusahaan: str):
    return cars_serializer(cars_collection.find({"perusahaan": nama_perusahaan}))

@car_router.post("/cars", tags=["Car"])
def add_car(car: Car, current_user:User = Depends(get_current_user)):
    _id = cars_collection.insert_one(dict(car))
    car = cars_serializer(cars_collection.find({"_id": _id.inserted_id}))
    return {"status": "ok", "data":car}