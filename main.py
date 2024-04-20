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

TEST_FILE = "./1. Введение в Курс по CSS.mp4"


client = OpenAI(api_key=OPEN_AI_KEY)


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


# Тестируем класс 
validator = Validator(AVAILABLE_EXTENSIONS, MAX_SIZE_FILE_MB)
print(validator(TEST_FILE))
print(validator(TEST_FILE_2))