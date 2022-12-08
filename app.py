import uvicorn
from fastapi import FastAPI
from server.routes.carRoute import car_router
from server.routes.predictCarRoute import predict_car_router
from server.routes.cicilanCarRoute import cicilan_car_router
from server.routes.rekomendasiCarRoute import rekomendasi_car_router
from server.routes.userRoute import user_router
import warnings
warnings.filterwarnings('ignore')

description = """
Ini adalah API untuk melihat informasi mobil bekas, melakukan prediksi harga, dan menghitung cicilan mobil bekas di Indonesia. Sebelum dapat melakukan request pada endpoints API ini, Anda diwajibkan untuk melakukan **Registrasion** dan **Login** atau melalui tombol **Authorize** pada API ini. Setelah terauthorize, Anda dapat melakukan request pada beberapa endpoints yang terdapat pada API ini, yaitu:

## Melihat Informasi Mobil Bekas
Anda dapat melakukan pencarian mobil bekas menggunakan kriteria-kriteria sebagai berikut:
1. Pencarian berdasarkan **nama**
2. Pencarian berdasarkan **tahun**
3. Pencarian berdasarkan **nama perusahaan / manufakturer**
4. Pencarian berdasarkan **jenis transmisi**

## Prediksi Harga Mobil Bekas
Anda dapat melakukan prediksi harga mobil bekas yang diestimasi berdasarkan **nama mobil, tahun, odo,** dan **jenis transmisinya**

## Menghitung Kredit Mobil Bekas
Anda dapat melakukan perhitungan kredit mobil bekas dengan 2 cara berikut:
1. Perhitungan menggunakan bunga fix\n
\tGunakan endpoint ini jika Anda ingin menghitung kredit mobil bekas Anda pada tenor yang memiliki kebijakan bunga fix dalam peminjamannya. Harap masukkan **harga mobil, janga waktu cicilan (tahun), bunga per tahun (%),** dan **persentase pembayaran uang muka** yang sesuai
2. Perhitungan sesuai dengan Bank penyedia KKB yang Anda pilih.\n
\tGunakan endpoint ini untuk melihat perhitungan kredit mobil bekas pada beberapa bank penyedia (BCA, Mandiri, BNI, dan CIMB Niaga). Anda hanya perlu memasukan **harga mobil** dan **persentase pembayaran uang muka**.

## Rekomendasi Mobil Bekas
Anda dapat melihat rekomendasi mobil bekas pada _database_ kami berdasarkan bank pilihan, harga, dan cicilan maksimal yang Anda inginkan
"""

app = FastAPI(
    title="Car Price Prediction API",
    description=description
)
app.include_router(user_router)
app.include_router(car_router)
app.include_router(predict_car_router)
app.include_router(cicilan_car_router)
app.include_router(rekomendasi_car_router)

if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=8090, reload=True)