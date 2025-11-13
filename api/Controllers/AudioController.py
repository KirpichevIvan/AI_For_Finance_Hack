from flask import jsonify, request, send_file
from gtts import gTTS
from flasgger import swag_from

def text_to_audio(text, path):
    tts = gTTS(text=text, lang='ru')
    tts.save(path)

@swag_from({
    'tags': ['Audio'],
    'consumes': ['application/x-www-form-urlencoded'],
    'parameters': [
        {
            'name': 'text',
            'in': 'formData',
            'type': 'string',
            'required': True,
            'description': 'Текст для преобразования в аудио'
        }
    ],
    'responses': {
        200: {
            'description': 'Аудиофайл успешно сгенерирован',
            'schema': {
                'type': 'file',
                'format': 'binary'
            }
        },
        400: {
            'description': 'Ошибка в запросе',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        }
    }
})
def convert_text_to_audio():
    if 'text' not in request.form:
        return jsonify({'error': 'Text parameter is missing'}), 400

    text = request.form['text']

    # Уникальное имя для аудиофайла
    audio_file_path = 'output_audio.wav'

    # Преобразование текста в аудиофайл
    text_to_audio(text, audio_file_path)

    # Посылаем аудиофайл обратно в ответе
    return send_file(audio_file_path, as_attachment=True)