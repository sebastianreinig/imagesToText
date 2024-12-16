from flask import Flask, render_template, request, redirect, url_for
from openai import OpenAI
import os
import re
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import base64


# API-Schlüssel aus Umgebungsvariablen abrufen
load_dotenv()
api_key = os.getenv("OPEN_AI_API_KEY")


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Ordner für hochgeladene Bilder
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max. 16 MB pro Datei

# OpenAI API-Initialisierung
client = OpenAI(api_key=api_key)

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Sicherstellen, dass der Upload-Ordner existiert
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def parse_content(content):
    """
    Parst den API-Response-Inhalt, um die relevanten Felder zu extrahieren.
    :param content: Textinhalt, der von der API zurückgegeben wurde.
    :return: Ein Dictionary mit Vorname, Nachname und DSGVO-Zustimmung.
    """
    print("Content received from API:", content)
    try:
        # Angepasste reguläre Ausdrücke für das Format mit Doppelpunkt nach den Markdown-Feldern
        first_name_match = re.search(r"\*\*First Name:\*\*\s*(\w+)", content, re.IGNORECASE)
        last_name_match = re.search(r"\*\*Last Name:\*\*\s*(\w+)", content, re.IGNORECASE)
        #dsgvo_match = re.search(r"DSGVO Consent:\s*(Yes|No)", content, re.IGNORECASE)
        
        # Flexibler Regex für DSGVO-Zustimmung
        dsgvo_match = re.search(
            r"\*\*DSGVO Consent Status:\*\*\s*(Yes|No|Ja|Nein)",
            content,
            re.IGNORECASE,
        )        
        print(dsgvo_match)

        # Ergebnisse speichern
        first_name = first_name_match.group(1) if first_name_match else "Unknown"
        last_name = last_name_match.group(1) if last_name_match else "Unknown"

        if dsgvo_match:
            if dsgvo_match.group(1).lower() in ["yes", "ja"]:
                dsgvo_consent = "Yes"
            else:
                dsgvo_consent = "No"
        else:
            dsgvo_consent = "No"  # Standardwert, falls kein Status gefunden wird

        
        return {"first_name": first_name, "last_name": last_name, "dsgvo_consent": dsgvo_consent}
    except Exception as e:
        return {"first_name": "Error", "last_name": "Error", "dsgvo_consent": "Error"}


def analyze_image(image_path):
    """
    Verarbeitet ein Bild mit OpenAI und extrahiert die gewünschten Informationen.
    :param image_path: Lokaler Pfad zum Bild.
    :return: Ein Dictionary mit Vorname, Nachname und DSGVO-Zustimmung.
    """
    try:
        with open(image_path, "rb") as img_file:
            # API-Anfrage mit Datei
            base64_image = encode_image(image_path)

            response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts data from images. The output should always look like this: **First Name:** <Firstname> - **Last Name:** <LastName> - **DSGVO Consent Status:** <Yes/No>"},
                {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": "Please extract First Name, Last Name, and DSGVO consent status from this image. Return the DSGVO consent as Yes or No.",
                    },
                    {
                    "type": "image_url",
                    "image_url": {
                        "url":  f"data:image/jpeg;base64,{base64_image}"
                    },
                    },
                ],
                }
            ],
            )
            # Extrahiere das Ergebnis
            content = response.choices[0].message.content
            
            # Parsing des Inhalts
            return parse_content(content)
    except Exception as e:
        #print(e)
        return {"first_name": "Error", "last_name": "Error", "dsgvo_consent": "Error"}

@app.route('/', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        uploaded_files = request.files.getlist("files")
        results = []

        for file in uploaded_files:
            if file.filename == '':
                continue
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Analyse des hochgeladenen Bildes
            result = analyze_image(filepath)
            results.append(result)

        return render_template('result.html', results=results)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
