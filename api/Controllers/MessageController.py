from flask import jsonify, request
from Models.Message import Message, db
from sqlalchemy import desc
from datetime import datetime
import speech_recognition as sr
import asyncio
import os
import requests
from pathlib import Path
import re
from flasgger import swag_from

API_URL = "https://api.polza.ai/api/v1/chat/completions"


def _load_env_from_file():
    # Пытаемся загрузить ключ из ближайших .env без выхода за пределы родителей
    here = Path(__file__).resolve()
    parents = list(here.parents)

    candidates = []
    # Корень проекта в контейнере (обычно '/')
    if len(parents) >= 2:
        candidates.append(parents[1] / ".env")  # '/.env' после COPY . .
    # Папка на уровень выше текущего файла (например, '/Controllers' -> '/.env')
    if len(parents) >= 1:
        candidates.append(parents[0].parent / ".env")
    # Локально рядом с файлом (на случай альтернативной раскладки)
    candidates.append(here.parent / ".env")

    # Учитываем test/.env только если он достижим без выхода за границы
    if len(parents) >= 2:
        test_env = parents[1] / "test" / ".env"
        candidates.append(test_env)

    for env_path in candidates:
        try:
            if env_path.exists():
                for raw in env_path.read_text(encoding="utf-8").splitlines():
                    line = raw.strip()
                    if not line or line.startswith('#') or '=' not in line:
                        continue
                    k, v = line.split('=', 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    os.environ.setdefault(k, v)
        except Exception:
            # Тихо игнорируем ошибки чтения .env
            pass


_load_env_from_file()


def _auth_header() -> str:
    token = os.getenv("POLZA_API_KEY", "").strip()
    if not token:
        raise RuntimeError("POLZA_API_KEY не задан (укажите в api/.env или test/.env)")
    return token if token.lower().startswith("bearer ") else f"Bearer {token}"


def audio_to_text(audio):
    # Создаем объект распознавателя речи
    recognizer = sr.Recognizer()

    # Загружаем аудио файл
    audio_file = sr.AudioFile(audio)

    # Распознаем речь из аудио файла
    with audio_file as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language="ru-RU")

    return text



def request_gpt_simple(text):
    # Установка политики цикла событий для предотвращения предупреждения (если где-то есть asyncio)
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())

    payload = {
        "model": "qwen/qwen-turbo",
        "messages": [
            {"role": "system", "content": "Ты голосовой помощник банка. Отвечай кратко и по делу."},
            {"role": "user", "content": f"Обращение: {text}"},
        ],
        "temperature": 0.7,
        "max_tokens": 512,
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": _auth_header(),
    }

    resp = requests.post(API_URL, json=payload, headers=headers, timeout=30)
    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        # Пробрасываем текст ответа для диагностики в логи/клиент
        raise requests.HTTPError(f"{e} | Body: {resp.text}") from e

    data = resp.json()
    return data.get("choices", [{}])[0].get("message", {}).get("content", "")

"""
method=GET

returns {
    status: true/false,
    message: OK / Error
    data = {{id, theme_id, message, time, type, code, sender}, ...} if success
}

sender: false -> user / true -> server
"""
@swag_from({
    'tags': ['Messages'],
    'responses': {
        200: {
            'description': 'Список сообщений',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'boolean'},
                    'message': {'type': 'string'},
                    'data': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
'properties': {
                            'id': {'type': 'integer'},
                            'message': {'type': 'string'},
                            'time': {'type': 'string'},
                            'type': {'type': 'boolean'},
                            'code': {'type': 'string'},
                            'sender': {'type': 'boolean'}
                        }
                        }
                    }
                }
            }
        }
    }
})
def get_messages():
    messages = Message.query.all()
    output = {
        'status': True if len(messages) > 0 else False,
        'message': "OK" if len(messages) > 0 else "Empty table",
        'data': []
    }
    for message in messages:
        user_data = {
            'id': message.id,
            'message': message.message,
            'time': message.time,
            'type': message.type,
            'code': message.code,
            'sender': message.sender
        }
        output['data'].append(user_data)
    return jsonify(output)

