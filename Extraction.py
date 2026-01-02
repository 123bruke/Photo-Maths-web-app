import pytesseract
import cv2
import re
import speech_recognition as sr
import fitz

def extract_equation_from_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    lines = re.findall(r'[^\n]+', text)
    return ' '.join(lines).strip()

def extract_equation_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text_list = [page.get_text() for page in doc]
    text = ' '.join(text_list)
    lines = re.findall(r'[^\n]+', text)
    return ' '.join(lines).strip()

def extract_equation_from_audio(audio_path):
    r = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio, language="th-TH")
    except:
        text = ""
    lines = re.findall(r'[^\n]+', text)
    return ' '.join(lines).strip()
