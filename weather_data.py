import psycopg2
from psycopg2 import sql
import schedule
import time
import requests

# Configure the connection
def create_connection():
    return psycopg2.connect(
        host="localhost",
        port="5433",
        database="weather_forecast",
        user="postgres",
        password="3Dm@rpostgresql"
    )

# Function to create the weather_data table
def create_table():
    connection = create_connection()
    cursor = connection.cursor()
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS weather_data (
        id SERIAL PRIMARY KEY,
        city VARCHAR(50) NOT NULL,
        temperature FLOAT NOT NULL,
        humidity FLOAT NOT NULL,
        weather_description VARCHAR(255),
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    '''
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()
    connection.close()
    print("Table weather_data created successfully")

# Function to fetch and store weather data
def fetch_and_store_weather_data():
    # Example API call to fetch weather data (replace with actual API and parameters)
    response = requests.get("https://api.openweathermap.org/data/2.5/weather?q=London&appid=a99000ba8dd160ef090516f7c455d498")
    data = response.json()

    city = data['name']
    temperature = data['main']['temp']
    humidity = data['main']['humidity']
    weather_description = data['weather'][0]['description']

    connection = create_connection()
    cursor = connection.cursor()
    insert_query = '''
    INSERT INTO weather_data (city, temperature, humidity, weather_description)
    VALUES (%s, %s, %s, %s)
    '''
    cursor.execute(insert_query, (city, temperature, humidity, weather_description))
    connection.commit()
    cursor.close()
    connection.close()
    print("Weather data stored successfully")

# Schedule the job to run daily at 8:00 AM
schedule.every().day.at("08:00").do(fetch_and_store_weather_data)

# Create the table if it doesn't exist
create_table()

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)