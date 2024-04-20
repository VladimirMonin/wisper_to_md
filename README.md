# wisper_to_md

## Ограничение модели

В настоящее время размер загружаемых файлов ограничен 25 МБ, и поддерживаются следующие типы входных файлов:
mp3
mp4
mpeg
mpga
m4a
wav
webm

ПОЛНЫЙ СПИСОК!
['flac', 'm4a', 'mp3', 'mp4', 'mpeg', 'mpga', 'oga', 'ogg', 'wav', 'webm']

Для вашего проекта, который принимает аудио- или видеофайлы, преобразует их и использует сервисы для распознавания речи, подойдут такие паттерны проектирования как Фасад, Стратегия, и возможно Фабрика для создания компонентов, в зависимости от типа файлов или операций. Я предложу следующую структуру программы с учетом масштабируемости и гибкости в добавлении новых функций.

### Структура программы

1. **Фасад (Facade)**
   - Создайте класс `FileProcessingFacade`, который будет предоставлять упрощенный интерфейс для сложной логики обработки файлов. Этот фасад будет координировать работу различных модулей системы.

2. **Стратегия (Strategy)**
   - Используйте паттерн стратегия для выбора метода конвертации в зависимости от типа и размера файла. Классы `AudioConversionStrategy` и `VideoConversionStrategy` могут быть производными от общего интерфейса `ConversionStrategy`.

3. **Фабрика (Factory)**
   - `ConverterFactory` может быть использован для создания нужного объекта `ConversionStrategy` в зависимости от типа и свойств файла.

4. **Компоненты**
   - `FileAnalyzer` - класс для определения типа и размера файла.
   - `FileConverter` - класс, который использует `ConversionStrategy` для преобразования файлов.
   - `SpeechRecognitionService` - класс для отправки аудио в OpenAI Whisper и получения текста.
   - `MarkdownGenerator` - класс для создания Markdown файла с результатами и метаданными.

5. **Dataclass и настройки**
   - Используйте `dataclasses` для управления настройками, такими как пути к каталогам, API ключи и другие параметры. Класс `AppConfig` может хранить все настройки.

6. **Расширяемость**
   - Для будущей обработки целой папки файлов можно добавить класс `DirectoryProcessor`, который будет итерировать по файлам в папке и использовать `FileProcessingFacade`.

### Пример кода (краткая схема)

```python
from dataclasses import dataclass

@dataclass
class AppConfig:
    obsidian_storage_path: str
    result_folder: str
    openai_api_key: str

class FileProcessingFacade:
    def __init__(self, config: AppConfig):
        self.config = config

    def process_file(self, file_path: str):
        # Анализ файла
        # Конвертация файла
        # Распознавание речи
        # Генерация Markdown
        pass

class FileAnalyzer:
    def analyze(self, file_path: str):
        # Возвращает тип файла и его размер
        pass

class ConversionStrategy:
    def convert(self, file_path: str):
        pass

class AudioConversionStrategy(ConversionStrategy):
    def convert(self, file_path: str):
        # Конвертация аудио
        pass

class VideoConversionStrategy(ConversionStrategy):
    def convert(self, file_path: str):
        # Конвертация видео
        pass

class ConverterFactory:
    def get_converter(self, file_type: str):
        if file_type == 'audio':
            return AudioConversionStrategy()
        elif file_type == 'video':
            return VideoConversionStrategy()

class SpeechRecognitionService:
    def recognize(self, file_path: str):
        # Отправка файла в OpenAI Whisper
        pass

class MarkdownGenerator:
    def generate(self, transcription, metadata):
        # Создание файла Markdown с метаданными
        pass

# Пример использования
config = AppConfig("path/to/obsidian", "path/to/results", "your_api_key")
facade = FileProcessingFacade(config)
facade.process_file("path/to/file.mp4")
```
