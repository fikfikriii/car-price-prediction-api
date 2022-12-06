import pickle
import numpy as np
import json

global model
with open('./server/models/car_price_prediction.pickle', 'rb') as f:
    model = pickle.load(f)

global perusahaan
global mobil
global transmisi

global data_columns
with open('./server/models/data_json/car_columns.json', 'r') as f:
    data_columns = json.load(f)['data_columns']
    perusahaan = data_columns[2:]
    mobil = data_columns[2:]
    transmisi = data_columns[2:]

def get_data_columns():
    return data_columns

def get_nama_perusahaan():
    return perusahaan

def get_nama_mobil():
    return mobil

def get_transmisi():
    return transmisi

def get_estimated_car_price(perusahaan, mobil, tahun, odo, transmisi ): 
    try:
        perusahaan_index = data_columns.index(perusahaan.capitalize())
    except:
        perusahaan_index = -1
    
    try:
        mobil_index = data_columns.index(mobil.capitalize())
    except:
        mobil_index = -1
    
    try:
        transmisi_index = data_columns.index(transmisi.capitalize())
    except:
        transmisi_index = -1
        
    x = np.zeros(len(data_columns))
    x[0] = odo
    x[1] = tahun
    
    if perusahaan_index >= 0 and mobil_index >= 0 and transmisi_index >= 0:
        x[perusahaan_index] = 1
        x[mobil_index] = 1
        x[transmisi_index] = 1
        return model.predict([x])[0]
    
    return "Data mobil tidak ditemukan"


def car_serializer(car) -> dict:
    return{
        "id": str(car["_id"]),
        "perusahaan": car["perusahaan"],
        "nama_mobil": car["nama_mobil"],
        "tahun": car["tahun"],
        "odo": car["odo"],
        "jenis_transmisi": car["transmisi"],
        "harga": car["harga"]
    }

def cars_serializer(cars) -> list:
    return [car_serializer(car) for car in cars]