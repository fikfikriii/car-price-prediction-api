from fastapi import Body, APIRouter, HTTPException
from server.config.database import cars_collection
from server.schemas import carSchema
from fastapi import Depends
from server.auth.authenticate import get_current_user
from server.models.userModel import User
from server.models.carModel import Car
from server.models.transmisiModel import Transmisi

predict_car_router = APIRouter(
    tags=['Prediksi Harga Mobil Bekas']
)

@predict_car_router.get("/predict_car")
def prediksi_harga_mobil(nama_mobil: str, tahun: int, odo: int, transmisi: Transmisi, current_user:User = Depends(get_current_user)):
    try:
        results = carSchema.get_estimated_car_price(nama_mobil, tahun, odo, transmisi)
        results = "{:,}".format(results)
        results = results.replace(',','.')
        return (f"Harga mobil bekas ini diprediksi sebesar Rp {results}")
    except:
        return ("Maaf, data mobil yang Anda masukan tidak dapat diprediksi harganya")