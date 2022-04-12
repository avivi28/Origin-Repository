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
                data=queryAll("SELECT * FROM attractions WHERE name LIKE %s LIMIT 12 OFFSET %s", (keyword, limit_page,))
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
                    id=data[x][0]
                    name=data[x][1]
                    category=data[x][2]
                    description=data[x][3]
                    address=data[x][4]
                    transport=data[x][5]
                    mrt=data[x][6]
                    latitude=data[x][7]
                    longitude=data[x][8]
                    images_data=data[x][9].replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').split(",")
                    
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
                    id=data[x][0]
                    name=data[x][1]
                    category=data[x][2]
                    description=data[x][3]
                    address=data[x][4]
                    transport=data[x][5]
                    mrt=data[x][6]
                    latitude=data[x][7]
                    longitude=data[x][8]
                    images_data=data[x][9].replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').split(",")
                    
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

attraction_model=AttractionModel()