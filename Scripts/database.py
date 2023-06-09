#compando para gerar as bibliotecas
#pip freeze > requirements.txt
#comando para instalar elas
#pip install -r requirements.txt
from pymongo import MongoClient
import json

def connect_to_database(databaseNameToConnect):
    client = MongoClient("mongodb+srv://IfscUser:IFSC2022@ifsccomponenteseletroni.6ixxshw.mongodb.net/test")

    db = client["ListaPinosComponentes"]
  
    Collection = db[databaseNameToConnect]

    return Collection

def return_component(componentName):
    collection = connect_to_database("ComponentesDigitais")
    cursor = collection.find({"nome":componentName})

    for record in cursor:
        return record
    
def return_DAQ_schematic():
    collection = connect_to_database("DAQ")
    cursor = collection.find({"nomeEquipamento":"Dev1"})
    for record in cursor:
        return record        

def return_expected_result(componentName):
    collection=connect_to_database("ResultadosEsperados")
    cursor = collection.find({"componente":componentName})
    for record in cursor:
        print('é o recorddd',record)
        return record
    

def return_allLinesDaq_digitalVersion():
    collection = connect_to_database("DAQ")
    cursor = collection.find({"nomeEquipamento":"Dev1"})
    for record in cursor:
        return record["pinosDigitais"]
    
def add_document_in_the_collection(filePath):
    if '/Cadastros/esquematicoDoComponente.txt' in filePath:
        collection = connect_to_database("ComponentesDigitais")
        with open(filePath, 'r') as arquivo_json:
            document = json.load(arquivo_json)
    else:
        collection = connect_to_database("ResultadosEsperados")
        with open(filePath, 'r') as arquivo_json:
            document = json.load(arquivo_json)
  
    return(collection.insert_one(document))    



