import os, sys,time
import datetime as dt
from PyQt5 import QtWidgets, QtGui
from PyQt5.uic import loadUi
from picamera2 import Picamera2, Preview
from libcamera import controls

class MyGUI(QtWidgets.QMainWindow):
    #A simple application for collecting data, no error-proof design, only test before going out.
    def __init__(self):
        super().__init__()
        loadUi('/home/pi/Desktop/metar_project/photo_take.ui',self)  #  <-----import UI designed in QT designer
        #write connections to methods, photo configs were pre-set, suffixes were included for future convenience
        self.pushButton_1.clicked.connect(lambda:self.take_picture(config = {"Contrast":1,"ExposureValue":0}, suffix = "N")) #button 1 for normal exposure
        self.pushButton_2.clicked.connect(lambda:self.take_picture(config = {"Contrast":1,"ExposureValue":1}, suffix = "O")) #button 2 for over exposure
        self.pushButton_3.clicked.connect(lambda:self.take_picture(config = {"Contrast":1, "ExposureValue":-1}, suffix = "U")) #button 3 for under exposure
        #take 3 photos for HDR merging
        self.pushButton_4.clicked.connect(self.HDR_captures)
        #save user input info, this can be further imporved by fetching METAR from online source
        self.pushButton_5.clicked.connect(self.save_metar)

        
    #class methods, to be triggered by user behaviour
    def take_picture(self,config,suffix):
        #record time point(tp) to be taken as file name, for both img and txt
        global tp_string
        tp = dt.datetime.now()
        tp_string = tp.strftime("%Y%m%d-%H%M%S")
        
        #capture a still image
        picam2 = Picamera2()
        tp_img = tp_string + suffix + '.jpg'
        picam2.configure() #initialse config parameters
        picam2.set_controls(config) #set config before the camera starts
        picam2.start(show_preview=False) #preview is turned off to avoid conflict with the programme
        brightness = round(picam2.capture_metadata()['Lux'],1) #save lux value as environment factor
        picam2.start_and_capture_file(tp_img)  #capture a still image and save
        picam2.close()

        #attach thumbmail to graphic show (create scene and attach pix img on)
        scene = QtWidgets.QGraphicsScene()
        scene.setSceneRect(0, 0, 400, 225)       # QGraphicsScene scene size = 400*225
        img = QtGui.QPixmap(tp_img)
        img = img.scaled(400,225)                # picture size = 400*225
        scene.addPixmap(img)
        self.graphicsView.setScene(scene)
        
        #set lux value onto textEdit
        self.textEdit.setText(f"Lux:{brightness}")
        self.textEdit.setReadOnly(False)
    
    def HDR_captures(self):
        self.label.clear()
        global tp_string
        tp = dt.datetime.now()
        tp_string = tp.strftime("%Y%m%d-%H%M%S")
        brightness = 0 #initial value
        
        suffix_dict = {-2:"_under.jpg",0:"_normal.jpg",2:"_over.jpg"}  #fixed local parameters
        for value, suffix in suffix_dict.items():
            #capture 3 still image with different exposure values to create high dynamic range photo
            picam2 = Picamera2()
            picam2.configure() 
            picam2.set_controls({"ExposureValue":value}) #load Exposure value from dict
            tp_img = tp_string+suffix #make unique name for each photo
            picam2.start(show_preview=False)
            brightness += picam2.capture_metadata()['Lux'] #accumulate 3 Lux value
            #brightness =round(brightness,1)
            picam2.start_and_capture_file(tp_img)  #capture a still image and save
            picam2.close()
        
        #show message on panel
        brightness = round(brightness/3,1) #average, this is close to normal (grey level 5) value
        self.label.setText('HDR capture success!')  
        self.textEdit.setText(f"Lux:{brightness}")
        self.textEdit.setReadOnly(False)
        
    def save_metar(self):
        #save user input metar info
        metar_text = self.textEdit.toPlainText()
        tp_text = tp_string + '.txt'
        with open(tp_text,'w') as file:
            file.write(metar_text)

#All ready, initilise app
if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyGUI()
    window.show()
    app.exec_()
    del app
