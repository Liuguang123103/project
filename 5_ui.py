import sys
import cv2
import numpy
from PIL import Image
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog

from yolo3.card_seg import Cardseg
from yolo3.plate_ui import Ui_MainWindow
from yolo3.yolo import YOLO


class MyMainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, detector= None):
        super(MyMainWindow, self).__init__()
        self.detector = detector
        self.setupUi(self)
        # Button 的颜色修改
        button_color = [self.pushButton, self.pushButton_2, self.pushButton_3]
        for i in range(3):
            button_color[i].setStyleSheet("QPushButton{color:rgb(68,68,51)}"
                                          "QPushButton:hover{color:yellow}"
                                          "QPushButton{background-color:rgb(68,221,204)}"
                                          "QPushButton{border:55px}"
                                          "QPushButton{font: bold}"
                                          "QPushButton{border-radius:20px}"
                                          "QPushButton{padding:18px 4px}")
        self.pushButton.clicked.connect(self.button_open_img_click)
        self.pushButton_2.clicked.connect(self.button_detection_clicked)
        self.pushButton_3.clicked.connect(self.close_ui)

    def button_open_img_click(self):
        self.pushButton.setText(u'寻找图像')
        self.lineEdit.setText('')
        self.pic_path, _ = QFileDialog.getOpenFileName(self, '选择图片', r'.', 'Image files(*.jpg *.JPG *.png)')
        if self.pic_path:
            image = cv2.imread(self.pic_path)
            # image = cv2.resize(image,(580,360))
            show2 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # 视频色彩转换回RGB，这样才是现实的颜色
            showImage = QtGui.QImage(show2.data, show2.shape[1], show2.shape[0],
                                     QtGui.QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
            self.label.setPixmap(QtGui.QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage
            self.label.setScaledContents(True)  #自适应大小
            # self.label.setScaledContents(False)  #自适应大小


    def button_detection_clicked(self):
        if self.pic_path:
            image = Image.open(self.pic_path)
            detect_img, _, self.palte = detector.detect_image(image)
            palte = cv2.cvtColor(self.palte, cv2.COLOR_RGB2BGR)
            try:
                _, _, pre_palte = Cardseg([palte], ['blue'], None)
            except:
                pre_palte = ''
            save_path = ''
            for s in pre_palte:
                save_path += s
            if not save_path:
                self.lineEdit.setText(u'未识别')
            else:
                self.lineEdit.setText(save_path)
            show2 = numpy.array(detect_img)
            showImage = QtGui.QImage(show2.data, show2.shape[1], show2.shape[0],
                                     QtGui.QImage.Format_RGB888)  # 把读取到的视频数据变成QImage形式
            self.label.setPixmap(QtGui.QPixmap.fromImage(showImage))  # 往显示视频的Label里 显示QImage
            self.label.setScaledContents(True)  #自适应大小
            # self.label.setScaledContents(False)  #自适应大小

    def close_ui(self):
        sys.exit()

if __name__ == '__main__':
    detector = YOLO()
    app = QApplication(sys.argv)
    myWin = MyMainWindow(detector)
    myWin.show()
    sys.exit(app.exec_())
