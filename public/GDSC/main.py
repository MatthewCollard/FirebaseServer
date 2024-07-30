import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np

from PyQt6.QtWidgets import QMainWindow,QListView, QApplication, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QStackedLayout, QLabel, QGridLayout, QListWidget, QListWidgetItem
from PyQt6.QtGui import QPalette, QColor, QGuiApplication
from PyQt6.QtCore import QDir, QRect, Qt,QSize
from PyQt6.QtGui import QIcon, QPixmap, QFont

from pyscript import display





class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GDSC Marine Garbage Detection")
        self.screen_size = QGuiApplication.primaryScreen().availableGeometry()#QDesktopWidget().screenGeometry(0)
        print(self.screen_size.width())
        screen_height = self.screen_size.height()
        screen_width = self.screen_size.width()
        x_pos = 0
        y_pos = 0
        self.setGeometry(x_pos, y_pos, screen_width, screen_height)
        self.showMaximized()
        #self.root=tk.Tk()
        


        #self.stacklayout = QStackedLayout()
        if(1):
            
            #mainLayout=QGridLayout()
            self.mainLayout=QStackedLayout()
            if(1):
                
                self.buttonLayout=QHBoxLayout()
                #self.setFixedHeight(300)
                self.button1 = QPushButton("Import Trash")
                #button1.pressed.connect(self.close)
                self.button1.pressed.connect(self.changeToImportImages)
                #button1.resize(200,50)
                self.button2 = QPushButton("Import Model")
                #self.button2.pressed.connect(self.close)
                self.button2.pressed.connect(self.changeToImportDataSet)

                self.button1.setMinimumSize(50,100)
                self.button2.setMinimumSize(50,100)

                #button2.resize(200,50)
                self.buttonLayout.addWidget(self.button1)
                self.buttonLayout.addWidget(self.button2)
                self.buttonLayout.setSpacing(100)
                buttonLayoutSize=QRect(50,100,50,100)
                self.buttonLayout.setContentsMargins(100,10,100,10)
                self.buttonLayout.setGeometry(buttonLayoutSize)
                self.button1.setStyleSheet('QPushButton {background-color: #A3C1DA; color: black;}')
                self.button2.setStyleSheet('QPushButton {background-color: #A3C1DA; color: black;}')
            #w=WidgetButton()
        #mainLayout.addLayout(self.stacklayout)
            if(1):
                self.importImageLayout=QVBoxLayout()
                self.importImageListLayout=QHBoxLayout()
                self.findImageLayout=QHBoxLayout()

                self.imageListView=QListWidget()
                self.imageListView.setIconSize(QSize(416,416))
                self.importButton=QPushButton("Import images")
                self.importButton.setMinimumSize(200,150)
                self.importButton.pressed.connect(self.importImages)
                self.importButton.setStyleSheet('QPushButton {background-color: #A3C1DA; color: black;}')
                self.imageListView.setStyleSheet('QPushButton {background-color: #A3C1DA; color: black;}')
                
                self.findButton=QPushButton("Find Trash")
                self.findButton.setMinimumSize(50,100)
                self.findButton.setMaximumSize(500,100)
                self.findButton.pressed.connect(self.classify)
                self.findButton.setStyleSheet('QPushButton {background-color: #A3C1DA; color: black;}')

                self.importImageListLayout.addWidget(self.importButton)
                self.importImageListLayout.addWidget(self.imageListView)

                self.findImageLayout.addWidget(self.findButton)
                tempWidget=QWidget()
                tempWidget.setLayout(self.importImageListLayout)
                tempWidget2=QWidget()
                tempWidget2.setLayout(self.findImageLayout)
                self.importImageLayout.addWidget(tempWidget)
                self.importImageLayout.addWidget(tempWidget2)
                self.importImageLayout.setSpacing(50)
                self.importImageLayout.setContentsMargins(100,10,100,10)

            if(1):
                self.resultsLayout=QVBoxLayout()
                widgetFont = QFont()
                widgetFont.setWeight(40)
                widgetFont.setPointSize(24)
                self.resultsSubLayout=QHBoxLayout()
                self.resultsListView=QListWidget()
                #self.originalListView=QListWidget()
                self.resultsListView.setIconSize(QSize(416,416))
                self.resultsSubLayout.addWidget(self.resultsListView)
                self.resultsListView.setFont(widgetFont)
                #self.resultsSubLayout.addWidget(self.originalListView)
                self.resultsLayout.setSpacing(100)
                self.importImageLayout.setContentsMargins(100,10,100,10)
                tempWidget3=QWidget()
                tempWidget3.setLayout(self.resultsSubLayout)
                self.resultsLayout.addWidget(tempWidget3)

                self.resultsLayout.setSpacing(100)



            mainMenuWidget=QWidget()
            #p=mainMenuWidget.palette()
            #p.setColor(w.backgroundRole(), QColor('red'))
            #mainMenuWidget.setAutoFillBackground(True)
            #mainMenuWidget.setPalette(p)
           

            #background = QPixmap('GarbageBackgroundPhoto.jpg').scaledToWidth(screen_width)
            #stylesheet = 'border-image: url("GarbageBackgroundPhoto.jpg");'
            #mainMenuWidget.setStyleSheet(stylesheet)
            #mainMenuWidget.setPixmap(QPixmap('GarbageBackgroundPhoto.jpg'))
            #mainLayout.addWidget(Color('blue'))
        #layout.addWidget(Color('red'))
            #label2 = QLabel("I want this text to appear on top of background image")
            #buttonLayout.addWidget(label2)
            #mainLayout.addLayout(w)
            #w.show()
            self.buttonWidget=QWidget()
            self.buttonWidget.setLayout(self.buttonLayout)
            self.mainLayout.addWidget(self.buttonWidget)

            self.imageImportWidget=QWidget()
            self.imageImportWidget.setLayout(self.importImageLayout)
            self.mainLayout.addWidget(self.imageImportWidget)

            self.resultsWidget=QWidget()
            self.resultsWidget.setLayout(self.resultsLayout)
            self.mainLayout.addWidget(self.resultsWidget)
            
            #mainLayout.addWidget(Color('blue'))
            self.mainLayout.setContentsMargins(0,0,0,0)
            self.mainLayout.setSpacing(0)

            mainMenuWidget.setLayout(self.mainLayout)
        
            self.setCentralWidget(mainMenuWidget)
