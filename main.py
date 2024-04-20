from settings import OPEN_AI_KEY
from openai import OpenAI


client = OpenAI(api_key=OPEN_AI_KEY)


audio_file= open("./1. Введение в Курс по CSS.mp4", "rb")
transcription = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file
)
print(transcription.text)

