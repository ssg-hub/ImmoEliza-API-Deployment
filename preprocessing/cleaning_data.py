import json

def error_msg(error_number):
    error_dict = {
    1: "Error : Area of property should be an integer",
    2: "Error: Type of property should be an House/Apartment/Others",
    3: "Error: Number of Rooms of property should be an integer",
    4: "Error: Zip code of property should be an integer",
    }

    error = error_dict.get(error_number)

    return print(error)


def preprocess(json_data_for_property):
    x = json_data_for_property

    # parse x:
    y = json.loads(x)    

    # the result is a Python dictionary:

    #checking for valid inputs and giving errors in case inputs are invalid
    if type(y["data"]["area"])is not int : 
        return error_msg(1)
    if y["data"]["property-type"].upper() not in ["APARTMENT","HOUSE","OTHERS"] : 
        return error_msg(2)
    if type(y["data"]["rooms-number"]) is not int:
        return error_msg(3)
    if type(y["data"]["zip-code"]) is not int:
        return error_msg(4)    
      
    return y

home = '{	"data": {    "area": 56 ,    "property-type": "APATMENT" ,    "rooms-number": 2, "zip-code":48326}    }'
print(preprocess(home))

preprocess()
'''{
  "data": {
    "area": int,
    "property-type": "APARTMENT" | "HOUSE" | "OTHERS",
    "rooms-number": int,
    "zip-code": int,
    "land-area": Optional[int],
    "garden": Optional[bool],
    "garden-area": Optional[int],
    "equipped-kitchen": Optional[bool],
    "full-address": Optional[str],
    "swimming-pool": Optional[bool],
    "furnished": Optional[bool],
    "open-fire": Optional[bool],
    "terrace": Optional[bool],
    "terrace-area": Optional[int],
    "facades-number": Optional[int],
    "building-state": Optional[
      "NEW" | "GOOD" | "TO RENOVATE" | "JUST RENOVATED" | "TO REBUILD"
    ]
  }
}'''

