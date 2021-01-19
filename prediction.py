import numpy as np
import os
import re




import keras
import matplotlib.pyplot as plt
from skimage.transform import resize
from io import BytesIO


import numpy as np
from werkzeug.utils import secure_filename


clases = ['fuego', 'no_fuego']
batch_size = 32
img_height = 180
img_width = 180

def predictSimple(listName):
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, 'inicial_model_update4.h5')
    model = keras.models.load_model(my_file)
    images = []
    for file in listName:
        img = plt.imread(file,0)
        image_resized = resize(img, (36, 36),anti_aliasing=True,clip=False,preserve_range=True)
        images.append(image_resized)
        
    X = np.array(images, dtype=np.uint8) #convierto de lista a numpy
    test_X = X.astype('float32')
    test_X = test_X / 255.
    print(test_X)
    predicted_classes = model.predict(test_X)
    listResp = []
    porcent=0
    for i, img_tagged in enumerate(predicted_classes):
        print("Imagen: ", listName[i])
        classDetected = clases[img_tagged.tolist().index(max(img_tagged))];
        print("Clase detectada: ", classDetected)
        probability = max(img_tagged)*100
        print("Probabilidad: "+str(probability) + "%")
        print(listName[i], classDetected, probability)
        porcent=probability
        if(classDetected == "fuego"):
            listResp.append({"fileName": listName[i], "probability":str(probability)})
        print("")
    return listResp, porcent
