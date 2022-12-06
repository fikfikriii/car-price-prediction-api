from pydantic import BaseModel, Field

class Car(BaseModel):
    perusahaan: str = Field(default=None)
    nama_mobil: str = Field(default=None)
    tahun: int = Field(default=None)
    odo: int = Field(default=None)
    jenis_transmisi: str = Field(default=None)
    class Config:
        schema_extra = {
            "car_demo" : {
                "id": "1",
                "perusahaan": "Honda",
                "nama_mobil": "Jazz",
                "tahun": 2008,
                "odo": 120000,
                "jenis_transmisi": "Automatic",
                "harga": 90000000
            }
        }