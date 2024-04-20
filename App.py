'''
Школьный проект "Голосовой ассистент Алекс"

Имя ассистента - Алекс

Презентация - Даниил Фёдоров(https://t.me/oaoaof)
Программный код - Владимир Шарапов(https://t.me/Lsxzvt)
'''

import speech_recognition
import sys
import time

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

TITLE = 'Alex Voice Assistant'
VERSION = '1.0.0'

class AlexApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(TITLE+' '+VERSION)
        self.setFixedSize(480, 515)
        # прослушивание аудио в потоке
        self.thread_listen = thread_with_exception(func=self.start_listen, name='прослушка')
        
        self.started_listen = False
        
        self.a1 = 1
        
        self.main()

    def main(self):
        self.central_widg = QWidget()
        
        Hor_Lt = QHBoxLayout(self.central_widg)

        self.title = Label(parent=self.central_widg, text=f'{TITLE}\nГолосовой Ассистент', font_size=18)
        self.title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.title.move(self.width()//2-self.title.width()//2, -50)
        
        self.listened = Label(parent=self.central_widg, text='Распознано: None', font_size=14)
        self.listened.resize(self.width()-10, 35)
        self.listened.move(self.width()//2-self.listened.width()//2, -50)
        
        self.scroll_widget = QScrollArea(self.central_widg)
        self.scroll_widget.setFixedSize(465, 225)
        
        self.output = alex.output
        self.output.setObjectName('in_scroll')
        self.output.setParent(self.central_widg)
        self.output.setFixedSize(440, 5000)
        self.output.resize(self.output.width()-20, self.output.height()+5000)
        self.output.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.output.setWordWrap(True)

        self.scroll_widget.setWidget(self.output)
        self.scroll_widget.move(-400, 175)
        self.output.resize(self.width()-10, 225)
        
        self.button_listen = QPushButton(self.central_widg)
        self.button_listen.setText('Слушать')
        self.button_listen.clicked.connect(self.start_listen)
        self.button_listen.move(-self.width(), 75)
        self.button_listen.resize(QSize(self.width()-10, 70))
        
        self.text = QLineEdit(self.central_widg)
        self.text.move(self.width()//2-self.text.width()//2, self.height()+20)
        
        self.button_read = QPushButton(self.central_widg)
        self.button_read.setText('Выполнить')
        self.button_read.move(self.width()//2-self.button_read.width()//2, self.height()+20)
        self.button_read.clicked.connect(self.alex_think)
        
        self.setCentralWidget(self.central_widg)
        self.timer_ = QTimer(self)
        self.timer_.timeout.connect(lambda:self.start_anim(0))
        self.timer_.start(250)

    def start_anim(self, step=0):
        speed_anim = 100
        if step == -1:
            self.timer_.timeout.connect(lambda: self.start_anim(0))
            self.timer_.setInterval(250)
        
        if step == 0:
            anim_title = QPropertyAnimation(self.title, b'pos', self)
            anim_title.setEndValue(QPoint(self.width()//2-self.title.width()//2, 10))
            anim_title.setDuration(speed_anim)
            anim_title.start()
            
            anim_listened = QPropertyAnimation(self.listened, b'pos', self)
            anim_listened.setEndValue(QPoint(self.width()//2-self.listened.width()//2, 140))
            anim_listened.setDuration(speed_anim)
            anim_listened.start()
            
            anim_scroll_w = QPropertyAnimation(self.scroll_widget, b'pos', self)
            anim_scroll_w.setEndValue(QPoint(self.width()//2-self.listened.width()//2, 170))
            anim_scroll_w.setDuration(speed_anim)
            anim_scroll_w.start()
            
            self.timer_.timeout.connect(lambda: self.start_anim(1))

        if step == 1:
            anim_btn_listen_0 = QPropertyAnimation(self.button_listen, b'pos', self)
            anim_btn_listen_0.setEndValue(QPoint(5, 75))
            anim_btn_listen_0.setDuration(speed_anim)
            anim_btn_listen_0.start()
            
            self.timer_.timeout.connect(lambda: self.start_anim(2))
        
        if step == 2:
            anim_text_inp_0 = QPropertyAnimation(self.text, b'pos', self)
            anim_text_inp_0.setEndValue(QPoint(5, 400))
            anim_text_inp_0.setDuration(speed_anim)
            anim_text_inp_0.start()
            
            anim_text_inp_1 = QPropertyAnimation(self.text, b'size', self)
            anim_text_inp_1.setEndValue(QSize(self.width()-10, 30))
            anim_text_inp_1.setDuration(speed_anim)
            anim_text_inp_1.start()
            
            self.timer_.timeout.connect(lambda: self.start_anim(3))
        
        if step == 3:
            anim_btn_read_0 = QPropertyAnimation(self.button_read, b'pos', self)
            anim_btn_read_0.setEndValue(QPoint(5, 435))
            anim_btn_read_0.setDuration(speed_anim)
            anim_btn_read_0.start()
            
            anim_btn_read_1 = QPropertyAnimation(self.button_read, b'size', self)
            anim_btn_read_1.setEndValue(QSize(self.width()-10, 75))
            anim_btn_read_1.setDuration(speed_anim)
            anim_btn_read_1.start()
            
            self.timer_.timeout.connect(lambda: self.start_anim(4))
        
        if step == 4:
            self.timer_.timeout.connect(lambda: self.start_anim(4))
            self.timer_.stop()

    def start_listen(self):
        voice_input = QThreadPool(self.central_widg)
        voice_input.setObjectName('QThreadPool')
        if not self.started_listen:
            print(f'поток \"{voice_input.objectName()}\" запущен')
            self.started_listen = True
            voice_input.start(self.record_and_recognize_audio)
        else:
            print(f'Уже идёт прослушка в потоке \"{voice_input.objectName()}\"!\nГоворите в микрофон.')
        
    def alex_think(self, returned=None):
        returned = self.text.text()
        thread = thread_with_exception(func=lambda: doing(returned), name='принятие запроса')
        
        if not thread.is_alive():
            thread.start()
        else:
            print('Поток уже запущен!')
        
    def record_and_recognize_audio(self):
        with microphone:
            recognized_data = ""

            # регулирование уровня окружающего шума
            recognizer.adjust_for_ambient_noise(microphone, duration=2)
            self.listened.setText(f'Распознано: ')

            try:
                print("Слушаем...")
                audio = recognizer.listen(microphone, 5, 5)

            except speech_recognition.WaitTimeoutError:
                # print("У вас некорректно настроен микрофон")
                # return
                pass

            # использование online-распознавания через Google 
            try:
                print("Распознавание...")
                recognized_data = recognizer.recognize_google(audio, language="ru").lower()

            except speech_recognition.UnknownValueError:
                print(f'Распознано: {recognized_data}')
                return

            # в случае проблем с доступом в Интернет происходит выброс ошибки
            except speech_recognition.RequestError:
                alex.say_msg("Простите, у вас нет подключения к интернету, или плохое соединение!")

            
            for i in recognized_data:
                self.listened.setText(self.listened.text()+i)
                time.sleep(0.05)
            
            thread = thread_with_exception(func=lambda: doing(recognized_data), name='принятие запроса')
        
            try:
                thread.join()
            except RuntimeError:
                thread.start()
            else:
                print('Поток уже запущен!')
            
            self.started_listen = False

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        alex_app.closeAllWindows()
        for i in list_threads: i.raise_exception()
        self.destroy(True, True)
        sys.exit(alex.say)

if __name__ == "__main__":
    from scripts.brain import doing
    from scripts.alex_data import alex, alex_app
    from scripts.widgets import Label
    from scripts.modif_thread import thread_with_exception, list_threads

    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    app = QApplication([])
    app.setStyle('fusion')
    a = AlexApp()
    a.show()
    with open('style.qss') as f:
        a.setStyleSheet(f.read())
    app.exec()
