from pypdf import PdfReader
import pyttsx3
from gtts import gTTS

reader = PdfReader("sample_pdf_to_speech.pdf")

text = ""

for page in reader.pages:
    text += page.extract_text()


engine = pyttsx3.init()
engine.say(text)
engine.runAndWait()

file = gTTS(text=text,lang="en")
file.save("speech.mp3")
