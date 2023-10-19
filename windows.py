from PyQt5 import QtWidgets
from PyQt5 import QtGui , QtCore
from PyQt5.QtWidgets import *
from image_capture import ImageCapture
from googletrans import Translator
from PyQt5.QtGui import *

path = ""


try:
    from PIL import Image
except ImportError:
    import image_capture
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


class mainWindow:
    def __init__(self) -> None:
        super().__init__()
        self.window3 = QtWidgets.QMainWindow()
        self.init_ui()
        
    #Initialize Window Components
    def init_ui(self) -> None:
        self.__stylingWindowOne()
        transl = QtWidgets.QPushButton("Text Translator", self.window3)
        transl.clicked[bool].connect(self.trans)
        transl.setGeometry(50, 420, 180, 40)
        transl.setStyleSheet("background-color: #3700B3 ; font : 12px ;font-weight: bold ; color : #fff")
        img_transl = QPushButton("Image Translator", self.window3)
        img_transl.clicked[bool].connect(self.imag_trans)
        img_transl.setGeometry(50, 370, 180, 40)
        img_transl.setStyleSheet("background-color:#3700B3 ; font : 12px;font-weight: bold ; color : #fff")
        
        self.window3.show()

     
    #Styling Window Components
    def __stylingWindowOne(self):
        self.window3.setWindowIcon(QtGui.QIcon("home.png"))
        self.window3.setWindowTitle("Picto Translate" )
        self.window3.setGeometry(400, 100, 300, 500)  # Samaa
        self.window3.setStyleSheet("background-color:#d6d2d2 ")

        welcome_label = QLabel("Welcome to Picto Translate.\n"
                               "Your Translator App.", self.window3)
        welcome_label.setFont(QtGui.QFont("Times", 15, QtGui.QFont.Bold))
        welcome_label.setFixedWidth(300)
        welcome_label.setAlignment(QtCore.Qt.AlignLeft)
        welcome_label.setWordWrap(True)
        welcome_label.setGeometry(20, 60, 140, 140)
        logo_label = QtWidgets.QLabel(self.window3)
        logo_label.setGeometry(30, 170, 400, 100)
        logo = QtGui.QPixmap('logo.jpg')
        logo2 = logo.scaled(250, 70)
        logo_label.setPixmap(logo2)
        #self.resize(logo.width(), logo.height())
    
    #Load Image Translator Window
    def imag_trans(self):
        self.window = TranslatorGUI()
        self.window3.hide()

    #Load Text Translator Window
    def trans(self):
        self.window1 = text_trans()
        self.window3.hide()
        
        

class TranslatorGUI (QWidget):
    """Subclass of QWidget that serves as the main window and interface for the application.
    """
   
    def __init__(self) -> None:

        super().__init__()
      
        self.window = QtWidgets.QMainWindow()
        self.init_ui()
        self.imageCaptureDelegate = ImageCapture() #call image capture class

    #Initialize Window Components
    def init_ui(self) -> None:
        self.__stylingWindowOne()
        
        take_pic_btn = QtWidgets.QPushButton("Capture Image", self.window)
        take_pic_btn.clicked[bool].connect(self.__take_picture)
        take_pic_btn.setGeometry(50,370,180,40)
        take_pic_btn.setStyleSheet("background-color: #3700B3 ; font : 12px ; font-weight: bold ; color : #fff ")
        slct_img_btn = QPushButton("Select existing Image", self.window)
        slct_img_btn.clicked[bool].connect(self.__select_existing_image)
        slct_img_btn.setGeometry(50,420,180,40)
        slct_img_btn.setStyleSheet("background-color:#3700B3 ; font : 12px; font-weight: bold ; color : #fff")

        self.window.show() #showing window

    #Styling Window Components
    def __stylingWindowOne (self):
        self.window.setWindowIcon(QtGui.QIcon("home.png"))
        self.window.setWindowTitle("Picto Translate")
        self.window.setGeometry(400, 100, 300, 500)  # Samaa
        self.window.setStyleSheet("background-color:#d6d2d2")

        welcome_label = QLabel("Select the Image you want to translate" , self.window)
        welcome_label.setFont(QtGui.QFont("Times", 15, QtGui.QFont.Bold))
        welcome_label.setFixedWidth(300)
        welcome_label.setAlignment(QtCore.Qt.AlignLeft)
        welcome_label.setWordWrap(True)
        welcome_label.setGeometry(20,60,140,140)
        logo_label = QtWidgets.QLabel(self.window)
        logo_label.setGeometry(30, 170, 400, 100)
        logo = QtGui.QPixmap('logo.jpg')
        logo2 =logo.scaled(250,70)
        logo_label.setPixmap(logo2)
        self.resize(logo.width(),logo.height())

    #Launches image capture window, allows user to take image, then loads it.
    def __take_picture(self) -> None:
        image_file_name = self.imageCaptureDelegate.capture_image()
        global path
        path = image_file_name
        self.ImageWindow()

    #Launches file dialog box, allows user to select an existing image, then loads it.
    def __select_existing_image(self) -> None: 
        file_dialog = QFileDialog()
        image_file_name  = file_dialog.getOpenFileName()
        global path
        path = image_file_name[0]
        self.ImageWindow()
        
    #Creating new Window
    def ImageWindow(self):
        self.window1 = ImageWindow()
        self.window.hide()
        

