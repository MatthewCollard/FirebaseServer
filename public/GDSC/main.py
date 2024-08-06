import numpy as np
import panel as pn
import pandas as pd
import glob
from bokeh.models import ColumnDataSource
from pyscript import display
from pyscript import document
import js

class ApplicationLayer():
    def importImages(self):
            self.image_list = []
            self.imageNameList=[]
            print(folderPath)
            for filename in glob.glob(folderPath+'/*.jpg'): #assuming gif        
                filename=str(pathlib.PureWindowsPath(filename).as_posix())
                picture = Image.open(filename)
                self.image_list.append(picture)
                self.imageNameList.append(filename)
                picture.thumbnail((416, 416), Image.LANCZOS)
                icon = QIcon(QPixmap(filename))#QIcon(QPixmap.fromImage(ImageQt.ImageQt(picture)))
                item = QListWidgetItem(os.path.basename(filename)[:20] + "...", self.imageListView)
                item.setStatusTip(filename)
                item.setIcon(icon)

    def classify(self):
            print("Classify")
            for i in self.imageNameList:
                img = image.load_img(i, target_size=(416, 416)) 
                img_array = image.img_to_array(img)
                img_array = np.expand_dims(img_array, axis=0)
                
            #img_array /= 255.0  # Normalize the image pixel values
            #icon = QIcon(QPixmap(i))#QIcon(QPixmap.fromImage(ImageQt.ImageQt(picture)))
            #widgetFont = QFont()
            #widgetFont.setWeight(40)
            #widgetFont.setPointSize(24)
                predictions=self.loaded_model.predict(img_array)
                print("Source Image: "+i)
                print("Predicted Probabilites:")
                print(predictions)
                predicted_class_index = np.argmax(predictions)
                if(predicted_class_index==0):
                    print("Predicted Class: Clean")
                    item = QListWidgetItem("Predicted Class: Clean \n"+i, self.resultsListView)
                    item.setFont(widgetFont)
                else:
                    print("Predicted Class: Dirty")
                    item = QListWidgetItem("Predicted Class: Dirty \n"+i, self.resultsListView)
                    item.setFont(widgetFont)
                item.setStatusTip(i)
                item.setIcon(icon)

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
    label.textContent = "Dirty"
            # Display the resized image in the output div
    output_img = js.document.createElement("img")
    output_img.src = resized_img
    output_img.alt = img.alt

    container.appendChild(output_img)
    container.appendChild(label)
    
    output_div.appendChild(container)


def importing(event):
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



#self.loaded_model = load_model("./marinemodel.h5")

#df = pd.DataFrame(np.random.randn(10, 4), columns=list('ABCD')).cumsum()
#tabulator = pn.widgets.Tabulator(df, height=450, width=400).servable(target='table')
#w=ApplicationLayer()
#w.importImages()



