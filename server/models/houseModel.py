from pydantic import BaseModel, Field

class House(BaseModel):
    luas_bangunan: int = Field(default=None)
    luas_tanah: int = Field(default=None)
    jumlah_kamar_tidur: int = Field(default=None)
    jumlah_kamar_mandi: int = Field(default=None)
    jumlah_garasi: int = Field(default=None)
    class Config:
        schema_extra = {
            "house_demo" : {
                "lb": 130,
                "lt": 120,
                "kt": 3,
                "km": 3,
                "grs": 1
            }
        }