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