import sys
from PyQt4 import QtGui, QtCore
import mneEEGlab

class Window(QtGui.QMainWindow):
    
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("ERPy2.0 Test 2")
        self.setWindowIcon(QtGui.QIcon("palm_tree.png"))
        
        #Initialize empty file
        self.fname = ''
        
        #File Menu Actions
        exitAction = QtGui.QAction("&Exit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip('Exit ERPy')
        exitAction.triggered.connect(self.close_application)
        
        #Edit Menu Actions
        prefsAction = QtGui.QAction('&Preferences', self)
        prefsAction.setShortcut('Ctrl+P')
        prefsAction.setStatusTip('Not Yet Functional')
        prefsAction.triggered.connect(self.not_implemented)
        
        #Editor
        openEditor = QtGui.QAction('&Editor', self)
        openEditor.setShortcut('Ctrl+E')
        openEditor.setStatusTip('Open Editor')
        openEditor.triggered.connect(self.editor)

        #Open File
        openFile = QtGui.QAction('&Open File', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open File')
        openFile.triggered.connect(self.file_open) 
        
        #Load File
        loadFile = QtGui.QAction('&Load File', self)
        loadFile.setShortcut('Ctrl+L')
        loadFile.setStatusTip('Load File')
        loadFile.triggered.connect(self.file_load)  
        
        #Save File
        saveFile = QtGui.QAction('&Save File', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.setStatusTip('Save File')
        saveFile.triggered.connect(self.file_save)         
        
        self.statusBar()
        
        mainMenu = self.menuBar()
        
        #File Menu Implementation
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(openFile)
        fileMenu.addAction(loadFile)
        fileMenu.addAction(saveFile)
        
        #Edit Menu Implementation
        editMenu = mainMenu.addMenu('&Edit')
        editMenu.addAction(prefsAction)
        editMenu.addAction(openEditor)
        
        self.home()
        
    def home(self):
        # Plot Button
        btn = QtGui.QPushButton("Plot", self)
        btn.clicked.connect(self.plot_data)
        btn.resize(btn.minimumSizeHint())
        btn.move(0,100)
        
        extractAction = QtGui.QAction(QtGui.QIcon('empty_magnifying_glass.png'), 'ExitERPy', self)
        extractAction.triggered.connect(self.close_application)
        self.toolBar = self.addToolBar("Extraction")
        self.toolBar.addAction(extractAction)
        
        #------------------------------Font Picker Widget-------------------------------------------
        fontChoice = QtGui.QAction('Font', self)
        fontChoice.triggered.connect(self.font_choice)
        #self.toolBar = self.addToolBar("Font")
        self.toolBar.addAction(fontChoice)
        
        #------------------------------Color Picker Widget------------------------------------------
        color = QtGui.QColor(0, 0, 0)
        
        fontColor = QtGui.QAction('Font bg Color', self)
        fontColor.triggered.connect(self.color_picker)
        
        self.toolBar.addAction(fontColor)
        
        
        #------------------------------Check Box Example-------------------------------------------- 
        # can use checkBox.toggle() to have it intially toggeled
        checkBox = QtGui.QCheckBox('Enlarge Window', self)
        checkBox.move(300, 25)
        checkBox.stateChanged.connect(self.enlarge_window)
        
        #------------------------------Progress Bar Example------------------------------------------
        self.progress = QtGui.QProgressBar(self)
        self.progress.setGeometry(200, 80, 250, 20)
        
        self.btn = QtGui.QPushButton('Download', self)
        self.btn.move(200, 120)
        self.btn.clicked.connect(self.download)
        
        #------------------Combo Box/Drop Down Menu Example------------------------------
        print(self.style().objectName())
        self.styleChoice = QtGui.QLabel('Windows', self)
        
        comboBox = QtGui.QComboBox(self)
        comboBox.addItem('motif')
        comboBox.addItem('Windows')
        comboBox.addItem('cde')
        comboBox.addItem('Plastique')
        comboBox.addItem('Cleanlooks')
        comboBox.addItem('windowsvista')
        
        comboBox.move(50, 250)
        self.styleChoice.move(50, 150)
        comboBox.activated[str].connect(self.style_choice)
        
        #-----------------------Calendar Widget--------------------------------------
        cal = QtGui.QCalendarWidget(self)
        cal.move(500,200)
        cal.resize(200, 200)
        
        #Show Home Window
        self.show()
        
    def color_picker(self):
        color = QtGui.QColorDialog.getColor()
        self.styleChoice.setStyleSheet('QWidget { background-color: %s}' % color.name())
        
    def editor(self):
        self.textEdit = QtGui.QTextEdit()
        self.setCentralWidget(self.textEdit)
        
    def file_open(self):
        name = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
        file = open(name,'r')
        
        self.editor()
        
        with file:
            text = file.read()
            self.textEdit.setText(text)
        
    def file_load(self):
        name = QtGui.QFileDialog.getOpenFileName(self, 'Load File')
        file = open(name, 'r')
        
        self.fname = file
        
    def file_save(self):
        name = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        file = open(name, 'w')
        text = self.textEdit.toPlainText()
        file.write(text)
        file.close()
        
    def font_choice(self):
        font, valid = QtGui.QFontDialog.getFont()
        if valid:
            self.styleChoice.setFont(font)
        
    def style_choice(self, text):
        self.styleChoice.setText(text)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(text))
        
    def download(self):
        self.completed = 0
        while self.completed < 100:
            self.completed += 0.0001
            self.progress.setValue(self.completed)
        
    def enlarge_window(self, state):
        if state == QtCore.Qt.Checked:
            self.setGeometry(50, 50, 1000, 600)
        else:
            self.setGeometry(50, 50, 500, 300)
    
    def close_application(self):
        choice = QtGui.QMessageBox.question(self, 'Exit', "Exit Erpy?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            print('Exiting ERPy')
            sys.exit()
        else:
            pass
        
    def not_implemented(self):
        print("This functionality has not yet been implemented")
        
    def plot_data(self):
        mneEEGlab.plot_data(self.fname)

def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())
    
run()
             