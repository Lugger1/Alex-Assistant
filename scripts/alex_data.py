from datetime import datetime

import pyttsx3
from pyttsx3.drivers import sapi5

from fuzzywuzzy import fuzz
import time

from scripts.modif_thread import thread_with_exception
from scripts.widgets import Label

class Alex:
    def __init__(self):
        self.name = 'Алекс'
        self.birth_date = datetime(2024, 4, 10, 18, 30, 0, 0)
        
        self.output = Label(None, 'Вывод: None')
        
        self.msg = ''
        
        self.engine = pyttsx3.init()
    
    def update_text(self, text)-> None:
        thread_with_exception(func=self._upd_text_thread, args=text, name='обновление текста').start()
    
    def _upd_text_thread(self, text):
        self.output.setText('Вывод: ')

        try:
            time_ = min(0.05, 0.03)
            print(time_)
            for a in text:
                time.sleep(time_)
                self.output.setText(self.output.text()+a)
        except TypeError as err:
            for a in str(err):
                time.sleep(0.2)
                self.output.setText(self.output.text()+a)
    
    def say(self, msg: str): # -> audio
        msg = msg.split('.')
        self.msg = msg[0]
        if len(self.msg) <= 150:
            try:
                self.msg += msg[1]
            except IndexError: pass
        
        self.initializate_voice()
        
        print(f'[{self.name}]говорю: {self.msg}')
        
        self.engine.say(self.msg)
        
        b = thread_with_exception(func=self.engine.runAndWait, name='возпроизведение').run()

    def initializate_voice(self) -> None:
        for i in self.engine.getProperty('voices'):
            if fuzz.partial_ratio('Pavel', i.name) == 100:
                self.engine.setProperty('voice', i.id)
                break
        else:
            raise WindowsError('Не был обнаружен TTS Microsoft Pavel')
        
        self.engine.setProperty('volume', 1)
        self.engine.setProperty('rate', 175)

from PyQt6.QtWidgets import QApplication            
alex_app = QApplication([])
alex = Alex()

