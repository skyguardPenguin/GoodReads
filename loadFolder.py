import os
import redis
import re
import json
import util
r = redis.Redis(host='localhost', port=6379, db=0)


# def load_folder(path):
#     files = os.listdir(path)
#     print(files)
#     for file in files:
#         match = re.match(r'^book(\d+).html$', file)
#         if match:
#             with open(path + file) as f:
#                 html = f.read()
#                 r.set(match.group(1), html)
#             print(match.group(0), match.group(1))


def load_json_elements(path, pattern):
    files = os.listdir(path)
    print(f"\t{files}")
    for file in files:
        match = re.match(r'^book(\d).json$',file)
        if(match):
            data = util.getJson(path + file)
            r.set(pattern + match.group(1),data[pattern])
            print(f"\tLibro {data['title']} guardado con éxito con la llave: {pattern}{match.group(1)}.")

def load_html_elements(path):
    files = os.listdir(path)
    print(files)
    for file in files:
        match = re.match(r"^[a-z0-9A-Z]*\.html$",file)
        if(match):
            fName = match.group(0).replace(".html","")
            data = util.getHtml(path + file)
            r.set(fName, data)
            print(f"\tPlantilla {fName} guardada con éxito con la llave: {fName}.")
        else:
            print(f"El archivo {file} no cumple con el patrón buscado")






print("Cargando información...")
print("Tútulos:")
load_json_elements('json/',"title")
print("Autores:")
load_json_elements('json/',"author")
print("Prefacios: ")
load_json_elements('json/',"preface")
print("Plantillas:")
load_html_elements('html/')

