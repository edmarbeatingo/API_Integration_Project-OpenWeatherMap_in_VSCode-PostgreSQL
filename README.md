# Weather Data Fetching, PostgreSQL Integration, and Power BI Connection

## Table of Contents
1. Project Overview
2. Technologies Used
3. API Data Fetching
4. PostgreSQL Integration
5. Power BI Connection
6. Running the Project
7. Troubleshooting

### 1. Project Overview
This project fetches real-time weather data using the OpenWeatherMap API, stores it in a PostgreSQL database, and integrates it with Power BI for data visualization. The solution is scheduled to run automatically every day.

### 2. Technologies Used
2.1 Python (for data fetching and storage)
2.2 PostgreSQL (for data storage and processing)
2.3 Power BI (for visualization and reporting)
2.4 VS Code (for development and integration testing)
2.5 Schedule (Python package for automating data fetching)

### 3. API Data Fetching
Fetching Weather Data
We use the OpenWeatherMap API to fetch real-time weather data for a given city.
API Endpoint: "http://api.openweathermap.org/data/2.5/weather?q=<CITY_NAME>&appid=<YOUR_API_KEY>&units=metric"

Required Data Fields: Temperature, Humidity, Weather Description, Timestamp, import requests
from datetime import datetime

### Python Script for Fetching Data
"API_KEY = "your_api_key_here"
CITY = "Delhi"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

response = requests.get(URL)
data = response.json()

weather_data = {
    'city': CITY,
    'temperature': data['main']['temp'],
    'humidity': data['main']['humidity'],
    'weather_description': data['weather'][0]['description'],
    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
}
print(weather_data)"

### 4. PostgreSQL Integration
CREATE DATABASE weather_analysis;
\c weather_analysis;

CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,
    city VARCHAR(50),
    temperature REAL,
    humidity REAL,
    weather_description VARCHAR(100),
    timestamp TIMESTAMP
);
Python Script to Store Data in PostgreSQL
import psycopg2

def create_connection():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="weather_analysis",
        user="postgres",
        password="your_password_here"
    )

def save_to_db(weather_data):
    connection = create_connection()
    cursor = connection.cursor()
    insert_query = '''
    INSERT INTO weather_data (city, temperature, humidity, weather_description, timestamp)
    VALUES (%s, %s, %s, %s, %s)
    '''
    cursor.execute(insert_query, (
        weather_data['city'],
        weather_data['temperature'],
        weather_data['humidity'],
        weather_data['weather_description'],
        weather_data['timestamp']
    ))
    connection.commit()
    cursor.close()
    connection.close()

### 5. Power BI Connection
Steps to Connect PostgreSQL to Power BI
5.1 Open Power BI Desktop
5.2 Go to Home > Get Data > More…
5.3 Select PostgreSQL Database
5.4 Enter Connection Details:
  Server: localhost
  Database: weather_analysis
  Username: postgres
  Password: your_password_here
5.5 Click ‘Connect’
5.6 Select weather_data Table and Load Data
5.7 Create Visualizations in Power BI (e.g., Temperature vs. Time Graph)

### 6. Running the Project
Install Dependencies
Run the following command in your terminal:
pip install requests psycopg2 schedule pandas matplotlib

Schedule Automatic Data Fetching
Add the script to the system scheduler to run every day.
For Windows (Task Scheduler):
schtasks /create /sc daily /tn "WeatherDataFetch" /tr "python path\to\weather_script.py" /st 08:00

### 7. Troubleshooting
Common Issues and Fixes
| Issue | Solution |
|--------|-------------|
|Connection to PostgreSQL fails| Ensure PostgreSQL is running, and credentials are correct|
|--------|-------------|
| API request fails| Check if the API key is valid and rate limits are not exceeded|
|--------|-------------|
|Data not showing in Power BI-|Ensure the table contains data and refresh the connection|
|--------|------|
