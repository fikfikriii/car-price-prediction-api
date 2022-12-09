import pickle
import numpy as np
import json
from fastapi import Body, APIRouter, HTTPException
from server.config.database import cars_collection
from server.schemas import carSchema
from fastapi import Depends
from server.auth.authenticate import get_current_user
from server.models.userModel import User
from server.models.carModel import Car
from server.models.bankModel import Bank
from server.models.transmisiModel import Transmisi

global model
with open('./server/models/data/car_price_prediction.pickle', 'rb') as f:
    model = pickle.load(f)

global perusahaan
global mobil
global transmisi

global data_columns
with open('./server/models/data/car_columns.json', 'r') as f:
    data_columns = json.load(f)['data_columns']
    mobil = data_columns[2:]
    transmisi = data_columns[2:]
    
def get_estimated_car_price(mobil, tahun, odo, transmisi):
    try:
        mobil_index = data_columns.index(mobil.capitalize())
    except:
        mobil_index = -1
    
    try:
        transmisi_index = data_columns.index(transmisi.name)
    except:
        transmisi_index = -1

    x = np.zeros(len(data_columns))
    x[0] = tahun
    x[1] = odo
    
    if mobil_index >= 0 and transmisi_index >= 0:
        x[mobil_index] = 1
        x[transmisi_index] = 1
        results = int(round(model.predict([x])[0], -3))
        return results
    
    return "Data mobil tidak ditemukan"

def filter_mobil(nama_mobil: str, odo_min: int, odo_max: int, tahun_min: int, tahun_max: int, transmisi: Transmisi, harga_min: int, harga_max: int):
    list_car = []
    for car in cars_serializer(cars_collection.find()):
        if (car['jenis_transmisi'] == transmisi.name):
            if (nama_mobil.lower() in car['nama_mobil'].lower()):
                if odo_min <= car['odo'] and odo_max >= car['odo']:
                    if (tahun_min <= car['tahun'] and tahun_max >= car['tahun']):
                        if (harga_min <= car['harga'] and harga_max >= car['harga']):
                            print("Ditemukan")
                            list_car.append(car)
    if len(list_car) == 0:
        return ("Maaf, tidak ada data mobil yang memenuhi kriteria yang Anda masukan")
    return {f"Terdapat {len(list_car)} mobil bekas yang memenuhi kriteria Anda": list_car}

def calculate_cicilan(harga_mobil: int, jangka_waktu: int, bunga_per_tahun: float) -> dict:
    angsuran_pokok = harga_mobil / (jangka_waktu*12)
    bunga_per_bulan = (bunga_per_tahun/12)*harga_mobil/100
    cicilan_per_bulan = angsuran_pokok + bunga_per_bulan
    return cicilan_per_bulan

def test():
    a = cars_serializer(cars_collection.find())
    for car in a:
        print(car['nama_mobil'])
        
def rekomendasi_mobil(max_harga_mobil: int, max_cicilan_per_bulan: int, bank: Bank):
    if bank.name == 'BCA':
        bunga_awal = 5.6
        bunga_akhir = 7
        tahun_awal = 3
        tahun_akhir = 2
    elif bank.name == 'Mandiri':
        bunga_awal = 6.1
        bunga_akhir = 7.15
        tahun_awal = 4
        tahun_akhir = 2
    elif bank.name == 'CIMB':
        bunga_awal = 3.69
        bunga_akhir = 7.25
        tahun_awal = 3
        tahun_akhir = 4
    else:
        bunga_awal = 6.25
        bunga_akhir = 6.75
        tahun_awal = 3
        tahun_akhir = 3
    tahun = tahun_akhir + tahun_awal
    car_by_harga = cars_serializer(cars_collection.find({"harga": {"$lt": max_harga_mobil}}))
    list_valid_car = []
    for car in car_by_harga:
        cicilan1 = calculate_cicilan(max_harga_mobil, tahun, bunga_awal)
        cicilan2 = calculate_cicilan(max_harga_mobil, tahun, bunga_akhir)
        if cicilan1 > cicilan2:
            cicilan = cicilan1
        else:
            cicilan = cicilan2
        if (cicilan < max_cicilan_per_bulan):
            list_valid_car.append(car)
    
    if len(list_valid_car) == 0:
        return ("Maaf, tidak ada mobil bekas yang memenuhi keinginan Anda")
    else:
        return (f"Ada {len(list_valid_car)} mobil bekas yang memenuhi keinginan Anda: ", list_valid_car)

