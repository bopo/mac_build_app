import os
import subprocess
from xml.dom.minidom import Document
from apps.win import Ui_MainWindow
from PyQt5.Qt import *
import cgitb
cgitb.enable(format='text')
__Author__ = '南城九叔'
__Version__ = '1.0.0'
__Email__ = '416572009@qq.com'
'''
MacOS下nuitka打包散件后，制作.app
Nuitka打包交流QQ群：365072404
'''


class MainWin(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWin, self).__init__()
        self.setupUi(self)
        self.init_signal()

    def set_ico(self):
        fname, _ = QFileDialog.getOpenFileName(self, '选择图标', '', '*.png;*.jpg')
        if fname:
            self.lineEdit.setText(fname)

    def set_app(self):
        fname, _ = QFileDialog.getOpenFileName(self, '选择主程序', '', '')
        if fname:
            self.lineEdit_5.setText(fname)

    def set_path(self, edit):
        fname = QFileDialog.getExistingDirectory(self, '选择文件夹', '')
        if fname:
            edit.setText(fname)

    def check_path(self):
        for edit in self.findChildren(QLineEdit):
            if not edit.text():
                self.textBrowser.setText('请填写完整信息！')
                return False
        return True

    def to_app(self):
        if self.pushButton.text() == '开始制作':
            if self.check_path():
                name = self.lineEdit_4.text()
                app = '/' + self.lineEdit_5.text()
                version = self.lineEdit_6.text()
                icns = self.lineEdit.text()
                in_path = self.lineEdit_2.text() + '/*'
                out_path = self.lineEdit_3.text()
                info = [name, app, version, icns, in_path, out_path]
                self.do = Work(info, tip=self.textBrowser.append, finished=self.pushButton.click)
                self.do.start()
                self.textBrowser.setText('开始制作')
                self.pushButton.setText('终止任务')
                app = app.split('/')[-1]
                self.filePath = out_path
                self.app = f'{out_path}/{app}.app'
                self.repaint()
        else:
            self.do.terminate()
            self.pushButton.setText('开始制作')
            self.repaint()

    def init_signal(self):
        self.pushButton.clicked.connect(self.to_app)
        self.pushButton_2.clicked.connect(self.set_ico)
        self.pushButton_3.clicked.connect(lambda: self.set_path(self.lineEdit_2))
        self.pushButton_4.clicked.connect(lambda: self.set_path(self.lineEdit_3))
        self.pushButton_5.clicked.connect(self.set_app)
        self.pushButton_6.clicked.connect(lambda: subprocess.call(["open", self.filePath]))
        self.pushButton_7.clicked.connect(lambda: subprocess.call(["open", self.app]))


class Work(QThread):
    tip = pyqtSignal(str)

    def __init__(self, info, *args, **kwargs):
        super(Work, self).__init__(*args, **kwargs)
        self.info = info

    def run(self):
        try:
            name, app, version, icns, in_path, out_path = self.info
            app = app.split('/')[-1]
            app_path = f'{out_path}/{app}.app'
            icns_temp = f'{out_path}/test.iconset'
            file_path = f'{app_path}/Contents/MacOS'
            icns_path = f'{app_path}/Contents/Resources'
            fm_path = f'{app_path}/Contents/Frameworks'
            if os.path.exists(app_path):
                delt = subprocess.Popen(f'rm -rf {app_path}', shell=True)
                delt.wait()
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            copy = subprocess.Popen(f'cp -r {in_path} {file_path}', shell=True)
            copy.wait()
            if not os.path.exists(icns_temp):
                os.makedirs(icns_temp)
            os.makedirs(fm_path)
            os.makedirs(icns_path)
            ml = f'''sips -z 16 16     {icns} --out {icns_temp}/icon_16x16.png
            sips -z 32 32     {icns} --out {icns_temp}/icon_16x16@2x.png
            sips -z 32 32     {icns} --out {icns_temp}/icon_32x32.png
            sips -z 64 64     {icns} --out {icns_temp}/icon_32x32@2x.png
            sips -z 128 128   {icns} --out {icns_temp}/icon_128x128.png
            sips -z 256 256   {icns} --out {icns_temp}/icon_128x128@2x.png
            sips -z 256 256   {icns} --out {icns_temp}/icon_256x256.png
            sips -z 512 512   {icns} --out {icns_temp}/icon_256x256@2x.png
            sips -z 512 512   {icns} --out {icns_temp}/icon_512x512.png
            sips -z 512 512   {icns} --out {icns_temp}/icon_512x512@2x.png'''
            pic = subprocess.Popen(ml, shell=True)
            pic.wait()
            ml = f'iconutil -c icns {icns_temp} -o {icns_path}/app.icns'
            icon = subprocess.Popen(ml, shell=True)
            icon.wait()
            doc = Document()
            plist = doc.createElement('plist')
            plist.setAttribute("version", "1.0")
            doc.appendChild(plist)
            dict = doc.createElement('dict')
            plist.appendChild(dict)
            names = ['CFBundleDisplayName', 'CFBundleExecutable', 'CFBundleIconFile', 'CFBundleIdentifier',
                     'CFBundleInfoDictionaryVersion', 'CFBundleName', 'CFBundlePackageType', 'CFBundleShortVersionString',
                     'NSHighResolutionCapable']
            value = [name, f'MacOS/{app}', 'app.icns', name, '6.0', name, 'APPL', version, 'ture']
            for i in range(len(names)):
                k1 = doc.createElement('key')
                k1.appendChild(doc.createTextNode(names[i]))
                dict.appendChild(k1)
                k1 = doc.createElement('string')
                k1.appendChild(doc.createTextNode(value[i]))
                dict.appendChild(k1)
            info_file = f'{app_path}/Contents/Info.plist'
            with open(info_file, 'w') as f:
                f.write(doc.toprettyxml(indent="  "))
            pkg_file = f'{app_path}/Contents/PkgInfo'
            with open(pkg_file, 'wb') as f:
                f.write(b'APPL????')
            delt = subprocess.Popen(f'rm -rf {icns_temp}', shell=True)
            delt.wait()
            self.tip.emit('制作完成')
        except Exception as e:
            self.tip.emit(f'发生错误：{e}')
