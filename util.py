import json

def getJson(filePath):
    with open(filePath, "r") as file:
        return json.load(file)
    
def getHtml(filePath):
    with open(filePath) as f:
        return f.read()
    