class ImageWindow(QWidget):

    #Initializing Window Components
    def __init__(self):
        super().__init__()

        self.window1 = QtWidgets.QMainWindow()
        self.window1.setWindowTitle("Image")
        self.window1.setWindowIcon(QtGui.QIcon("image.png"))
        self.window1.setGeometry(400, 100, 300, 500) 
        self.window1.setStyleSheet("background-color:#d6d2d2")

        global path
        global src_lang
        global target_lang
        img = QtWidgets.QLabel(self.window1)
        img.setGeometry(15, -125, 500, 700)
        logo = QtGui.QPixmap(path)
        logo2 = logo.scaled(270, 400)
        img.setPixmap(logo2)
        self.resize(logo.width(), logo.height())

        translate_btn = QPushButton("Extract && Translate!",self.window1)
        translate_btn.clicked.connect(self.openSecondDialog)
        translate_btn.setGeometry(20, 450, 120, 40)
        translate_btn.setStyleSheet("background-color:#3700B3 ; font : 12px ; color : #fff ")
        back_btn = QPushButton(" Back" , self.window1)
        back_btn.clicked.connect(self.goBack)
        back_btn.setGeometry(155, 450, 120, 40)
        back_btn.setStyleSheet("background-color: #3700B3 ; font : 16px ; color : #fff")
        self.window1.show()
    
    #Load Main Window
    def goBack(self):
        self.window = mainWindow()
        self.window1.hide()
        
    #Load Language Dialoge
    def openSecondDialog(self):
        global languages
        languages = QDialog()
        languages.setGeometry(450, 200, 200, 200)
        languages.setWindowTitle("Languages")
        languages.setWindowIcon(QtGui.QIcon("translate.png"))
        languages.setModal(True)

        global listoflang
        listoflang =[' Select Language...', 'Afrikaans', 'Irish', 'Albanian', 'Italian', 'Arabic', 'Japanese', 'Azerbaijani',
             'Kannada', 'Basque', 'Korean', 'Bengali', 'Latin', 'Belarusian', 'Latvian',
             'Bulgarian', 'Lithuanian', 'Catalan', 'Macedonian', 'Chinese Simplified', 'Malay',
             'Chinese Traditional', 'Maltese', 'Croatian', 'Norwegian', 'Czech', 'Persian',
             'Danish', 'Polish', 'Dutch', 'Portuguese', 'English', 'Romanian', 'Esperanto',
             'Russian', 'Estonian', 'Serbian', 'Filipino', 'Slovak', 'Finnish', 'Slovenian',
             'French', 'Spanish', 'Galician', 'Swahili', 'Georgian', 'Swedish', 'German',
             'Tamil', 'Greek', 'Telugu', 'Gujarati', 'Thai', 'Haitian Creole', 'Turkish',
             'Hebrew', 'Ukrainian', 'Hindi', 'Urdu', 'Hungarian', 'Vietnamese', 'Icelandic',
             'Welsh', 'Indonesian', 'Yiddish']
        listoflang.sort()

        src__lang = QLabel("Source Language : ", languages)
        src__lang.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        src__lang.setFixedWidth(200)
        src__lang.setAlignment(QtCore.Qt.AlignLeft)
        src__lang.setWordWrap(True)
        src__lang.move(10, 20)

        global select_src_language_box
        select_src_language_box = QComboBox(languages)
        select_src_language_box.move(10, 50)
        select_src_language_box.setFixedWidth(150)
        select_src_language_box.setFont(QtGui.QFont("Times", 12))
        select_src_language_box.addItems(listoflang)
        select_src_language_box.setEditable(True)
        select_src_language_box.setInsertPolicy(QComboBox.NoInsert)


        target__lang = QLabel("Target Language : ", languages)
        target__lang.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        target__lang.setFixedWidth(200)
        target__lang.setAlignment(QtCore.Qt.AlignLeft)
        target__lang.setWordWrap(True)
        target__lang.move(10, 90)

        global select_target_language_box
        select_target_language_box = QComboBox(languages)
        select_target_language_box.move(10, 120)
        select_target_language_box.setFixedWidth(150)
        select_target_language_box.setFont(QtGui.QFont("Times", 12))
        select_target_language_box.addItems(listoflang)
        select_target_language_box.setEditable(True)
        select_target_language_box.setInsertPolicy(QComboBox.NoInsert)


        select_src_language_box.currentIndexChanged.connect(
            lambda x: self.test1(select_src_language_box.currentText()))
        select_target_language_box.currentIndexChanged.connect(
            lambda x: self.test2(select_target_language_box.currentText()))


        ok = QPushButton("OK" , languages)
        ok.move(130,160)
        ok.setFixedSize(50,30)
        ok.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        #ok.clicked.connect(languages.close)
        ok.clicked.connect(self.translate_)

        QWidget.setFocus(ok)

        languages.exec()

    #Setting Source Language
    def test1(self, src):
        global src_lang
        src_lang = src

    #Setting Target Language
    def test2(self, target):
        global target_lang
        target_lang = target
        
    #Encoding Source and Target Languages
    def translate_(self):
        global target_lang
        global src_lang
        
        #Error Handling: Missing Source and Traget Languages
        if select_src_language_box.currentIndex() == 0 and select_target_language_box.currentIndex() == 0:
            src_lang = "English"
            target_lang = "English"
            error = QDialog()
            error.setWindowTitle("Error")
            error.setGeometry(450, 200, 200, 200)
            widget1 = QLabel("Both Language is not specified.\n\n Your default language is English.", error)
            widget1.setWordWrap(True)
            widget1.setFixedWidth(180)
            widget1.move(10, 30)
            widget1.setFont(QtGui.QFont("Times", 11, QtGui.QFont.Bold))

            widget2 = QPushButton("OK", error)
            widget2.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
            widget2.clicked.connect(error.close)
            widget2.clicked.connect(self.transition)
            widget2.move(20, 150)
            widget2.setFixedSize(70, 40)
            widget2.clicked.connect(languages.close)

            widget3 = QPushButton("Edit", error)
            widget3.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
            widget3.move(100, 150)
            widget3.setFixedSize(70, 40)
            widget3.clicked.connect(error.close)
            error.exec()
            
        #Error Handling: Missing Source Language
        elif select_src_language_box.currentIndex() == 0:
            src_lang = "English"
            error_src = QDialog()
            error_src.setWindowTitle("Error")
            error_src.setGeometry(450, 200, 200, 200)
            widget1 = QLabel("Source Language is not specified.\n\n Your default language is English.", error_src)
            widget1.setWordWrap(True)
            widget1.setFixedWidth(180)
            widget1.move(10, 30)
            widget1.setFont(QtGui.QFont("Times", 11, QtGui.QFont.Bold))

            widget2 = QPushButton("OK", error_src)
            widget2.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
            widget2.clicked.connect(error_src.close)
            widget2.clicked.connect(self.transition)
            widget2.move(20, 150)
            widget2.setFixedSize(70,40)
            widget2.clicked.connect(languages.close)

            widget3 = QPushButton("Edit", error_src)
            widget3.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
            widget3.move(100, 150)
            widget3.setFixedSize(70,40)
            widget3.clicked.connect(error_src.close)
            error_src.exec()
            
        #Error Handling: Missing Traget Language
        elif select_target_language_box.currentIndex() == 0:
            target_lang="English"
            error_target = QDialog()
            error_target.setWindowTitle("Error")
            error_target.setGeometry(450, 200, 200, 200)
            widget1 = QLabel("Target Language is not specified.\n\n Your default language is English.", error_target)
            widget1.setWordWrap(True)
            widget1.setFixedWidth(180)
            widget1.move(10, 30)
            widget1.setFont(QtGui.QFont("Times", 11, QtGui.QFont.Bold))

            widget2 = QPushButton("OK", error_target)
            widget2.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
            widget2.clicked.connect(error_target.close)
            widget2.clicked.connect(self.transition)
            widget2.move(20, 150)
            widget2.setFixedSize(70, 40)
            widget2.clicked.connect(languages.close)

            widget3 = QPushButton("Edit", error_target)
            widget3.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
            widget3.move(100, 150)
            widget3.setFixedSize(70, 40)
            widget3.clicked.connect(error_target.close)
            error_target.exec()

        else:
            languages.close()
            self.transition()

    #Load Translation Window
    def transition (self):
        self.window2 = TranslatedWindow()
        self.window1.hide()
        
        
