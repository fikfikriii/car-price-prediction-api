from fastapi import Body, APIRouter, HTTPException
from server.config.database import cars_collection
from server.schemas import carSchema
from fastapi import Depends
from server.auth.authenticate import get_current_user
from server.models.userModel import User
from server.models.carModel import Car
from server.models.bankModel import Bank
from server.schemas import carSchema

rekomendasi_car_router = APIRouter(
    tags=['Rekomendasi Mobil Bekas']
)

@rekomendasi_car_router.get('/rekomendasi')
async def rekomendasi_mobil_bekas(max_harga_mobil: int, max_cicilan_per_bulan: int, bank: Bank, current_user:User = Depends(get_current_user)):
    return carSchema.rekomendasi_mobil(max_harga_mobil, max_cicilan_per_bulan, bank)