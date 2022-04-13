from flask import *
from model.database import queryAll,queryOne

class AttractionModel:
    def get(self):
        try:
            page=request.args.get("page",0)
            page=int(page)
            limit_page=page*12
            keyword=request.args.get("keyword")

            if keyword is not None:
                keyword="%"+keyword+"%"
                data=queryAll("SELECT * FROM attractions WHERE attractions_name LIKE %s LIMIT 12 OFFSET %s", (keyword, limit_page,))
                data=list(data)
                if len(data)>=13: #in case 有整數
                    next_page=page+1
                else:
                    null=None
                    next_page=null
                success_data_return={
                "nextPage": next_page,
                "data": []
                }
                
                for x in range(0,len(data)):
                    id=data[x]['attractions_id']
                    name=data[x]['attractions_name']
                    category=data[x]['category']
                    description=data[x]['description']
                    address=data[x]['address']
                    transport=data[x]['transport']
                    mrt=data[x]['mrt']
                    latitude=data[x]['latitude']
                    longitude=data[x]['longitude']
                    images_data=data[x]['images'].replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').split(",")
                    
                    temp = {
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
                    success_data_return["data"].append(temp)
                return success_data_return
            else:
                data=queryAll("SELECT * FROM attractions LIMIT 12 OFFSET %s", (limit_page,))
                data=list(data)
                if len(data)>=12:
                    next_page=page+1
                else:
                    null=None
                    next_page=null
                success_data_return={
                "nextPage": next_page,
                "data": []
                }
                
                for x in range(0,len(data)):
                    id=data[x]['attractions_id']
                    name=data[x]['attractions_name']
                    category=data[x]['category']
                    description=data[x]['description']
                    address=data[x]['address']
                    transport=data[x]['transport']
                    mrt=data[x]['mrt']
                    latitude=data[x]['latitude']
                    longitude=data[x]['longitude']
                    images_data=data[x]['images'].replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').split(",")
                    
                    temp = {
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
                    success_data_return["data"].append(temp) #要一步步塞data進去
                return success_data_return
        except:
            true = True
            error_message={
                "error": true,
                "message": "Server Side Error!"
            }
            return error_message
        
    def getId(self,attractionId):
        try:
            attractionId=int(attractionId)
            Id_data=queryOne("SELECT * FROM attractions WHERE attractions_id = %s", (attractionId,))

            images_data=Id_data['images'].replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').split(",")

            success_idData_return={
                "data": {
                    "id": Id_data['attractions_id'],
                    "name": Id_data['attractions_name'],
                    "category": Id_data['category'],
                    "description": Id_data['description'],
                    "address": Id_data['address'],
                    "transport": Id_data['transport'],
                    "mrt": Id_data['mrt'],
                    "latitude": Id_data['latitude'],
                    "longitude": Id_data['longitude'],
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

attraction_model=AttractionModel()