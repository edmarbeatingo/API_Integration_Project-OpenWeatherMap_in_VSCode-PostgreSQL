# Weather Data Fetching, PostgreSQL Integration, and Power BI Connection

## Table of Contents
1. [Project Overview](#project-overview)
2. [Technologies Used](#technologies-used)
3. [API Data Fetching](#api-data-fetching)
4. [PostgreSQL Integration](#postgresql-integration)
5. [Power BI Connection](#power-bi-connection)
6. [Running the Project](#running-the-project)
7. [Troubleshooting](#troubleshooting)

## 1. Project Overview
This project fetches real-time weather data using the OpenWeatherMap API, stores it in a PostgreSQL database, and integrates it with Power BI for data visualization. The solution is scheduled to run automatically every day.

## 2. Technologies Used
- **Python** (for data fetching and storage)
- **PostgreSQL** (for data storage and processing)
- **Power BI** (for visualization and reporting)
- **VS Code** (for development and integration testing)
- **Schedule** (Python package for automating data fetching)

## 3. API Data Fetching
### Fetching Weather Data
We use the OpenWeatherMap API to fetch real-time weather data for a given city.  
**API Endpoint**:  
`http://api.openweathermap.org/data/2.5/weather?q=<CITY_NAME>&appid=<YOUR_API_KEY>&units=metric`

### Required Data Fields:
- Temperature
- Humidity
- Weather Description
- Timestamp

### Python Script for Fetching Data:
```python
import requests
from datetime import datetime

API_KEY = "your_api_key_here"
CITY = "Beijing
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

print(weather_data)
```

## 4. PostgreSQL Integration
### Create Database and Table
To store weather data in PostgreSQL, follow these steps:

### 1. Create a database and connect to it:
```python
CREATE DATABASE weather_analysis;
\c weather_analysis;
``
CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,
    city VARCHAR(50),
    temperature REAL,
    humidity REAL,
    weather_description VARCHAR(100),
    timestamp TIMESTAMP
);
```
### 2. Create the table to store weather data:
```python
CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,
    city VARCHAR(50),
    temperature REAL,
    humidity REAL,
    weather_description VARCHAR(100),
    timestamp TIMESTAMP
);
```
### Python Script to Store Data in PostgreSQL
```python
import psycopg2``
``
def create_connection():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="weather_analysis",
        user="postgres",
        password="your_password_here"``
   `` )
`
def save_to_db(weather_data):`
    connection = create_connection()`
    cursor = connection.cursor()``
    
`insert_query = '''
    INSERT INTO weather_data (city, temperature, humidity, weather_description, timestamp)
    VALUES (%s, %s, %s, %s, %s)
    '''`
    
`cursor.execute(insert_query, (
        weather_data['city'],
        weather_data['temperature'],
        weather_data['humidity'],
        weather_data['weather_description'],
        weather_data['timestamp']
    ))`
    
`connection.commit()
    cursor.close()
    connection.close()`
   ` 
print("Data Saved to PostgreSQL")`
```
## 5. Power BI Connection
### Steps to Connect PostgreSQL to Power BI:
1. Open Power BI Desktop.
2. Go to Home > Get Data > More….
3. Select PostgreSQL Database.
4. Enter the connection details:
    -Server: localhost
    -Database: weather_analysis
    -Username: postgres
    -Password: your_password_here
5. Click Connect.
6. Select the weather_data table and load the data.
7. Create visualizations in Power BI (e.g., Temperature vs. Time Graph).

## 6. Running the Project
### Install Dependencies
Run the following command in your terminal to install the required dependencies
```python
pip install requests psycopg2 schedule pandas matplotlib``
```
### Schedule Automatic Data Fetching
To run the script automatically every day, add it to your system scheduler.
### For Windows (Task Scheduler):
```python
schtasks /create /sc daily /tn "WeatherDataFetch" /tr "python path\to\weather_script.py" /st 08:00
f``
```
## 7. Troubleshooting
| **Issue**                          | **Solution**                                          |
|------------------------------------|------------------------------------------------------|
| Connection to PostgreSQL fails     | Ensure PostgreSQL is running, and credentials are correct. |
| API request fails                  | Check if the API key is valid and rate limits are not exceeded. |
| Data not showing in Power BI       | Ensure the table contains data and refresh the connection. |