class Color(QWidget):
    def __init__(self,color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)
        
        palette=self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

class WidgetButton(QWidget):
    def __init__(self, parent=None):
        super(WidgetButton, self).__init__(parent)
        buttonLayout=QHBoxLayout()
        self.setFixedHeight(300)
        button1 = QPushButton("Import Trash")
        button1.pressed.connect(self.close)
        button1.setStyleSheet("background-color: green; color: white;")
        #button1.resize(200,50)
        button2 = QPushButton("Import Model")
        button2.pressed.connect(self.close)
        #button2.resize(200,50)
        buttonLayout.addWidget(button1)
        buttonLayout.addWidget(button2)
        buttonLayout.setSpacing(30)
        #buttonLayoutSize=QRect(50,100,50,100)
        buttonLayout.setContentsMargins(10,10,10,10)
        #buttonLayout.setGeometry(buttonLayoutSize)


# First create the x and y coordinates of the points.
n_angles = 36
n_radii = 8
min_radius = 0.25
radii = np.linspace(min_radius, 0.95, n_radii)

angles = np.linspace(0, 2 * np.pi, n_angles, endpoint=False)
angles = np.repeat(angles[..., np.newaxis], n_radii, axis=1)
angles[:, 1::2] += np.pi / n_angles

x = (radii * np.cos(angles)).flatten()
y = (radii * np.sin(angles)).flatten()
z = (np.cos(radii) * np.cos(3 * angles)).flatten()

# Create the Triangulation; no triangles so Delaunay triangulation created.
triang = tri.Triangulation(x, y)

# Mask off unwanted triangles.
triang.set_mask(np.hypot(x[triang.triangles].mean(axis=1),
                            y[triang.triangles].mean(axis=1))
                < min_radius)

fig1, ax1 = plt.subplots()
ax1.set_aspect('equal')
tpc = ax1.tripcolor(triang, z, shading='flat')
fig1.colorbar(tpc)
ax1.set_title('tripcolor of Delaunay triangulation, flat shading')

display(fig1, target="mpl")

#w = MainWindow()
#display(w,target="mainapp")
#w.show()
stylesheet = """
    MainWindow {
        background-image: url("AnimatedOcean.jpg"); 
        background-repeat: no-repeat; 
        background-position: center;
    }
"""

custom_font = QFont()
custom_font.setWeight(26);
#QApplication.setFont(custom_font, "QLabel")
app = QApplication(sys.argv)
app.setFont(custom_font)
app.setStyleSheet(stylesheet)
w = MainWindow()
display(w.show(),target="mpl")
display(app.exec())