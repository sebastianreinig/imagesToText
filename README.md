# imagesToText with OpenAI



## Overview
Zero-SQL is a web-based application that generates and executes SQL queries based on natural language input using OpenAI's API. The application is built with Flask and Python, providing a user-friendly interface for generating SQL queries without needing SQL knowledge. It also executes the generated SQL queries on a local SQLite database and displays the results in a table format.

Details to the API: OpenAI Platform Documentation

## Requirements
To run this project, you'll need the following dependencies:

Flask
OpenAI API
SQLite3

You can install these dependencies using:

```bash
pip install -r requirements.txt
```


To start the application, run the following command:

```bash
python main.py
```

Once the server is running, you can access the web application at http://127.0.0.1:5000.


## Features
Natural Language to SQL Query Conversion: Enter your question or query in natural language, and OpenAI will generate the SQL code.
SQL Query Execution: The application automatically executes the generated SQL on a SQLite database.
Results Display: The query results are displayed in a formatted table for easy viewing.

## How It Works
Create a .env file and place your OpenAPI Key.

The application can convert images to text via http://127.0.0.1:5000.


## Credits
This project was created with Python and Flask, leveraging OpenAI's API for natural language processing assistance.

