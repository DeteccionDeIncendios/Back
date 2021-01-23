from flask import Flask, request, jsonify
from flask_cors import CORS


from io import BytesIO
from prediction import predictSimple
from werkzeug.utils import secure_filename
import os
from PIL import Image

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
print("THIS_FOLDER: ",THIS_FOLDER)
Upload =  os.path.join(THIS_FOLDER, 'upload')
Upload_modified = os.path.join(THIS_FOLDER, 'upload_modificado')
print("Upload: ",Upload)


app = Flask(__name__)
app.config['uploadFolder'] = Upload
app.config['uploadFolderModified'] = Upload_modified
CORS(app)


import firebase_admin
from firebase_admin import credentials, messaging
my_file = os.path.join(THIS_FOLDER, 'iaproject-9cd7b-firebase-adminsdk-66qpu-3f5f300eff.json')
cred = credentials.Certificate(my_file)
firebase_admin.initialize_app(cred)


@app.route("/predict", methods=["POST"])
def predict():

    #se recibe el request y se guarda las fotos en la carpeta upload
    listName = []
    listNameModified = []
    for file in request.files.listvalues():
        photo = file[0]
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['uploadFolder'], filename))
        img = Image.open(os.path.join(app.config['uploadFolder'], filename)).convert("RGB")
        img.save(os.path.join(app.config['uploadFolderModified'], "prueba.jpg" ))
        listName.append(Upload_modified+'/'+"prueba.jpg")

    #response base de ejecucion
    response = {"fireExists": False, "files":[], "label":"", "porcentaje":0}

    #se realiza la predccion y se retorna una lista de los archivos o fotos que sean de clase 'fuego'
    resp ,response["porcentaje"] = predictSimple(listName)

    #si existe alguna img de clase fuego se envia la notif a la app android
    if(len(resp) > 0):
        print("Se envia notificacion en caso de que exista alguna img de clase fuego")
        #este bloque se encarga de armar la estructura de la notif y enviarla a los dispositivos que tengan el app instalada 
        message = messaging.Message(
            data={
                "title":"Sistema de Detección",
                "body": "ALERTA INCENDIO DETECTADO",
                "color":"red"
            },
            topic="IA-PROJECT"
        )
        resMens = messaging.send(message)
        print(resMens)

    #se actualizan los valores de respuesta
    response["fireExists"] = len(resp) > 0
    response["files"] = resp
    response["label"] = "FIRE" if len(resp) > 0 else "NO FIRE"

    #se eliminan los archivos o img que se recibieron
    for file in listName:
        os.remove(file)

    #se eliminan los archivos o img modificados
    for file in listNameModified:
        os.remore(file)

    #se retorna la respuesta json
    return jsonify(response)

                    
if __name__ == "__main__":
    app.run(debug = True, port=8080)
