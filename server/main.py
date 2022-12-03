import uvicorn
from fastapi import FastAPI
from routes.carRoute import car_router
from routes.userRoute import user_router
from routes.houseRoute import house_router

description = """
Ini adalah API untuk melakukan prediksi harga rumah di Indonesia. Silakan masukan input yang sesuai dengan deksripsi di bawah ini untuk mendapatkan harga rumah berdasarkan kriteria yang Anda inginkan. 🚀

Beberapa instance yang terdapat pada API ini:

## Users

Anda dapat melakukan:
* **Registrasion**
* **Login**

## Items

Anda dapat ...
"""

app = FastAPI(
    title="House Price Prediction API",
    description=description
)
app.include_router(user_router)
app.include_router(car_router)
app.include_router(house_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8090, reload=True)