"""
method=GET/message_id

returns {
    status: true/false,
    message: OK / Error
    data = {id, theme_id, message, time, type, code, sender} if success
}

sender: 0 -> user / 1 -> server
"""
@swag_from({
    'tags': ['Messages'],
    'parameters': [
        {
            'name': 'item_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID сообщения'
        }
    ],
    'responses': {
        200: {
            'description': 'Информация о сообщении',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'boolean'},
                    'message': {'type': 'string'},
                    'data': {
                        'type': 'object',
'properties': {
                            'id': {'type': 'integer'},
                            'message': {'type': 'string'},
                            'time': {'type': 'string'},
                            'type': {'type': 'boolean'},
                            'code': {'type': 'string'},
                            'sender': {'type': 'boolean'}
                        }
                    }
                }
            }
        },
        404: {
            'description': 'Сообщение не найдено',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        }
    }
})
def get_message(item_id):
    message = Message.query.get(item_id)
    if message:
        user_data = {
            'id': message.id,
            'message': message.message,
            'time': message.time,
            'type': message.type,
            'code': message.code,
            'sender': message.sender
        }
        return jsonify({'status': True, 'message': 'OK', 'data': user_data})
    else:
        return jsonify({'status': False, 'message': 'Message not found'}), 404

"""
method=POST

POST body for sending message: user_id, type, code="000", message
type: 0 -> text message / 1 -> audio message
returns {
    status: true/false,
    message: Server response / "none" (if ai is dumb)
    ai_msg_time = time, when server responded
    user_msg_time = time, when server registered user request
    redir = ""
    message_id = user inserted message id
}

POST body for target action: code
returns {
    message: server ask (you should pop it into chat from server)
    redir = "api/*insert api route*" / false
    values = {code: user_option1, code: user_option2} / code
}

example logic - if (redir) route(localhost/redir)
"""    
@swag_from({
    'tags': ['Messages'],
    'consumes': ['application/x-www-form-urlencoded', 'multipart/form-data'],
    'parameters': [
        {
            'name': 'user_id',
            'in': 'formData',
            'type': 'integer',
            'required': True,
            'description': 'ID пользователя'
        },
        {
            'name': 'type',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Тип сообщения (0 - текст, 1 - аудио)'
        },
        {
            'name': 'code',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Код сообщения'
        },
        {
            'name': 'message',
            'in': 'formData',
            'type': 'string',
            'required': False,
            'description': 'Текст сообщения (для type=0). Для type=1 отправьте файл в поле message как multipart/form-data.'
        }
    ],
    'responses': {
        200: {
            'description': 'Сообщение обработано',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'redir': {'type': 'string'},
                    'values': {
                        'oneOf': [
                            {'type': 'string'},
                            {
                                'type': 'object',
                                'additionalProperties': {
                                    'type': 'string'
                                }
                            }
                        ]
                    },
                    'title': {'type': 'string'}
                }
            }
        },
        400: {
            'description': 'Ошибка в запросе',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        },
        201: {
            'description': 'Сообщение добавлено',
            'schema': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'boolean'},
                    'message': {'type': 'string'},
                    'user_msg_time': {'type': 'string'},
                    'ai_msg_time': {'type': 'string'},
                    'redir': {'type': 'string'},
                    'message_id': {'type': 'integer'}
                }
            }
        }
    }
})
def add_message():
    user_id = request.form.get('user_id', -1)
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    type = request.form.get('type', 2)
    code = request.form.get('code')
    sender = False
    redir = ""
    if code != "000":
        target_theme_id = list(code)[0]
        theme_index = list(code)[1]
        mas_index = list(code)[2]
        match target_theme_id:
            case "1":
                match theme_index:
                    case "1":   # Потребительский
                        match mas_index:
                            case "0":
                                response = "Какая у вас цель кредитования?"
                                return jsonify({'message': response, 'redir': redir if redir != "" else False, 'values': "111"}), 200
                            case "1":
                                response = "На какую сумму вы хотите взять кредит?"
                                return jsonify({'message': response, 'redir': redir if redir != "" else False, 'values': "112"}), 200
                            case "2":
                                response = "На какой срок вы планируете взять кредит?"
                                return jsonify({'message': response, 'redir': redir if redir != "" else False, 'values': "115"}), 200
                    case "2":    # Автокредит
                        match mas_index:
                            case "0":
                                response = "Какая стоимость автомобиля?"
                                return jsonify({'message': response, 'redir': redir if redir != "" else False, 'values': "121"}), 200
                            case "1":
                                response = "Каков первоначальный взнос?"
                                return jsonify({'message': response, 'redir': redir if redir != "" else False, 'values': "122"}), 200
                            case "2":
                                response = "На какой срок вы планируете взять кредит?"
                                return jsonify({'message': response, 'redir': redir if redir != "" else False, 'values': "125"}), 200

                    case "3":   # Ипотека
                        match mas_index:
                            case "0":
                                response = "Какая у вас цель кредитования?"
                                return jsonify({'message': response, 'redir': redir if redir != "" else False, 'values': "131"}), 200
                            case "1":
                                response = "На какую сумму вы хотите взять кредит?"
                                return jsonify({'message': response, 'redir': redir if redir != "" else False, 'values': "132"}), 200
                            case "2":
                                response = "Каков первоначальный взнос?"
                                return jsonify({'message': response, 'redir': redir if redir != "" else False, 'values': "133"}), 200
                            case "3":
                                response = "На какой срок вы планируете взять кредит?"
                                return jsonify({'message': response, 'redir': redir if redir != "" else False, 'values': "135"}), 200
                match mas_index:
                    case "5":
                        response = "Укажите Наименование"
                        return jsonify({'message': response, 'redir': redir if redir != "" else False, 'values': "1" + theme_index + "6"}), 200
                    case "6":
                        response = "Укажите ИНН"
                        return jsonify({'message': response, 'redir': redir if redir != "" else False, 'values': "1" + theme_index + "7"}), 200
                    case "7":
                        response = "Укажите Фактический адрес компании по месту вашей работы"
                        return jsonify({'message': response, 'redir': redir if redir != "" else False, 'values': "1" + theme_index + "8"}), 200
                    case "8":
                        response = "Укажите Среднемесячный доход после уплаты налогов за последние 12 месяцев"
                        return jsonify({'message': response, 'redir': redir if redir != "" else False, 'values': "1" + theme_index + "9"}), 200
                    case "9":    
                        if theme_index == '1':
                            redir = "api/consumercredits/"
                            title = "Потребительский кредит"
                        elif theme_index == '2':
                            redir = "api/autocredits/"
                            title = "Автокредит"
                        elif theme_index == '3':
                            redir = "api/mortgages/"
                            title = "Ипотека"
                        return jsonify({'redir': redir if redir != "" else False, 'title': "История операций"}), 200

            case "2":
                match theme_index:
                    case "1":
                        response = "Какая сумма вклада?"
                        return jsonify({'message': response, 'redir': redir if redir != "" else False, 'values': "220"}), 200
                    case "2":
                        response = "Какой срок размещения?"
                        return jsonify({'message': response, 'redir': redir if redir != "" else False, 'values': "230"}), 200
                    case "3":
                        redir = "api/contributions"
                        return jsonify({'redir': redir if redir != "" else False, 'title': "Открытие вклада"}), 200
            case "3":
                match theme_index:
                    case "1":
                        response = "На какую валюту вы хотите обменять?"
                        return jsonify({'message': response, 'redir': redir if redir != "" else False, 'values': "320"}), 200
                    case "2":
                        response = "Сколько вы хотите обменять?"
                        return jsonify({'message': response, 'redir': redir if redir != "" else False, 'values': "330"}), 200
                    case "3":
                        redir = "api/currencyexchanges"
                        return jsonify({'redir': redir if redir != "" else False, 'title': "Обмен валюты"}), 200

            case "4":
                match theme_index:
                    case "1":
                        response = "Укажите номер счета на который вы хотите перевести деньги?"
                        return jsonify({'message': response, 'redir': redir if redir != "" else False, 'values': "320"}), 200
                    case "2":
                        response = "Укажите сумму перевода?"
                        return jsonify({'message': response, 'redir': redir if redir != "" else False, 'values': "330"}), 200
                    case "3":
                        redir = "api/transactions"
                        return jsonify({'redir': redir if redir != "" else False, 'title': "Перевод"}), 200
            case "6":
                match theme_index:
                    case "1":
                        redir = "periodSpend"
                        return jsonify({'redir': redir if redir != "" else False, 'title': "Расход за период"}), 200
    else:
        if int(user_id) < 1 or not type or not code:
            return jsonify({'status': False, 'message': 'Missing required fields'}), 400
        
        if type == '1':
            # Проверяем, есть ли файл в запросе
            if 'message' not in request.files:
                return jsonify({'status': False, 'message': 'No file part'}), 400

            # Получаем файл из запроса
            message_file = request.files['message']
            message = audio_to_text(message_file)
        elif type == '0':
            message = request.form.get('message')
        
        # Ответ без тематики
        response = request_gpt_simple(message)

        new_message = Message(message=message, time=time, type=bool(int(type)), code=code, sender=sender)
        new_response = Message(message=response, time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), type=False, code="000", sender=True)
        db.session.add(new_message)
        db.session.add(new_response)
        db.session.commit()

        inserted_message_id = new_message.id

        return jsonify({'status': True, 'message': response, 'user_msg_time': new_message.time, 'ai_msg_time': new_response.time, 'redir': redir, 'message_id': inserted_message_id}), 201

        # Находим последнюю тему для данного пользователя
        last_theme = Theme.query.filter_by(user_id=user_id).order_by(desc(Theme.id)).first()

        if last_theme is None:
            last_theme = "chupakabra"
            last_theme_id = 0
        else: 
            last_theme_id = last_theme.id
            last_theme = last_theme.theme_name

        response, theme = request_gpt(message, ("Открытие кредита", "Открытие вклада", "Обмен валюты", "Перевод", "История операций", "Расход за период"), last_theme, last_theme_id)
        if (response == "none"):
            response, theme = request_gpt(message, ("Открытие кредита", "Открытие вклада", "Обмен валюты", "Перевод", "История операций", "Расход за период"), last_theme, last_theme_id)

        spec_theme = ("открытие кредита", "открытие вклада", "обмен валюты", "перевод", "история операций", "расход за период")
        if theme.strip() in spec_theme:
            if theme.strip() == spec_theme[0]:
                code = "100"
                response = "Какой кредит вы хотите открыть?" # НА ФРОНТ ТЕКСТОМ НА ВЫВОД В ДИАЛОГ
                values = {110: "Потребительский", 120: "Автокредит", 130: "Ипотека"}
                return jsonify({'message': response, 'redir': redir if redir != "" else False, 'values': values}), 200
            elif theme.strip() == spec_theme[1]:
                code = "200"
                response = "Условия договора:/n Срок договора - 36 месяцев/n Расторжение без потери % ежеквартально/n Выплата % ежеквартально/n Без пополнения/n С капитализацией/n Без автопролонгации/n Хотите открыть вклад?" # НА ФРОНТ ТЕКСТОМ НА ВЫВОД В ДИАЛОГ
                return jsonify({'message': response, 'redir': redir if redir != "" else False, 'values': "210"}), 200
            elif theme.strip() == spec_theme[2]:
                code = "300"
                response = "Какую валюту вы хотите обменять?"  # НА ФРОНТ ТЕКСТОМ НА ВЫВОД В ДИАЛОГ
                return jsonify({'message': response, 'redir': redir if redir != "" else False, 'values': "310"}), 200
            elif theme.strip() == spec_theme[3]:
                code = "400"
                response = "С какого счета вы хотите перевести деньги?"  # НА ФРОНТ ТЕКСТОМ НА ВЫВОД В ДИАЛОГ
                return jsonify({'message': response, 'redir': redir if redir != "" else False, 'values': "410"}), 200
            elif theme.strip() == spec_theme[4]:
                code = "500"
                redir = "/api/historyOperations"
                return jsonify({'redir': redir if redir != "" else False, 'title': "История операций"}), 200
            elif theme.strip() == spec_theme[5]:
                code = "600"
                response = "С какого по какое число вы хотите узнать расход средств?" # ПРИЗЫВ К ДЕЙСТВИИ НА ПЕРЕХОД К СТРАНИЦЕ РАСХОД ЗА ПЕРИОД
                return jsonify({'message': response, 'redir': redir if redir != "" else False, 'values': "610"}), 200
        else:

            if last_theme.strip() == theme.strip():
                theme_id = last_theme_id
            else:
                url = 'http://localhost:5000/api/themes/' 
                payload = {
                    'user_id': user_id,
                    'theme_name': theme
                }
                themeJSON = requests.post(url, data=payload)
                # Обработка ответа и извлечение theme_id
                if themeJSON.status_code == 201:  # Проверяем успешность запроса
                    theme_id = themeJSON.json().get('theme_id')

            new_message = Message(theme_id=theme_id, message=message, time=time, type=bool(int(type)), code=code, sender = sender)
            new_response = Message(theme_id=theme_id, message=response, time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), type=False, code="000", sender = True)
            db.session.add(new_message)
            db.session.add(new_response)
            db.session.commit()

            inserted_message_id = new_message.id

            return jsonify({'status': True, 'message': response, 'user_msg_time': new_message.time, 'ai_msg_time': new_response.time, 'redir': redir, 'message_id': inserted_message_id}), 201