class TranslatedWindow(QWidget):
    
    #Error Handling no text Recogonised from OCR
    def error(self):
        mydialog = QDialog()
        mydialog.setWindowTitle("Error")
        mydialog.setGeometry(450, 200, 200, 200)
        widget1 = QLabel("No Text Recogonised...", mydialog)
        widget2 = QPushButton("Try Again", mydialog) #to input another image
        widget1.move(40, 80)
        widget1.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        widget2.move(110, 160)
        widget2.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        widget2.clicked.connect(mydialog.close)
        widget2.clicked.connect(self.goBack)

        mydialog.exec()

    #Initializing Window Components
    def __init__(self):
        super().__init__()

        self.window2 = QtWidgets.QMainWindow()
        self.window2.setWindowTitle("Translator")
        self.window2.setWindowIcon(QtGui.QIcon("translate.png"))
        self.window2.setGeometry(400, 100, 300, 500)  # Samaa
        self.window2.setStyleSheet("background-color:#d6d2d2")

        global trans_text
        
        #Translation Languages Encoding
        trans_language_codes = {'Afrikaans': 'af', 'Irish': 'ga', 'Albanian': 'sq', 'Italian': 'it', 'Arabic': 'ar',
                          'Japanese': 'ja', 'Azerbaijani': 'az',
                          'Kannada': 'kn', 'Basque': 'eu', 'Korean': 'ko', 'Bengali': 'bn', 'Latin': 'la',
                          'Belarusian': 'be', 'Latvian': 'lv',
                          'Bulgarian': 'bg', 'Lithuanian': 'lt', 'Catalan': 'ca', 'Macedonian': 'mk',
                          'Chinese Simplified': 'zh-CN', 'Malay': 'ms',
                          'Chinese Traditional': 'zh-TW', 'Maltese': 'mt', 'Croatian': 'hr', 'Norwegian': 'no',
                          'Czech': 'cs', 'Persian': 'fa',
                          'Danish': 'da', 'Polish': 'pl', 'Dutch': 'nl', 'Portuguese': 'pt', 'English': 'en',
                          'Romanian': 'ro', 'Esperanto': 'eo',
                          'Russian': 'ru', 'Estonian': 'et', 'Serbian': 'sr', 'Filipino': 'tl', 'Slovak': 'sk',
                          'Finnish': 'fi', 'Slovenian': 'sl',
                          'French': 'fr', 'Spanish': 'es', 'Galician': 'gl', 'Swahili': 'sw', 'Georgian': 'ka',
                          'Swedish': 'sv', 'German': 'de',
                          'Tamil': 'ta', 'Greek': 'el', 'Telugu': 'te', 'Gujarati': 'gu', 'Thai': 'th',
                          'Haitian Creole': 'ht', 'Turkish': 'tr',
                          'Hebrew': 'iw', 'Ukrainian': 'uk', 'Hindi': 'hi', 'Urdu': 'ur', 'Hungarian': 'hu',
                          'Vietnamese': 'vi', 'Icelandic': 'is',
                          'Welsh': 'y', 'Indonesian': 'id', 'Yiddish': 'yi'}
        
        #OCR Languages Encoding
        OCR_language_codes = {'Afrikaans': 'afr', 'Irish': 'gle', 'Albanian': 'sqi', 'Italian': 'ita', 'Arabic': "ara",
                                 'Japanese': 'jpn', 'Azerbaijani': 'aze',
                                 'Kannada': 'kan', 'Basque': 'eus', 'Korean': 'kor', 'Bengali': 'ben', 'Latin': 'lat',
                                 'Belarusian': 'bel', 'Latvian': 'lav',
                                 'Bulgarian': 'bul', 'Lithuanian': 'lit', 'Catalan': 'cat', 'Macedonian': 'mkd',
                                 'Chinese Simplified': 'chi_sim', 'Malay': 'msa',
                                 'Chinese Traditional': 'chi_tra', 'Maltese': 'mlt', 'Croatian': 'hrv', 'Norwegian': 'nor',
                                 'Czech': 'ces', 'Persian': 'fas',
                                 'Danish': 'dan', 'Polish': 'pol', 'Dutch': 'nld', 'Portuguese': 'por', 'English': 'eng',
                                 'Romanian': 'ron', 'Esperanto': 'epo',
                                 'Russian': 'rus', 'Estonian': 'est', 'Serbian': 'srp', 'Filipino': 'tgl', 'Slovak': 'slk',
                                 'Finnish': 'fin', 'Slovenian': 'slv',
                                 'French': 'fra', 'Spanish': 'spa', 'Galician': 'glg', 'Swahili': 'swa', 'Georgian': 'kat',
                                 'Swedish': 'swe', 'German': 'deu',
                                 'Tamil': 'tam', 'Greek': 'ell', 'Telugu': 'tel', 'Gujarati': 'guj', 'Thai': 'tha',
                                 'Haitian Creole': 'hat', 'Turkish': 'tur',
                                 'Hebrew': 'heb', 'Ukrainian': 'ukr', 'Hindi': 'hin', 'Urdu': 'urd', 'Hungarian': 'hun',
                                 'Vietnamese': 'vie', 'Icelandic': 'isl',
                                 'Welsh': 'cym', 'Indonesian': 'ind', 'Yiddish': 'yid'}



        src_lang_OCR = OCR_language_codes[src_lang]
        global detected_text
        detected_text = self.ocr_core(path, src_lang_OCR)
        
        #Error Handling: No text Detected
        if detected_text == "":
            self.error()
        else:
            src_lang_ = trans_language_codes[src_lang]
            target_lang_ = trans_language_codes[target_lang]
            trans_text = self.translate(detected_text, src_lang_, target_lang_)

            widget1 = QLabel("Extracted \nText : ", self.window2)
            widget1.setFont(QtGui.QFont("Times", 14, QtGui.QFont.Bold))

            widget1.setFixedSize(200,60)
            widget1.setAlignment(QtCore.Qt.AlignLeft)
            widget1.setWordWrap(True)
            widget1.move(10, 30)

            self.textbox =QPlainTextEdit(self.window2)
            self.textbox.move(15, 90)
            self.textbox.setFixedSize(270, 130)
            self.textbox.setFont(QtGui.QFont("Times", 14 ))
            self.textbox.setStyleSheet("background-color:#fff")
            self.textbox.appendPlainText(detected_text)

            widget2 = QLabel("Translated \nText : ", self.window2)
            widget2.setFont(QtGui.QFont("Times", 14, QtGui.QFont.Bold))

            widget2.setFixedSize(200,60)
            widget2.setAlignment(QtCore.Qt.AlignLeft)
            widget2.setWordWrap(True)
            widget2.move(15,240)


            self.textbox = QPlainTextEdit(self.window2)
            self.textbox.move(15, 300)
            self.textbox.setFixedSize(270, 130)
            self.textbox.setFont(QtGui.QFont("Times", 14))
            self.textbox.setStyleSheet("background-color:#fff")
            self.textbox.appendPlainText(trans_text)

            back_btn = QPushButton("Done", self.window2)
            back_btn.clicked.connect(self.goBack)
            back_btn.setGeometry(155, 450, 120, 40)
            back_btn.setStyleSheet("background-color: #3700B3; font : 14px;font-weight: bold ; color : #fff")
         

            self.window2.show()

    def goBack(self):
        self.window = mainWindow()
        self.window2.hide()

    def ocr_core(self, filename,src_lang_OCR):
        """
        This function will handle the core OCR processing of images.
        """
        config = ("-l " + src_lang_OCR)
        text = pytesseract.image_to_string(Image.open(filename),config=config)  # We'll use Pillow's Image class to open the image and pytesseract to detect the string in the image
        return text

    #Translation Function using GoogleTrans
    def translate(self, text, source, destination):
        translator = Translator()
        trans_text = translator.translate(text, src=source, dest=destination).text
        return trans_text
    
    
