from fastapi import Body, APIRouter, HTTPException
from server.config.database import cars_collection
from server.schemas import carSchema
from fastapi import Depends
from server.auth.authenticate import get_current_user
from server.models.userModel import User
from server.models.carModel import Car
from server.models.bankModel import Bank

cicilan_car_router = APIRouter(
    tags=['Hitung Kredit Mobil Bekas']
)

@cicilan_car_router.get('/cicilan')
def hitung_cicilan_menggunakan_bunga_fix(harga_mobil: int, jangka_waktu: int, bunga_per_tahun: float, persentase_uang_muka: float, current_user:User = Depends(get_current_user)) -> dict:
    return carSchema.calculate_cicilan_bunga_fix(harga_mobil, jangka_waktu, bunga_per_tahun, persentase_uang_muka)

@cicilan_car_router.get('/cicilan-by-bank')
def hitung_cicilan_menggunakan_kebijakan_KKB_bank(harga_mobil: int, persentase_uang_muka: float, bank: Bank, current_user:User = Depends(get_current_user)):
    return carSchema.calculate_2_jenis_bunga(harga_mobil, persentase_uang_muka, bank)