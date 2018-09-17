import sys,os
from layout2 import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication,QListWidgetItem
from PyQt5.QtGui import QImage,QPixmap,QPalette,QPainter,QPen,QIcon
from PyQt5.QtCore import pyqtSlot,QTimer,Qt,QSize
import numpy as np
import cv2
import requests
import json
import dlib
import jsonpickle
from threading import Thread
from queue import Queue

frame = None
frameQ = Queue()
#host = '10.2.137.179'
host = 'localhost'
port = '5000'
class imageSender:
    def __init__(self):
        self.base_url = 'http://{}:{}'.format(host,port)
        self.api = self.base_url + '/api/facedetection'
        self.content_type = 'image/jpeg'
        self.headers = {'content-type': self.content_type}

    def send(self,img):
        _, img_encoded = cv2.imencode('.jpg', img)
        try:
            response = requests.post(self.api, data=img_encoded.tostring(), headers=self.headers)
            print('reponse msg:{}'.format(response.text))
            return json.loads(response.text)
        except Exception as e:
            print(str(e))
            return {}

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setAcceptDrops(True)
        self.cap = cv2.VideoCapture()
        self.file_opened = False
        self.frame = None
        self.frame2 = None
        self.ret = False
        self.play.clicked.connect(self.on_click)
        self.pause.clicked.connect(self.pause_btn)
        self.timer = QTimer()
        self.timer.timeout.connect(self._showVideoFrame)
        self.video_width = self.video_view.frameGeometry().width()
        self.video_height = self.video_view.frameGeometry().height()
        self.frame_sender = imageSender()
        self.imageQ = Queue()
        self.detectionThread = None
        self.detection_res = []
        #for i in range(10):
        #    self.res_list.addItem("item {}".format(i))
        #print(dir(self.video_view.picture()))

    def _send2server(self,img):
        res = self.frame_sender.send(img)
        self.detection_res = res.get('yolo_res',[])
        self.res_list.clear()
        self.res_list.setIconSize(QSize(200,200))      
        #self.res_list.setSizeHint((50,50))  
        for detected_obj in self.detection_res:
            box = '{} {} {} {}'.format(detected_obj.get('top'),detected_obj.get('left')
                    ,detected_obj.get('bottom'),detected_obj.get('right'))
            #self.res_list.addItem('{}\n{}'.format(detected_obj.get('class'),box))
            roi = self._draw_rect(img,detected_obj)
            #qroi = self._convert_cv2Qtimg(roi)
            pixmap = self._matToQImage(roi)
            pix = QPixmap.fromImage(pixmap)            
            item = QListWidgetItem()
            #print(roi.shape)
            item.setIcon(QIcon(pix))            
            item.setSizeHint(QSize(roi.shape[1],roi.shape[0]))
            
            self.res_list.addItem(item)




    def _send_to_server(self):
        print('thread start')
        while not self.imageQ.empty():
            img = self.imageQ.get()
            self._send2server(img)
            '''
            res = self.frame_sender.send(img)
            '''
            self.detection_res = res.get('centers',[])
            self.res_list.clear()
            for i, c in enumerate(self.detection_res):
                self.res_list.addItem('face {}:{}'.format(i,c))
            
            #n = self._draw_dots(self.frame,self.detection_res)
            #self._convert_cv2Qtimg(n)
    
    def _matToQImage(self,img):
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        height, width, channel = img.shape
        bytesPerLine = channel * width
        return QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)

    def _clearFrame(self):
        color = self.palette().color(QPalette.Background)
        size = self.video_width, self.video_height, 3
        m = np.zeros(size, dtype=np.uint8)
        m+=color.red()
        self._convert_cv2Qtimg(m)

    def _fit_size(self,img):
        img_height, img_width, _=img.shape 
        scale = img_height/self.video_height
        new_size = (int(img_width/scale),int(img_height/scale))
        return cv2.resize(img,new_size)
        pass

    def _convert_cv2Qtimg(self,img):
        if not isinstance(img,np.ndarray):
            return
        img = self._fit_size(img)
        pixmap = self._matToQImage(img)
        pix = QPixmap.fromImage(pixmap)
        self.video_view.setPixmap(pix)

    def _draw_rect(self,img,det_res):
        #img2 = img.copy()
        top = int(det_res.get('top'))
        left = int(det_res.get('left'))
        bottom = int(det_res.get('bottom'))
        right = int(det_res.get('right'))
        pt1 = int(left),int(top)
        pt2 = int(right),int(bottom)
        cv2.rectangle(img,pt1,pt2,(255,0,0),3)

        fontFace = cv2.FONT_HERSHEY_SIMPLEX
        label = det_res.get('class')
        if top <= 10:
            top = top+20
        cv2.putText(img, label, (left,top), fontFace, 1.5, (0,0,255), 2)

        #roi = im[y1:y2, x1:x2]
        #return img2[top:bottom,left:right,:]
        return self.frame2[top:bottom,left:right,:]

    def _draw_dots(self,img,dots):
        print(dots)
        for center in dots:
            cv2.circle(img,(center[0],center[1]),1,(255,0,0),10)

    def _showVideoFrame(self):

        self.ret, self.frame = self.cap.read()
        if self.ret == True:
            self.frame2 = self.frame.copy()
            #frame = self.frame
            #self.imageQ.put(self.frame)
            self._send2server(self.frame)
            print(self.frame.shape)
            #print(self.imageQ.qsize())
            #frame_s.send()
            #res = self._send_to_server(self.frame)
            #centers = res.get('centers')
            #self._draw_dots(self.frame,centers)
            self._convert_cv2Qtimg(self.frame)
            print('read frame success')
        else:
            self.timer.stop()
            if isinstance(self.detectionThread,Thread):
                #self.detectionThread.join()
                pass
            #self._clearFrame()
            print('read frame fail')

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.timer.stop()
        for url in e.mimeData().urls():
            path = url.toLocalFile()
            if os.path.isfile(path):
                print('open file:{}'.format(path)) 
                self.file_opened = self.cap.open(path)
                if self.file_opened:
                    print('open file success')
                    #self.detectionThread = Thread(target=self._send_to_server)
                    self._showVideoFrame()

    @pyqtSlot()
    def on_click(self):
        print('click play button')
        if self.ret == True:
            self.timer.start(33)
            #self.detectionThread.start()
    @pyqtSlot()
    def pause_btn(self):
        print('click pause button')
        self.timer.stop()

                        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