class text_trans():

    #Initializing Window Components
    def __init__(self):
        super().__init__()

        self.window4 = QtWidgets.QMainWindow()
        self.window4.setWindowTitle("Translator")
        self.window4.setWindowIcon(QtGui.QIcon("translate.png"))
        self.window4.setGeometry(400, 100, 300, 500)  # Samaa
        self.window4.setStyleSheet("background-color:#d6d2d2")

        widget1 = QLabel("Text : ", self.window4)
        widget1.setFont(QtGui.QFont("Times", 14, QtGui.QFont.Bold) )
        widget1.setFixedWidth(200)
        widget1.setAlignment(QtCore.Qt.AlignLeft)
        widget1.setWordWrap(True)
        widget1.move(10, 20)

        global Tbox
        Tbox =QPlainTextEdit(self.window4)
        Tbox.move(15, 60)
        Tbox.setFixedSize(270, 130)
        Tbox.setFont(QtGui.QFont("Times", 14 ))
        Tbox.setStyleSheet("background-color:#fff")
        Tbox.setPlaceholderText("Type your text here...")
        widget2 = QLabel("Translated \nText : ", self.window4)
        widget2.setFont(QtGui.QFont("Times", 14, QtGui.QFont.Bold))

        widget2.setFixedSize(200,60)
        widget2.setAlignment(QtCore.Qt.AlignLeft)
        widget2.setWordWrap(True)
        widget2.move(15,240)

        global textbox1
        textbox1 = QPlainTextEdit(self.window4)
        textbox1.move(15, 300)
        textbox1.setFixedSize(270, 130)
        textbox1.setFont(QtGui.QFont("Times", 14))
        textbox1.setStyleSheet("background-color:#fff")
        textbox1.setReadOnly(True)
        textbox1.setPlaceholderText("Translated Text...")
       

        back_btn = QPushButton("Done", self.window4)
        back_btn.clicked.connect(self.goBack)
        back_btn.setGeometry(155, 450, 120, 40)
        back_btn.setStyleSheet("background-color: #3700B3 ; color : #fff; font : 14px; font-weight: bold ")
        

        trans_btn = QPushButton("Translate!", self.window4)
        trans_btn.clicked.connect(self.translate_text)
        trans_btn.setGeometry(20, 450, 120, 40)
        trans_btn.setStyleSheet("background-color:#3700B3; font : 14px;font-weight: bold ; color : #fff")
        

        global languages2
        languages2 = QDialog()
        languages2.setGeometry(450, 200, 200, 200)
        languages2.setWindowTitle("Languages")
        languages2.setWindowIcon(QtGui.QIcon("translate.png"))
        languages2.setModal(True)

        global listoflang2
        listoflang2= [' Select Language...', 'Afrikaans', 'Irish', 'Albanian', 'Italian', 'Arabic', 'Japanese',
                      'Azerbaijani',
                      'Kannada', 'Basque', 'Korean', 'Bengali', 'Latin', 'Belarusian', 'Latvian',
                      'Bulgarian', 'Lithuanian', 'Catalan', 'Macedonian', 'Chinese Simplified', 'Malay',
                      'Chinese Traditional', 'Maltese', 'Croatian', 'Norwegian', 'Czech', 'Persian',
                      'Danish', 'Polish', 'Dutch', 'Portuguese', 'English', 'Romanian', 'Esperanto',
                      'Russian', 'Estonian', 'Serbian', 'Filipino', 'Slovak', 'Finnish', 'Slovenian',
                      'French', 'Spanish', 'Galician', 'Swahili', 'Georgian', 'Swedish', 'German',
                      'Tamil', 'Greek', 'Telugu', 'Gujarati', 'Thai', 'Haitian Creole', 'Turkish',
                      'Hebrew', 'Ukrainian', 'Hindi', 'Urdu', 'Hungarian', 'Vietnamese', 'Icelandic',
                      'Welsh', 'Indonesian', 'Yiddish']
        listoflang2.sort()

        src__lang2 = QLabel("Source Language : ", languages2)
        src__lang2.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        src__lang2.setFixedWidth(200)
        src__lang2.setAlignment(QtCore.Qt.AlignLeft)
        src__lang2.setWordWrap(True)
        src__lang2.move(10, 20)

        global select_src_language_box2
        select_src_language_box2 = QComboBox(languages2)
        select_src_language_box2.move(10, 50)
        select_src_language_box2.setFixedWidth(150)
        select_src_language_box2.setFont(QtGui.QFont("Times", 12))
        select_src_language_box2.addItems(listoflang2)
        select_src_language_box2.setEditable(True)
        select_src_language_box2.setInsertPolicy(QComboBox.NoInsert)

        target__lang2 = QLabel("Target Language : ", languages2)
        target__lang2.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        target__lang2.setFixedWidth(200)
        target__lang2.setAlignment(QtCore.Qt.AlignLeft)
        target__lang2.setWordWrap(True)
        target__lang2.move(10, 90)

        global select_target_language_box2
        select_target_language_box2 = QComboBox(languages2)
        select_target_language_box2.move(10, 120)
        select_target_language_box2.setFixedWidth(150)
        select_target_language_box2.setFont(QtGui.QFont("Times", 12))
        select_target_language_box2.addItems(listoflang2)
        select_target_language_box2.setEditable(True)
        select_target_language_box2.setInsertPolicy(QComboBox.NoInsert)

        select_src_language_box2.currentIndexChanged.connect(
            lambda x: self.test1(select_src_language_box2.currentText()))
        select_target_language_box2.currentIndexChanged.connect(
            lambda x: self.test2(select_target_language_box2.currentText()))

        ok = QPushButton("OK", languages2)
        ok.move(130, 160)
        ok.setFixedSize(50, 30)
        ok.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
        ok.clicked.connect(self.translate_)
        QWidget.setFocus(ok)
        self.window4.show()
        languages2.exec()

    #Load Main Window
    def goBack(self):
        self.window = mainWindow()
        self.window4.hide()

    #Setting Source Language
    def test1(self, src):
        global src_lang2
        src_lang2 = src
        
    #Setting Target Language
    def test2(self, target):
        global target_lang2
        target_lang2 = target

    def translate_(self):
        global target_lang2
        global src_lang2

        if select_src_language_box2.currentIndex() == 0 and select_target_language_box2.currentIndex() == 0:
            src_lang2 = "English"
            target_lang2 = "English"
            error = QDialog()
            error.setWindowTitle("Error")
            error.setGeometry(450, 200, 200, 200)
            widget1 = QLabel("Both Language is not specified.\n\n Your default language is English.", error)
            widget1.setWordWrap(True)
            widget1.setFixedWidth(180)
            widget1.move(10, 30)
            widget1.setFont(QtGui.QFont("Times", 11, QtGui.QFont.Bold))

            widget2 = QPushButton("OK", error)
            widget2.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
            widget2.clicked.connect(error.close)
            #widget2.clicked.connect(self.transition)
            widget2.move(20, 150)
            widget2.setFixedSize(70, 40)
            widget2.clicked.connect(languages2.close)

            widget3 = QPushButton("Edit", error)
            widget3.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
            widget3.move(100, 150)
            widget3.setFixedSize(70, 40)
            widget3.clicked.connect(error.close)
            error.exec()

        elif select_src_language_box2.currentIndex() == 0:
            src_lang2 = "English"
            error_src = QDialog()
            error_src.setWindowTitle("Error")
            error_src.setGeometry(450, 200, 200, 200)
            widget1 = QLabel("Source Language is not specified.\n\n Your default language is English.", error_src)
            widget1.setWordWrap(True)
            widget1.setFixedWidth(180)
            widget1.move(10, 30)
            widget1.setFont(QtGui.QFont("Times", 11, QtGui.QFont.Bold))

            widget2 = QPushButton("OK", error_src)
            widget2.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
            widget2.clicked.connect(error_src.close)
            #widget2.clicked.connect(self.transition)
            widget2.move(20, 150)
            widget2.setFixedSize(70,40)
            widget2.clicked.connect(languages2.close)

            widget3 = QPushButton("Edit", error_src)
            widget3.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
            widget3.move(100, 150)
            widget3.setFixedSize(70,40)
            widget3.clicked.connect(error_src.close)
            error_src.exec()

        elif select_target_language_box2.currentIndex() == 0:
            target_lang2="English"
            error_target = QDialog()
            error_target.setWindowTitle("Error")
            error_target.setGeometry(450, 200, 200, 200)
            widget1 = QLabel("Target Language is not specified.\n\n Your default language is English.", error_target)
            widget1.setWordWrap(True)
            widget1.setFixedWidth(180)
            widget1.move(10, 30)
            widget1.setFont(QtGui.QFont("Times", 11, QtGui.QFont.Bold))

            widget2 = QPushButton("OK", error_target)
            widget2.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
            widget2.clicked.connect(error_target.close)
            widget2.move(20, 150)
            widget2.setFixedSize(70, 40)
            widget2.clicked.connect(languages2.close)

            widget3 = QPushButton("Edit", error_target)
            widget3.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
            widget3.move(100, 150)
            widget3.setFixedSize(70, 40)
            widget3.clicked.connect(error_target.close)
            error_target.exec()

        else:
            languages2.close()

    def translate_text(self):

        if Tbox.toPlainText() == "":
            mydialog = QDialog()
            mydialog.setWindowTitle("Error")
            mydialog.setGeometry(450, 200, 200, 200)
            widget1 = QLabel("Please enter a text to be translated.", mydialog)
            widget1.setWordWrap(True)
            widget1.setFixedWidth(180)
            widget2 = QPushButton("Try Again", mydialog)
            widget1.move(10, 80)
            widget1.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
            widget2.move(110, 160)
            widget2.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
            widget2.clicked.connect(mydialog.close)
            
            mydialog.exec()

        else:
            global src_lang2
            global target_lang2
            self.translate(Tbox.toPlainText(),src_lang2,target_lang2)
            
      
    #Translation Function using GoogleTrans
    def translate(self, text, source, destination):
        translator = Translator()
        trans_text = translator.translate(text, src=source, dest=destination).text
        textbox1.appendPlainText(trans_text)
        
        
        