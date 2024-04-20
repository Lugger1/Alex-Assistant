import urllib.request
import requests
import json

def get_weather(city = None) -> str:
    print(f'запрошенный город: {city}')
    url = f'https://api.openweathermap.org/data/2.5/weather?q={get_location() if not city else city}&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'

    weather_json = requests.get(url).json()
    
    print(f'weather_json: {weather_json}')
    
    info = {}
    try:
        info['name'] = weather_json['name']
        info['descriprion'] = weather_json['weather'][0]['description']
        info['degrees'] = weather_json['main']['temp']
        info['wind'] = weather_json['wind']['speed']
    except KeyError:
        return 'Такой город не найден!'
    
    wind = ''
    if list(str(round(info['wind'])))[-1] == '1':
        wind = ' метр в секунду. '
    elif list(str(round(info['wind'])))[-1] in ['2', '3', '4']:
        wind = ' метра в секунду. '
    else: wind = ' метров в секунду. '

    end = ''
    if not city: end = '(Информация была взята с вашего примерного местоположения из-за отсутствия указанного города)'

    sayed_string = f'Сегодня в городе {info['name']} {info['descriprion']}, температура {round(info['degrees'])} градусов по цельсию, и ветер {info['wind']}'+wind+end

    return sayed_string

def get_location():
    url = 'http://ipinfo.io/json'
    response = urllib.request.urlopen(url)
    data = json.load(response)

    return data['city']

if __name__ == '__main__':
    print(get_weather())
