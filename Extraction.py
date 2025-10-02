import pytesseract
import cv2
import re

def extract_equation_from_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    lines = re.findall(r'[^\n]+', text)
    return ' '.join(lines).strip()
  
