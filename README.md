# imagesToText with OpenAI

![imagesToText](https://github.com/user-attachments/assets/7bc6dcdf-2373-4719-865a-182030db58ed)


## Overview
This Application allows users to upload images, which are then processed using OpenAI for data extraction. The process involves the following steps:

File Upload:
Users can upload multiple images (e.g., JPEGs) via a user-friendly web interface.

Analysis with OpenAI:
The uploaded images are sent to OpenAI's API for analysis.
The AI extracts key information from the images, including:
First Name
Last Name
DSGVO Consent (Yes/No)

Display Results in a Table:
The extracted information is displayed in a structured table format, showing:
First Name
Last Name
GDPR Consent (Yes/No)

Automation and Flexibility:
The application is designed to handle various image formats and content, extracting the most relevant data efficiently.

## Requirements

You can install these dependencies using:

```bash
pip install -r requirements.txt
```


To start the application, run the following command:

```bash
python main.py
```

Once the server is running, you can access the web application at http://127.0.0.1:5000.



## How It Works
Create a .env file and place your OpenAPI Key.

The application can convert images to text via http://127.0.0.1:5000.


## Credits
This project was created with Python and Flask, leveraging OpenAI's API for natural language processing assistance.

