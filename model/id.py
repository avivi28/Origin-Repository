from flask import *
from model.database import queryOne

class IdModel:
    def getId(self,attractionId):
        try:
            attractionId=int(attractionId)
            Id_data=queryOne("SELECT * FROM attractions WHERE id = %s", (attractionId,))

            id=Id_data[0]
            name=Id_data[1]
            category=Id_data[2]
            description=Id_data[3]
            address=Id_data[4]
            transport=Id_data[5]
            mrt=Id_data[6]
            latitude=Id_data[7]
            longitude=Id_data[8]
            images_data=Id_data[9].replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').split(",")

            success_idData_return={
                "data": {
                    "id": id,
                    "name": name,
                    "category": category,
                    "description": description,
                    "address": address,
                    "transport": transport,
                    "mrt": mrt,
                    "latitude": latitude,
                    "longitude": longitude,
                    "images": images_data
                    }
                }
            return success_idData_return
        except TypeError: 
            true = True
            error_message={
                "error": true,
                "message": "Wrong Request ID!"
            }
            return error_message
        except:
            true = True
            error_message={
                "error": true,
                "message": "Server Side Error!"
            }
            return error_message
        
id_model = IdModel()