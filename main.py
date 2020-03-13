import os
from gmaps.places_api import places_api
from utils.json_rw import read_json
from utils.json_rw import write_json




def read_business_types():
    businessTypes = list()
    with open("business_types.txt", 'r') as f:
        text = f.readlines()

    for line in text:
        businessTypes.append(line.replace('\n', ''))

    return businessTypes


def main():
    try:
        data = read_json("us_cities.json")
        businessTypes = read_business_types()

        for bType in businessTypes:
            jsonData = {}

            for city in data["cities"]:
                try: 
                    cityName = city['city']
                    cityCoords = city["coordinates"]

                    #check through dirs/files if no file for type_city preform search
                    if not os.path.exists(f"data/{cityName}/{cityName}_{bType}.json"):
                        print(f"Performing {cityName} and {bType}")
                        jsonData[f"{bType}"] = places_api(bType, cityCoords)
                        write_json(f"{cityName}_{bType}.json", jsonData[f"{bType}"], cityName)
                except: 
                    continue
    
    except:
        print("Error")

        

    
# End of Main

main()

print("Done")
