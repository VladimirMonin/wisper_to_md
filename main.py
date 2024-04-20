"""
Программа для отправки аудио и видео файлов на сервер OpenAI и получения текстовой транскрипции

Классы:

WisperFacade - управляющий класс
SpeechRecognitionService - класс для отправки аудио и видео файлов на сервер OpenAI и получения текстовой транскрипции
FileValidator - класс для проверки файлов на соответствие формату
"""

from settings import OPEN_AI_KEY, AVAILABLE_EXTENSIONS, MAX_SIZE_FILE_MB
from openai import OpenAI
import os

TEST_FILE = r"E:\COURSES\Добрый добрый Джанго - Балакирев\10. OAuth 2.0 - социальная аутентификация\10.1 Протокол OAuth 2.0. Установка пакета Python-Social-Auth\Шаг 1 – Протокол OAuth 2.0. Установка пакета Python-Social-Auth.mp4"


client = OpenAI(api_key=OPEN_AI_KEY)

settings_dict = {}

# audio_file= open(TEST_FILE, "rb")
# transcription = client.audio.transcriptions.create(
#   model="whisper-1", 
#   file=audio_file
# )
# print(transcription.text)


# FileValidator

class Validator:
    def __init__(self, available_extensions: tuple[str], max_size_file_mb: int):
        self.file_path: str | None = None
        self.file_name: str | None = None
        self.available_extensions = available_extensions
        self.max_size_file_mb = max_size_file_mb

    def __get_file_name(self, file_path: str) -> str:
        self.file_name = file_path.split('/')[-1]

    def __check_extension(self, file_name: str) -> bool:
        return file_name.endswith(self.available_extensions)
    
    def __validate_size_file(self, file_path: str) -> bool:
        return os.path.getsize(file_path) <= self.max_size_file_mb * 1024 * 1024
    
    def validate(self, file_path: str) -> bool:
        self.__get_file_name(file_path)
        return self.__check_extension(self.file_name) and self.__validate_size_file(file_path)
    
    def __call__(self, file_path: str) -> bool:
        return self.validate(file_path)


class SpeechRecognitionService:
    """
    Класс для отправки аудио и видео файлов на сервер OpenAI и получения текстовой транскрипции
    Используется внутри класса WisperFacade, сразу после валидации файла

    Обрабатывает файлы через __call__ метод

    Атрибуты:
    client - объект класса OpenAI
    api_key - ключ для доступа к API OpenAI

    Методы:
    __call__ - отправляет файл на сервер OpenAI и возвращает текстовую транскрипцию, отдает результат в WisperFacade
    open_file - открывает файл на чтение
    request - отправляет запрос к серверу OpenAI

    """
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)
        self.file_path: str | None = None

        
    def __request(self) -> str:
        """
        Отправляем запрос на сервер OpenAI
        """
        audio_file= open(self.file_path, "rb")
        transcription = self.client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-1",

        )
        return transcription.text
    
    def __call__(self, file_path: str) -> str:
        """
        Отправляем файл на сервер OpenAI и возвращаем текстовую транскрипцию
        """
        self.file_path = file_path
        return self.__request()
    


class WisperFacade:
    """
    Управляющий класс

    Атрибуты:
    validator - объект класса FileValidator
    speech_recognition - объект класса SpeechRecognitionService

    Методы:
    __call__ - вызывает методы валидации файла и отправки файла на сервер OpenAI
    """
    def __init__(self, api_key: str, available_extensions: tuple[str], max_size_file_mb: int):
        self.validator = Validator(available_extensions, max_size_file_mb)
        self.speech_recognition = SpeechRecognitionService(api_key)
    
    def __call__(self, file_path: str) -> str:
        if self.validator(file_path):
            return self.speech_recognition(file_path)
        else:
            return "File is not valid"
        

wisper = WisperFacade(OPEN_AI_KEY, AVAILABLE_EXTENSIONS, MAX_SIZE_FILE_MB)
result = wisper(TEST_FILE)


# Сохраним в markdown файл
with open("result.md", "w", encoding="utf-8") as file:
    file.write(result)
