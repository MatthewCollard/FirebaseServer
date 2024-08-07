import numpy as np
import panel as pn
import pandas as pd
import glob
from bokeh.models import ColumnDataSource
from pyscript import display
from pyscript import document
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import js

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

def resize_image(img, output_div):
    canvas = js.document.createElement("canvas")
    canvas.width = 416
    canvas.height = 416
    ctx = canvas.getContext("2d")
    ctx.drawImage(img, 0, 0, 416, 416)
            
    resized_img = canvas.toDataURL("image/jpeg")
    resized_images.append(resized_img)

    container = js.document.createElement("div")
    container.className = "image-container"
            
            # Create label element
    label = js.document.createElement("p")
    label.textContent = classify(resized_img)
            # Display the resized image in the output div
    output_img = js.document.createElement("img")
    output_img.src = resized_img
    output_img.alt = img.alt

    container.appendChild(output_img)
    container.appendChild(label)
    
    output_div.appendChild(container)
    js.uploadImage(resized_img,file_name)


def importing(event):
    loaded_model = load_model("./marinemodel.h5")
    input_text = document.querySelector("#ctrl")
    output_div = document.querySelector("#out")
    files = input_text.files
    #output_div.innerText = file_names
    
    
    def onload(event):
    # Create an image element and set its source to the file data
        img = document.createElement("img")
        img.src = event.target.result
        print("got here")
        img.alt = event.target.result
        img.style.margin = "10px"

        img.onload = lambda e: resize_image(img, output_div)
        # Append the image to the output div
        #output_div.appendChild(img)
        
    for i in range(files.length):
        file=files.item(i)
        reader = js.FileReader.new()
        reader.onload = onload
        reader.readAsDataURL(files.item(i))
        
    
    
    #display(files.item(1))





#df = pd.DataFrame(np.random.randn(10, 4), columns=list('ABCD')).cumsum()
#tabulator = pn.widgets.Tabulator(df, height=450, width=400).servable(target='table')
#w=ApplicationLayer()
#w.importImages()



