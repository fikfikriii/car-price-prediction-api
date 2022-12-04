import pickle
import numpy as np

global model
with open('./server/models/home_price_prediction.pickle', 'rb') as f:
    model = pickle.load(f)

def house_serializer(house) -> dict:
    return{
        "lb": house["lb"],
        "lt": house["lt"],
        "kt": house["kt"],
        "km": house["km"],
        "grs": house["grs"]
    }

def houses_serializer(houses) -> list:
    return [house_serializer(house) for house in houses]

def get_estimated_price(lb, lt, kt, km, grs):
    x = np.zeros(5)
    x[0] = lb
    x[1] = lt
    x[2] = kt
    x[3] = km
    x[4] = grs
    print(x)
    return round(model.predict([x])[0], -3)