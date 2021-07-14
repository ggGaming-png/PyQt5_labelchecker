import sys
import os
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from functools import partial
import json


class picture(QWidget):
    def __init__(self, classlist):
        super(picture, self).__init__()
        
        self.resize(1000, 2500)
        self.setWindowTitle("检查图片")

        self.label = QLabel(self)
        self.label.setText("显示图片")
        self.label.setFixedSize(400, 800)
        self.label.move(100, 150)
        
        self.label.setStyleSheet("QLabel{background:white;}"
                                 "QLabel{color:rgb(300,300,300,120);font-size:10px;font-weight:bold;font-family:宋体;}"
                                 )

        # index
        self.index = 0
        self.check_occ = 0
        self.check_qua = 0
        self.check_box = 0
        # 导入文件夹
        self.pic_path_list = []
        btn = QPushButton(self)
        btn.setText("导入文件夹")
        btn.setGeometry(QRect(10,10,110,35))
        btn.clicked.connect(self.opendir)
        # print('self pic path is', self.pic_path_list)

        self.classlist = classlist
        # 创建标注类别按钮
        # get cfg class list
        # for 循环创建
        btn_list = []
        

        for i  in range(len(self.classlist)):
            btn = QPushButton(self)
            btn.setText(self.classlist[i])
            btn.setGeometry(QRect(10+110*i,45,110,35))
            btn_list.append(btn)

        for id in range(len(btn_list)):
            btn_list[id].clicked.connect(
                partial(self.writelabel, btn_list[id].text(), btn_list, id))
        self.labelstr = "OK! LET'S GO!"
        self.indexstr = "NOT FIND ENEMNY "

        self.checkstr_occ = "occ:"
        self.checkstr_qua = "qua:"
        self.checkstr_box = "box:"
        
        self.total = 0
        # 图片显示部分
        btn = QPushButton(self)
        btn.setText("显示图片")
        btn.setGeometry(QRect(10,80,110,35))
        btn.clicked.connect(self.showimage)

        btn = QPushButton(self)
        btn.setText("上一张")
        btn.setGeometry(QRect(120,80,110,35))
        btn.clicked.connect(self.show_beforeimage)

        btn = QPushButton(self)
        btn.setText("下一张")
        btn.setGeometry(QRect(230,80,110,35))
        btn.clicked.connect(self.show_nextimage)

        print(self.labelstr)
        self.lb1 = QLabel(self)        # add a label to this dialog
        self.lb1.setText(self.labelstr)
        self.lb1.setGeometry(QtCore.QRect(500, 500, 500, 100))
        self.lb1.setStyleSheet('background-color:#838383;color:white;font:bold 24px;')

        #显示该照片信息
        self.lb2 = QLabel(self)        # add a label to this dialog
        self.lb2.setText(self.indexstr)
        self.lb2.setGeometry(QtCore.QRect(500, 400, 500, 100))
        self.lb2.setStyleSheet('background-color:#fff0f0;color:orange;font:bold 30px;')
         
        #显示需要跳转的照片
        self.btn = QPushButton('跳转', self)
        self.btn.setGeometry(QtCore.QRect(850, 435, 50, 20))
        self.btn.clicked.connect(self.jumpTo)
        #occ_ check

        self.lb3 = QLabel(self)        # add a label to this dialog
        self.lb3.setText(self.checkstr_occ)
        self.lb3.setGeometry(QtCore.QRect(500, 200, 500, 70))
        self.lb3.setStyleSheet('background-color:#fff0f0;color:purple;font:bold 25px;')
        #qua_check
        self.lb4 = QLabel(self)        # add a label to this dialog
        self.lb4.setText(self.checkstr_qua)
        self.lb4.setGeometry(QtCore.QRect(500, 270, 500, 70))
        self.lb4.setStyleSheet('background-color:#fff0f0;color:purple;font:bold 25px;')
        #box_check 
        self.lb5 = QLabel(self)        # add a label to this dialog
        self.lb5.setText(self.checkstr_box)
        self.lb5.setGeometry(QtCore.QRect(500, 340, 500, 70))
        self.lb5.setStyleSheet('background-color:#fff0f0;color:purple;font:bold 25px;')

        #改正occasion错误率
        self.btn = QPushButton('+', self)
        # self.btn.move(800, 300)
        self.btn.clicked.connect(self.addOne_occ)
        self.btn.setGeometry(QtCore.QRect(940, 225, 30, 30))

        self.btn = QPushButton('-', self)
        # self.btn.move(850, 300)
        self.btn.clicked.connect(self.minusOne_occ)
        self.btn.setGeometry(QtCore.QRect(970, 225, 30, 30))

        #改正quality错误率
        self.btn = QPushButton('+', self)
        # self.btn.move(800, 300)
        self.btn.clicked.connect(self.addOne_qua)
        self.btn.setGeometry(QtCore.QRect(940, 295, 30, 30))

        self.btn = QPushButton('-', self)
        # self.btn.move(850, 300)
        self.btn.clicked.connect(self.minusOne_qua)
        self.btn.setGeometry(QtCore.QRect(970, 295, 30, 30))


        #改正box错误率
        self.btn = QPushButton('+', self)
        # self.btn.move(800, 300)
        self.btn.clicked.connect(self.addOne_box)
        self.btn.setGeometry(QtCore.QRect(940, 365, 30, 30))

        self.btn = QPushButton('-', self)
        # self.btn.move(850, 300)
        self.btn.clicked.connect(self.minusOne_box)
        self.btn.setGeometry(QtCore.QRect(970, 365, 30, 30))



        #索引跳转
        self.btn = QPushButton('跳转', self)
        self.btn.move(850, 435)
        self.btn.clicked.connect(self.jumpTo)
         
        self.btn = QPushButton('输入历史错误信息', self)
        self.btn.setGeometry(QRect(500,180,200,20))
        self.btn.clicked.connect(self.setchecks)


        
        #显示
    # 导入一个文件夹的图片
    # 返回包含图片路径的list

    def opendir(self):
        file_path = QFileDialog.getExistingDirectory(
            self, "请选择模板保存路径...", "./")
        print(file_path)
        pic_list = os.listdir(file_path)
        print(pic_list)
        #achieve rangeIndex
        k = 1
        for i in pic_list:
            k -= 1
            pic_path = file_path + '/' + i
            
            # print(pic_path)

            if k <= 0:
                self.total += 1
                self.pic_path_list.append((pic_path))
                
        # print(self.pic_path_list)

    # 用于显示图片
    #

    def showimage(self):
        print("ok")
        jpg = QtGui.QPixmap(self.pic_path_list[self.index]).scaled(
            self.label.width(), self.label.height())
        self.label.setPixmap(jpg)
        self.setCheck()
        self.showPicInfo()


    def show_nextimage(self):
        self.index += 1
        self.index %= self.total
        jpg = QtGui.QPixmap(self.pic_path_list[self.index]).scaled(
            self.label.width(), self.label.height())
        self.label.setPixmap(jpg)
        self.setCheck()
        self.showPicInfo()

      

    def show_beforeimage(self):
        self.index -= 1
        self.index %= self.total
        jpg = QtGui.QPixmap(self.pic_path_list[self.index]).scaled(
            self.label.width(), self.label.height())
        self.label.setPixmap(jpg)
        self.setCheck()
        self.showPicInfo()


    def writelabel(self, label, btn_list, id):
        print(label)
        labstr = str(label)
        value = labstr[-1]
        j = labstr.find('_')
        index = labstr[:j]
        #执行判错提示
        if index == 'occasion':
            self.addOne_occ()

        elif index == 'quality':
            self.addOne_qua()
        elif index == 'box':
            self.addOne_box()

        print(index)
        now_txt_path = self.pic_path_list[self.index].replace("jpg", "json")
        now_txt_path = now_txt_path.replace("new_20210707", "result_0707")
        print(now_txt_path)
        with open(now_txt_path, 'rb') as f:
            json_data = json.load(f)
            print(json_data)
            json_data[index] = int(value)
            # self.labelstr = "occasion:" + json_data["occasion"] + "quality:" + json_data["quality"] + "box:" + json_data["box"]
            self.labelstr = "occasion: " + str(json_data["occasion"]) + "  quality: " + str(json_data["quality"]) + "  box: " + str(json_data["box"])
            self.lb1.setText(self.labelstr)
            print(json_data)
            f.close()
            with open(now_txt_path, 'w') as f:
		            json.dump(json_data,f)
            f.close()
        if self.index == len(self.pic_path_list)-1:
            sys.exit()
        # 触发按钮颜色变化
        for b_Button_id in range(len(btn_list)):
            if b_Button_id == id:
                btn_list[b_Button_id].setStyleSheet(
                    'background-color: #7FFFAA')
            else:
                btn_list[b_Button_id].setStyleSheet(
                    'background-color: #FFFFFF')

    def jumpTo(self):
        value, ok = QInputDialog.getInt(self, 'JUMP',
            'The picture you want to jump:')
        if value >= 0 and value < self.total and ok:
            self.index = value
            self.showimage()
    
    #occasion错误记录
    def addOne_occ(self):
        self.check_occ +=1
        self.checkstr_occ = "occ: {0} 当前进度错误率为: {1:.2f} %".format(self.check_occ,self.check_occ / (self.index+1))
        self.lb3.setText(self.checkstr_occ)
    
    def minusOne_occ(self):
        self.check_occ -= 1
        self.checkstr_occ = "occ: {0} 当前进度错误率为: {1:.2f} %".format(self.check_occ,self.check_occ / (self.index+1))
        self.lb3.setText(self.checkstr_occ)

    #quality错误记录
    def addOne_qua(self):
        self.check_qua +=1
        self.checkstr_qua = "qua: {0} 当前进度错误率为: {1:.2f} %".format(self.check_qua,self.check_qua / (self.index+1))
        self.lb4.setText(self.checkstr_qua)
    
    def minusOne_qua(self):
        self.check_qua -= 1
        self.checkstr_qua = "qua: {0} 当前进度错误率为: {1:.2f} %".format(self.check_qua,self.check_qua / (self.index+1))
        self.lb4.setText(self.checkstr_qua)

    #box错误记录
    def addOne_box(self):
        self.check_box +=1
        self.checkstr_box = "box: {0} 当前进度错误率为: {1:.2f} %".format(self.check_box,self.check_box / (self.index+1))
        self.lb5.setText(self.checkstr_box)
    
    def minusOne_box(self):
        self.check_box -= 1
        self.checkstr_box = "box: {0} 当前进度错误率为: {1:.2f} %".format(self.check_box,self.check_box / (self.index+1))
        self.lb5.setText(self.checkstr_box)

    def setCheck(self):
        self.checkstr_occ = "occ: {0} 当前进度错误率为: {1:.2f} %".format(self.check_occ,self.check_occ / (self.index+1))
        self.checkstr_qua = "qua: {0} 当前进度错误率为: {1:.2f} %".format(self.check_qua,self.check_qua / (self.index+1))
        self.checkstr_box = "box: {0} 当前进度错误率为: {1:.2f} %".format(self.check_box,self.check_box / (self.index+1))
        self.lb3.setText(self.checkstr_occ)
        self.lb4.setText(self.checkstr_qua)
        self.lb5.setText(self.checkstr_box)

    def showPicInfo(self):
        now_txt_path = self.pic_path_list[self.index].replace("jpg", "json")
        now_txt_path = now_txt_path.replace("new_20210707", "result_0707")
        with open(now_txt_path, 'rb') as f:
            json_data = json.load(f)
            # self.labelstr = "occasion:" + json_data["occasion"] + "quality:" + json_data["quality"] + "box:" + json_data["box"]
            self.labelstr = "occasion: " + str(json_data["occasion"]) + "  quality: " + str(json_data["quality"]) + "  box: " + str(json_data["box"])
            self.lb1.setText(self.labelstr)
            f.close()
        
        self.indexstr = "当前进度{0}/{1} RISE!".format(self.index,self.total)
        self.lb2.setText(self.indexstr)
    def setchecks(self):
        value, ok = QInputDialog.getInt(self, 'Occassion_mistake',
            'Input the number of occassion mistakes:')
        if ok :
            self.check_occ = value
        
        value, ok = QInputDialog.getInt(self, 'Quality_mistake',
            'Input the number of quality mistakes:')
        if ok :
            self.check_qua = value

        value, ok = QInputDialog.getInt(self, 'Box_mistake',
            'Input the number of box mistakes:')
        if ok :
            self.check_box = value
        self.showimage()
        

    


if __name__ == "__main__":
    list = ["occasion_0", "occasion_1", "occasion_2","quality_0", "quality_1", "quality_2","box_0","box_1", "box_2"]
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Windows"))
    my = picture(list)
    my.show()
    sys.exit(app.exec_())
