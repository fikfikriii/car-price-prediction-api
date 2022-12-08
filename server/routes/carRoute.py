from fastapi import Body, APIRouter, HTTPException
from server.config.database import cars_collection
from server.schemas import carSchema
from fastapi import Depends
from server.auth.authenticate import get_current_user
from server.models.userModel import User
from server.models.carModel import Car
from server.models.bankModel import Bank
from server.models.transmisiModel import Transmisi

car_router = APIRouter(
    tags=['Informasi Mobil']
)

@car_router.get("/cars")
async def get_all_cars(current_user:User = Depends(get_current_user)):
    cars = carSchema.cars_serializer(cars_collection.find())
    return {"status": "ok", "data": cars}

@car_router.get("/cars/search-nama/{nama_mobil}")
async def get_cars_by_name(nama_mobil: str, current_user:User = Depends(get_current_user)):
    list_car = []
    for car in carSchema.cars_serializer(cars_collection.find()):
        if (nama_mobil.lower() in car['nama_mobil'].lower()):
            list_car.append(car)
    return list_car

@car_router.get("/cars/search/tahun/{tahun}")
async def get_cars_by_tahun(tahun: int, current_user:User = Depends(get_current_user)):
    car_by_tahun = {"tahun": tahun}
    return carSchema.cars_serializer(cars_collection.find(car_by_tahun))

@car_router.get("/cars/search-perusahaan/{nama_perusahaan}")
async def get_cars_by_perusahaan(nama_perusahaan: str, current_user:User = Depends(get_current_user)):
    car_by_perusahaan = { "perusahaan": {"$regex": nama_perusahaan.capitalize()} }
    return carSchema.cars_serializer(cars_collection.find(car_by_perusahaan))

@car_router.get("/cars/search-transmisi/{transmisi}")
async def get_cars_by_transmisi(transmisi: Transmisi, current_user:User = Depends(get_current_user)):
    list_car = []
    for car in carSchema.cars_serializer(cars_collection.find()):
        if (transmisi.name == car['jenis_transmisi']):
            list_car.append(car)
    return list_car

@car_router.get("/cars/search-harga")
async def get_cars_by_harga(harga_min: int, harga_max: int, current_user:User = Depends(get_current_user)):
    list_car = []
    for car in carSchema.cars_serializer(cars_collection.find()):
        if (harga_min <= car['harga'] and harga_max >= car['harga']):
            list_car.append(car)
    return list_car

@car_router.get("/cars/filter")
async def get_filtered_cars(nama_mobil: str, odo_min: int, odo_max: int, tahun_min: int, tahun_max: int, harga_min: int, harga_max: int, transmisi: Transmisi, current_user:User = Depends(get_current_user)):
    print("TESSS")
    return carSchema.filter_mobil(nama_mobil, odo_min, odo_max, tahun_min, tahun_max, transmisi, harga_min, harga_max)