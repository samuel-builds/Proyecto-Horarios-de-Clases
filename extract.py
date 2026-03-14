import sys
import subprocess

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import fitz
except ImportError:
    install('PyMuPDF')
    import fitz

text = ""
with fitz.open("Proyecto Algoritmos 2526-2.pdf") as doc:
    for page in doc:
        text += page.get_text()

with open("pdf_text.txt", "w", encoding="utf-8") as f:
    f.write(text)
print("PDF extracted successfully.")
