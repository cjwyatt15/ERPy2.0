import sys
from PyQt4 import QtGui, QtCore
import mne
from mne import io, Epochs
from mne.preprocessing import ICA

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
        
        #Filter Dataset
        filterData = QtGui.QAction('&Filter Data', self)
        filterData.setStatusTip('Add Frequency Filter to current Dataset')
        filterData.triggered.connect(self.filter_menu)
        
        #Plot Dataset
        plotData = QtGui.QAction('&Plot Data', self)
        plotData.setStatusTip('Plot Currently Loaded Dataset')
        plotData.triggered.connect(self.plot_data)
        
        self.statusBar()
        
        mainMenu = self.menuBar()
        
        #File Menu Implementation
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(openFile)
        fileMenu.addAction(loadFile)
        fileMenu.addAction(saveFile)
        fileMenu.addAction(exitAction)
        
        #Edit Menu Implementation
        editMenu = mainMenu.addMenu('&Edit')
        editMenu.addAction(prefsAction)
        editMenu.addAction(openEditor)
        
        #Dataset Menu Implementation
        datasetMenu = mainMenu.addMenu('&Dataset')
        datasetMenu.addAction(plotData)
        datasetMenu.addAction(filterData)
        
        self.home()
        
    def home(self): 
        #-----------------------------Output log---------------------------------------------------
        self.logOutput = QtGui.QTextEdit(self)
        self.logOutput.setReadOnly(True)
        self.logOutput.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.logOutput.setGeometry(50, 200, 350, 100)
        
        logFont = self.logOutput.font()
        logFont.setFamily("Courier")
        logFont.setPointSize(10)
        
        self.logOutput.move(100, 25)
        
        #Show Home Window
        self.show()
        
    def plot_data(self):
        if self.fname == '':
            self.log_print('There is no file selected. Please select a file\n')
            print('There is no file selected. Please select a file')
        else:
            self.log_print('Plotting data...')
            raw = io.read_raw_eeglab(str(self.fname))  #109_raw.set
            raw.plot(block=True)
            
    def frequency_filter(self, fname, lfreq, hfreq):
        if fname == '':
            self.log_print('There is no file selected. Please select a file\n')
            print('There is no file selected. Please select a file')
        else:
            fname = io.read_raw_eeglab(str(fname))
            fname.load_data()
            fname.filter(lfreq, hfreq)
            fname.plot()
            self.log_print('Filter applied\n') 
            print('Filter applied')    
        
    def log_print(self, text):
        self.logOutput.moveCursor(QtGui.QTextCursor.End)
        self.logOutput.insertPlainText(text)
        sb = self.logOutput.verticalScrollBar()
        sb.setValue(sb.maximum())
        
    def filter_menu(self):
        #freqWindow = QDialog()
        #l_freqEdit = QLineEdit()
        freq_string,  ok = QtGui.QInputDialog.getText(self, 'InputDialog', 'Enter frequencies separated by a space (low high): ')
        if ok:
            freq_array = str(freq_string).split()  
            l_freq = float(freq_array[0])
            h_freq = float(freq_array[1])
            self.log_print('Applying filter...\n')
            self.frequency_filter(self.fname, l_freq, h_freq)
              
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
        #file = open(name, 'r')
        
        self.fname = name
        self.log_print(self.fname)
        self.log_print('\n')
        print(self.fname)
        
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
            self.log_print('Exiting ERPy')
            sys.exit()
        else:
            pass
        
    def not_implemented(self):
        print("This functionality has not yet been implemented")
        

def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())
    
run()
