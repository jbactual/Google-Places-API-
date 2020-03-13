import json
import os

def write_json(fileName, jsonData, cityName):
    print("Writing Data To File")

    if not os.path.exists(f"data/{cityName}"):
        os.makedirs(f"data/{cityName}")
        
    with open(f"data/{cityName}/{fileName}", 'w+') as f:
        json.dump(jsonData, f)

def read_json(jsonFile):
    with open(jsonFile) as file:
        data = json.load(file)

    return data