def calculate_cicilan_bunga_fix(harga_mobil: int, jangka_waktu: int, bunga_per_tahun: float, persentase_uang_muka: float) -> dict:
    uang_muka = persentase_uang_muka*harga_mobil/100
    plafon_pinjaman = harga_mobil - uang_muka
    angsuran_pokok = plafon_pinjaman / (jangka_waktu*12)
    bunga_per_bulan = (bunga_per_tahun/12)*plafon_pinjaman/100
    cicilan_per_bulan = angsuran_pokok + bunga_per_bulan
    total_bayar = uang_muka + cicilan_per_bulan*jangka_waktu*12
    return {
        "Informasi Pinjaman Anda": {
            "Harga Mobil": f" Rp {harga_mobil}",
            "Uang Muka (DP)": f"Rp {round(uang_muka)}",
            "Plafon Pinjaman Anda": f" Rp {round(plafon_pinjaman)}",
            "Tenor": f"{jangka_waktu} tahun",
            "Bunga (flat)": f"{bunga_per_tahun}%",
            "Angsuran pertama": f"Rp {round(cicilan_per_bulan+uang_muka)}"
        },
        "Informasi Kredit Anda": {
            "Angsuran pokok per bulan": f"Rp {round(angsuran_pokok)}",
            "Angsuran bunga per bulan": f"Rp {round(bunga_per_bulan)}",
            "Total angsuran per bulan": f"Rp {round(cicilan_per_bulan)}"    
        },
        "Jumlah uang yang harus dibayar": f"Rp {round(total_bayar)}"
    }

def calculate_2_jenis_bunga(harga_mobil: int, persentase_uang_muka: float, bank: Bank) -> dict:
    if bank.name == 'BCA':
        bunga_awal = 5.6
        bunga_akhir = 7
        tahun_awal = 3
        tahun_akhir = 2
    elif bank.name == 'Mandiri':
        bunga_awal = 6.1
        bunga_akhir = 7.15
        tahun_awal = 4
        tahun_akhir = 2
    elif bank.name == 'CIMB':
        bunga_awal = 3.69
        bunga_akhir = 7.25
        tahun_awal = 3
        tahun_akhir = 4
    else:
        bunga_awal = 6.25
        bunga_akhir = 6.75
        tahun_awal = 3
        tahun_akhir = 3
        
    tahun = tahun_awal + tahun_akhir
    uang_muka = persentase_uang_muka*harga_mobil/100
    plafon_pinjaman = harga_mobil - uang_muka
    angsuran_pokok = plafon_pinjaman / (tahun*12)
    
    # Termin 1
    bunga_pertama = (bunga_awal/12)*plafon_pinjaman/100
    cicilan_pertama = angsuran_pokok + bunga_pertama
    
    # Termin 2
    bunga_kedua= (bunga_akhir/12)*plafon_pinjaman/100
    cicilan_kedua = angsuran_pokok + bunga_kedua
    
    # Total
    total_bayar = uang_muka + cicilan_pertama*tahun_awal*12 + cicilan_kedua*tahun_akhir*12
    return {
        "Informasi Pinjaman Anda": {
            "KKB Bank": bank,
            "Harga Mobil": f" Rp {harga_mobil}",
            "Uang Muka (DP)": f"Rp {round(uang_muka)}",
            "Plafon Pinjaman": f" Rp {round(plafon_pinjaman)}",
            "Angsuran pokok per bulan": f"Rp {round(angsuran_pokok)}",            "Angsuran awal": f"Rp {round(cicilan_pertama+uang_muka)}"
        },
        "Angsuran Termin 1": {
            "Lama termin 1": f"{tahun_awal} tahun",
            "Bunga termin 1": f"{bunga_awal}%",
            "Angsuran bunga termin 1": f"Rp {round(bunga_pertama)}",
            "Angsuran per bulan termin 1": f"Rp {round(cicilan_pertama)}"    
        },
        "Angsuran Termin 2": {
            "Lama termin 2": f"{tahun_akhir} tahun",
            "Bunga termin 2": f"{bunga_akhir}%",
            "Angsuran bunga termin 2": f"Rp {round(bunga_kedua)}",
            "Angsuran per bulan termin 2": f"Rp {round(cicilan_kedua)}" 
        },
        "Jumlah uang yang harus dibayar": f"Rp {round(total_bayar)}"
    }
    
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
        results = int(carSchema.get_estimated_car_price(perusahaan, nama_mobil, tahun, odo, transmisi))
        return results
    except:
        return "Data mobil tidak ditemukan"
    
def car_serializer(car) -> dict:
    return{
        "id": str(car["_id"]),
        "perusahaan": car["perusahaan"],
        "nama_mobil": car["nama_mobil"],
        "tahun": car["tahun"],
        "odo": car["odo"],
        "jenis_transmisi": car["jenis_transmisi"],
        "harga": car["harga"]
    }

def cars_serializer(cars) -> list:
    return [car_serializer(car) for car in cars]