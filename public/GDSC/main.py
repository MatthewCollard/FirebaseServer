import numpy as np
from asyncio.windows_events import NULL
import panel as pn
import pandas as pd
import glob
import requests
import base64
from bokeh.models import ColumnDataSource
from pyscript import display
from pyscript import document
import js
#from pyscript.js_modules import code
FIREBASE_API_KEY = "AIzaSyA74K-gs9HxyKZK_V7C_U2WTf-O4arVzDg"
FIREBASE_STORAGE_BUCKET ="matthew-collard.appspot.com"
FIREBASE_UPLOAD_URL = f"https://firebasestorage.googleapis.com/v0/b/{FIREBASE_STORAGE_BUCKET}/o"

class FileTransfer:
    file=NULL

    @staticmethod
    def setFile(file):
        FileTransfer.file=file

    @staticmethod
    def getFile():
        return FileTransfer.file


#matthew-collard.appspot.com
def upload_image_to_firebase(image_data, file_name):
    headers = {
        "Authorization": f"Bearer {FIREBASE_API_KEY}",
        "Content-Type": "image/jpeg",
    }
    upload_url = f"{FIREBASE_UPLOAD_URL}/{file_name}?uploadType=media"
    response = requests.post(upload_url, headers=headers, data=image_data)
    if response.status_code == 200:
        print(f"Uploaded {file_name} successfully!")
    else:
        print(f"Failed to upload {file_name}. Status code: {response.status_code}, Error: {response.text}")

def classify(target):
    print("Classify")
    img = image.load_img(target, target_size=(416, 416)) 
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
                
    predictions=loaded_model.predict(img_array)
    predicted_class_index = np.argmax(predictions)
    if(predicted_class_index==0):
        return("Predicted Class: Clean")
    else:
        return("Predicted Class: Dirty")

resized_images=[]

def resize_image(img, file_name, output_div):
    canvas = js.document.createElement("canvas")
    canvas.width = 416
    canvas.height = 416
    ctx = canvas.getContext("2d")
    ctx.drawImage(img, 0, 0, 416, 416)
            
    resized_img = canvas.toDataURL("image/jpeg")
    image_data=base64.b64decode(resized_img)

    resized_images.append(resized_img)

    container = js.document.createElement("div")
    container.className = "image-container"
            
            # Create label element
    label = js.document.createElement("p")
    label.textContent = "Dirty"
            # Display the resized image in the output div
    output_img = js.document.createElement("img")
    output_img.src = resized_img
    output_img.alt = img.alt

    container.appendChild(output_img)
    container.appendChild(label)
    
    output_div.appendChild(container)
    upload_image_to_firebase(image_data,file_name)
    #code.uploadImage(resized_img,file_name)


def importing(event):
    input_text = document.querySelector("#ctrl")
    output_div = document.querySelector("#out")
    files = input_text.files
    #output_div.innerText = file_names
    
    def onload(event):
    # Create an image element and set its source to the file data
        img = document.createElement("img")
        img.src = event.target.result
        img.alt = event.target.result
        img.style.margin = "10px"

        img.onload = lambda e: resize_image(img, FileTransfer.getFile().name, output_div)
        # Append the image to the output div
        #output_div.appendChild(img)
        
    for i in range(files.length):
        FileTransfer.setFile(files.item(i))
        reader = js.FileReader.new()
        reader.onload = onload
        reader.readAsDataURL(files.item(i))
        
    
    
    #display(files.item(1))





#df = pd.DataFrame(np.random.randn(10, 4), columns=list('ABCD')).cumsum()
#tabulator = pn.widgets.Tabulator(df, height=450, width=400).servable(target='table')
#w=ApplicationLayer()
#w.importImages()



