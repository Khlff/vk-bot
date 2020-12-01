import vk_api, random
import requests
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import json

token = "061e5dadc62dcb9fdc2beb62aa892d94b75cbc04bda257f0e7bf35b7c4d9f3dd2892f65c6db4eae9b57c7"
weather_api = 'b4819bc1fc3f0bac87716929d12c4f13'

def get_weath(s_city):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find", params={'q': s_city, 'units': 'metric', 'lang': 'ru', 'APPID': weather_api})
        data = res.json()
        strana = 'Страна: ' + str(data['list'][0]['sys']['country'])
        first_str= "Температура в городе " + s_city + ': ' + str(data['list'][0]['main']['temp'])
        second_str = "Ощущается как: "+ str(data['list'][0]['main']['feels_like'])
        third_str = "Влажность: " + str(data['list'][0]['main']['humidity']) + '%'
        fourth_str = "Сейчас:  "+ str(data['list'][0]['weather'][0]['description'])
        rain=''
        snow=''
        if data['list'][0]['rain']!=None:
            rain = 'Идёт дождь'
        if data['list'][0]['snow']!=None:
            snow = 'Идёт снег'
    except Exception as e:
        print("Exception (forecast):", e)
        pass
    return [strana,first_str,second_str,third_str,fourth_str,rain,snow]


vk = vk_api.VkApi(token=token)
vk._auth_token()
longpoll = VkBotLongPoll(vk, 200723963 )


print("Бот запущен")

while True:
    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            mess = event.obj['message']
            peer_id = mess['peer_id']
            text = mess['text']
            text=text.split()
            if text[0] == 'Начать':
                vk.method('messages.send', {'peer_id': peer_id, 'message': 'Привет! Пиши "Погода", чтобы узнать погоду в городе из твоего профиля вк или же используй "Погода *город*"', 'random_id': random.randint(-2147483648, 2147483647)})


            if len(text)==1 and text[0]=='Погода':
                try:
                    city = vk.method('users.get', {'user_ids':peer_id, 'fields': 'city'})[0]['city']['title']
                    for i in get_weath(city):
                        if i != '':
                            vk.method('messages.send', {'peer_id': peer_id, 'message': i, 'random_id': random.randint(-2147483648, 2147483647)})
                except:
                    vk.method('messages.send', {'peer_id': peer_id, 'message': 'В вашем профиле не указан город, пожалуйста введите его вручную используя Погода Ваш_город', 'random_id': random.randint(-2147483648, 2147483647)})
            
            elif len(text)==2 and text[0]=='Погода':
                try:
                    for i in get_weath(text[1]):
                            if i != '':
                                vk.method('messages.send', {'peer_id': peer_id, 'message': i, 'random_id': random.randint(-2147483648, 2147483647)})
                except:
                    vk.method('messages.send', {'peer_id': peer_id, 'message': 'Введите правильное название города', 'random_id': random.randint(-2147483648, 2147483647)})

            elif text[0]=='Погода' and len(text)>2:
                vk.method('messages.send', {'peer_id': peer_id, 'message': 'Введите город через дефис', 'random_id': random.randint(-2147483648, 2147483647)})