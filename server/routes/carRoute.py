from fastapi import Body, APIRouter, HTTPException
from server.config.database import cars_collection
from server.schemas.carSchema import car_serializer, cars_serializer, get_estimated_car_price
from fastapi import Depends
from server.auth.authenticate import get_current_user
from server.models.userModel import User
from server.models.carModel import Car

car_router = APIRouter(
    tags=['Car']
)

@car_router.get("/cars")
async def get_cars(current_user:User = Depends(get_current_user)):
    cars = cars_serializer(cars_collection.find())
    return {"status": "ok", "data": cars}

@car_router.get("/cars/search-nama/{nama_mobil}")
async def get_cars_by_name(nama_mobil: str, current_user:User = Depends(get_current_user)):
    car_by_nama = { "nama_mobil": {"$regex": nama_mobil.capitalize()} }
    return cars_serializer(cars_collection.find(car_by_nama))

# current_user:User = Depends(get_current_user)
@car_router.get("/cars/search/tahun/{tahun}")
async def get_cars_by_tahun(tahun: int):
    car_by_tahun = {"tahun": tahun}
    return cars_serializer(cars_collection.find(car_by_tahun))

@car_router.get("/cars/search-perusahaan/{nama_perusahaan}")
async def get_cars_by_perusahaan(nama_perusahaan: str):
    car_by_perusahaan = { "perusahaan": {"$regex": nama_perusahaan.capitalize()} }
    return cars_serializer(cars_collection.find(car_by_perusahaan))

@car_router.get("/cars/search-transmisi/{transmisi}")
async def get_cars_by_perusahaan(transmisi: str):
    car_by_transmisi = { "transmisi": {"$regex": transmisi.capitalize()} }
    return cars_serializer(cars_collection.find(car_by_transmisi))

@car_router.post("/cars")
def add_car(car: Car, current_user:User = Depends(get_current_user)):
    _id = cars_collection.insert_one(dict(car))
    car = cars_serializer(cars_collection.find({"_id": _id.inserted_id}))
    return {"status": "ok", "data":car}

@car_router.post("/predict_car")
def predict_car_price(car: Car = Body(...)) -> dict:
    if(not(car)):
        raise HTTPException(status_code=400,
                            detail= "Please provide a valid input!")
    perusahaan = car.perusahaan
    nama_mobil = car.nama_mobil
    tahun = car.tahun
    odo = car.odo
    transmisi = car.jenis_transmisi
    try:
        results = int(get_estimated_car_price(perusahaan, nama_mobil, tahun, odo, transmisi))
        return results
    except:
        return "Data mobil tidak ditemukan"