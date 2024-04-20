# сравнивание строк
from fuzzywuzzy import fuzz
from fuzzywuzzy import process as fuzz_list
# управление временем
from datetime import datetime
# рандомизация
import random
# открыть ссылку в браузере
import webbrowser
from wikipedia.exceptions import DisambiguationError
import requests
# импорт написанных скриптов для использования взависимости от ввода
from scripts.alex_data import alex
from scripts.wikipedia_skearch import search, err
from scripts.weather import get_weather
from scripts.modif_thread import thread_with_exception
from scripts.timer_script import Timer

def doing(msg: str = None) -> None:
    global dictionary, alex, err

    message = msg.split()
    
    if not len(message) or not msg:
        alex.say('Вы ничего не сказали!')
        alex.update_text('Вы ничего не сказали!')
        return

    else: print('Начинаю анализ...')
    
    max_count = 3
    count = 0
    help = 'Структура словаря:\n'\
                    '┏ Привет\n'\
                    '┃ └алекс - рандомное приветствие\n'\
                    '┣ Погода - автоматический вывод погоды в области вашего проживания\n'\
                    '┣ Выход  - выключение асистента\n'\
                    '┗ Помощь - вывод этого сообщения\n'
    help_say = 'Здравствуй, я могу сказать тебе прогноз погоды, дать полезную информацию из википедии, запланировать какое-либо событие в календаре, поставить таймер, и многое другое.'
    if fuzz_list.extractOne(message[0], ['привет', 'приветствую'])[1] >= 60:
        if datetime.now().hour < 12:
            greeting_day = random.choice(['Доброе утро', 'Доброго утра, создатель', 'Утречка доброго'])
        elif 13 > datetime.now().hour > 12:
            greeting_day = random.choice(['Добрый полдень', 'Прекрасного вам полудня, создатель'])
        elif datetime.now().hour >= 18:
            greeting_day = random.choice(['Добрый вечер', 'Прекрасен сей вечер!'])
        
        alex.say(greeting_day)
        alex.update_text(greeting_day)
    
    elif fuzz_list.extractOne(message[0], ['помощь', 'справка', 'документация'])[1] >= 60:
        alex.say(help_say)
        alex.update_text(help)

    elif fuzz_list.extractOne(message[0], ['таймер'])[1] >= 60 or fuzz_list.extractOne(message[0], ['таймер'])[1] and fuzz_list.extractOne(message[1], ['на'])[1] >= 60:
        try:
            if message[3] == 'минут':
                thread_with_exception(func=lambda: Timer(int(message[2])*60), name='старт таймера').start()
            elif message[3] == 'секунд':
                thread_with_exception(func=lambda: Timer(int(message[2])), name='старт таймера').start()

        except IndexError:
            if message[2] == 'минут':
                thread_with_exception(func=lambda: Timer(int(message[1])*60), name='старт таймера').start()
            elif message[2] == 'секунд':
                thread_with_exception(func=lambda: Timer(int(message[1])), name='старт таймера').start()

    elif fuzz_list.extractOne(message[0], ['что', 'кто'])[1] >= 60:
        if fuzz_list.extractOne(message[1], ['за', 'такое', 'такой', 'такая', 'такие'])[1] >= 60:
            sc = ''
            for i in message[2:]: sc += i+' '
            if sc[-1] == ' ':   
                sc = list(sc)
                sc.pop(-1)
                a = ''
            
            for i in sc: a += i
            
            try:
                data = search(a)
            except requests.exceptions.ConnectTimeout:
                alex.update_text('Плохое интернет соединение, не удалось соединиться с сайтом https://ru.wikipedia.org')
            
            if not err:
                bb = thread_with_exception(func=alex.update_text, args=data, name='обновление текста')
                aa = thread_with_exception(func=alex.say, args=data, name='воспроизведение')
                bb.run()
                aa.run()
            else:
                err = False
                alex.update_text(data)
            
        elif fuzz_list.extractOne(message[1], ['ты', 'вы'])[1] >= 60:
            if fuzz_list.extractOne(message[2], ['умеешь', 'умеете'])[1] >= 60:
                print(help)
            elif fuzz_list.extractOne(message[2], ['такой', 'такое'])[1] >= 60:
                a = random.choice([f"Меня зовут f{alex.name}", f"Я f{alex.name}"])
                alex.say(a)
                alex.update_text(a)
                
    elif fuzz_list.extractOne(message[0], ['поиск', 'найди'])[1] >= 60:
        if len(message[1:]) >= 1:
            a = ''
            for i in message[1:]:
                a += i+' '
            
            if a[-1] == ' ':
                a = list(a)
                a.pop(-1)
            
            b = ''
            for i in a:
                b += i
        
        alex.say(f'открывается {b}')
        alex.update_text(f'открывается {b}')
        webbrowser.open('https://yandex.ru/search/?text='+b, 2)
    
    elif fuzz_list.extractOne(message[0], ['погода', 'прогноз'])[1] >= 60:
        if message[0] == 'прогноз' and message[1] == 'погоды':
            return get_weather()
        
        elif len(message) > 1 and message[0] == 'погода':
            town = ''
            for i in message[1:]: town += i+' '
            if town[-1] == ' ':
                town = list(town)
                town.pop(-1)
            a = ''
            for i in town:
                a+=i
            
            return get_weather(a)
        
        else:
            alex.update_text(get_weather())
            alex.say(get_weather())
    
    elif message[0].isdigit():
        try:
            print('функции математики')
            if message[2].isdigit():
                print('+-/*')
                print(message[1])
                if message[1] == '+':
                    thr1 = thread_with_exception(func=alex.update_text, args=f'будет {int(message[0])+int(message[2])}', name='обновление текста')
                    thr2 = thread_with_exception(func=alex.say, args=f'будет {int(message[0])+int(message[2])}', name='воспроизведение')
                    thr1.start()
                    thr2.start()
                elif message[1] == '-':
                    thr1 = thread_with_exception(func=alex.update_text, args=f'будет {int(message[0])-int(message[2])}', name='обновление текста')
                    thr2 = thread_with_exception(func=alex.say, args=f'будет {int(message[0])-int(message[2])}', name='воспроизведение')
                    thr1.start()
                    thr2.start()
                elif message[1] in ['/', '\\']:
                    thr1 = thread_with_exception(alex.update_text, args=f'будет {int(message[0])/int(message[2])}', name='обновление текста')
                    thr2 = thread_with_exception(alex.say, args=f'будет {int(message[0])/int(message[2])}', name='воспроизведение')
                    thr1.start()
                    thr2.start()
                elif message[1] == 'х':
                    thr1 = thread_with_exception(func=alex.update_text, args=f'будет {int(message[0])*int(message[2])}', name='обновление текста')
                    thr2 = thread_with_exception(func=alex.say, args=f'будет {int(message[0])*int(message[2])}', name='воспроизведение')
                    thr1.start()
                    thr2.start()

            if message[3].isdigit():
                print('**')
                if fuzz_list.extractOne(message[1], ['в'])[1] >= 60 and\
                    fuzz_list.extractOne(message[2], ['степень', 'степени'])[1] >= 60:
                    thr1 = thread_with_exception(func=alex.say, args=f'будет {int(message[0])**int(message[3])}', name='воспроизведение')
                    thr2 = thread_with_exception(func=alex.update_text, args=f'будет {int(message[0])**int(message[3])}', name='обновление текста')
                    thr1.start()
                    thr2.start()

            if message[4].isdigit():
                print('**')
                if fuzz_list.extractOne(message[1], ['возвести', 'возведи'])[1] >= 60 and\
                    fuzz_list.extractOne(message[2], ['в'])[1] >= 60 and\
                    fuzz_list.extractOne(message[3], ['степень'])[1] >= 60:
                    thr1 = thread_with_exception(func=alex.say, args=f'будет {int(message[0])**int(message[4])}', name='воспроизведение')
                    thr2 = thread_with_exception(func=alex.update_text, args=f'будет {int(message[0])**int(message[4])}', name='обновление текста')
                    thr1.start()
                    thr2.start()

        except IndexError:
            print('Ошибка индекса(ничего страшного не произошло)')
        
    else:
        thr1 = thread_with_exception(func=alex.say, args='Я не понял ваш запрос, сформулируйте иначе!', name='воспроизведение')
        thr2 = thread_with_exception(func=alex.update_text, args='Я не понял ваш запрос, сформулируйте иначе!', name='обновление текста')
        thr1.start()
        thr2.start()

    print("Готово")