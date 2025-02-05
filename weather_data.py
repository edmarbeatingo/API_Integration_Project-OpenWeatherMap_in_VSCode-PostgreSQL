import requests
import csv
import os
import psycopg2
import schedule
import time
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Get the absolute path to the Downloads folder
DOWNLOADS_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")

# Define file paths
CSV_FILE = os.path.join(DOWNLOADS_FOLDER, "weather_data.csv")
PLOT_FILE = os.path.join(DOWNLOADS_FOLDER, "temperature_plot.png")

# Database connection details
DB_CONFIG = {
    "host": "localhost",
    "port": "5433",
    "database": "weather_analysis",
    "user": "postgres",
    "password": "3Dm@rpostgresql"
}

# OpenWeatherMap API Configuration
CITY = "Beijing"
API_KEY = "a99000ba8dd160ef090516f7c455d498"  # Replace with your actual API key

# 🔹 Fetch weather data from OpenWeatherMap API
def get_weather_data(city, api_key):
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {'q': city, 'appid': api_key, 'units': 'metric'}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        weather_data = {
            'city': city,
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'weather_description': data['weather'][0]['description'],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        return weather_data

    except requests.exceptions.RequestException as e:
        print(f"❌ API Request Failed: {e}")
        return None

# 🔹 Save weather data to CSV
def save_to_csv(weather_data):
    fieldnames = ['city', 'temperature', 'humidity', 'weather_description', 'timestamp']
    file_exists = os.path.isfile(CSV_FILE)

    try:
        with open(CSV_FILE, mode='a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(weather_data)
        print(f"✅ Data saved to CSV: {CSV_FILE}")

    except Exception as e:
        print(f"❌ Error saving to CSV: {e}")

# 🔹 Establish database connection
def create_connection():
    try:
        connection = psycopg2.connect(**DB_CONFIG)
        return connection
    except psycopg2.Error as e:
        print(f"❌ Database Connection Error: {e}")
        return None

# 🔹 Save weather data to PostgreSQL database
def save_to_db(weather_data):
    connection = create_connection()
    if not connection:
        return

    cursor = connection.cursor()
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS weather_data (
        id SERIAL PRIMARY KEY,
        city VARCHAR(50),
        temperature REAL,
        humidity REAL,
        weather_description VARCHAR(100),
        timestamp TIMESTAMP
    )
    '''
    
    insert_query = '''
    INSERT INTO weather_data (city, temperature, humidity, weather_description, timestamp)
    VALUES (%s, %s, %s, %s, %s)
    '''

    try:
        cursor.execute(create_table_query)
        cursor.execute(insert_query, (
            weather_data['city'],
            weather_data['temperature'],
            weather_data['humidity'],
            weather_data['weather_description'],
            weather_data['timestamp']
        ))
        connection.commit()
        print("✅ Data saved to PostgreSQL database")

    except psycopg2.Error as e:
        print(f"❌ Database Error: {e}")
    
    finally:
        cursor.close()
        connection.close()

# 🔹 Fetch and store weather data
def fetch_and_store_weather_data():
    weather_data = get_weather_data(CITY, API_KEY)
    if weather_data:
        save_to_csv(weather_data)
        save_to_db(weather_data)
        print("✅ Weather data successfully stored.")
    else:
        print("❌ Failed to fetch weather data.")

# 🔹 Fetch past 7 days' data from PostgreSQL
def fetch_past_week_data():
    connection = create_connection()
    if not connection:
        return []

    cursor = connection.cursor()
    query = '''
    SELECT city, temperature, humidity, weather_description, timestamp
    FROM weather_data
    WHERE timestamp >= NOW() - INTERVAL '7 days'
    ORDER BY timestamp
    '''
    
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows

    except psycopg2.Error as e:
        print(f"❌ Database Query Error: {e}")
        return []

    finally:
        cursor.close()
        connection.close()

# 🔹 Compute averages
def compute_averages(data):
    df = pd.DataFrame(data, columns=['city', 'temperature', 'humidity', 'weather_description', 'timestamp'])
    if df.empty:
        return None, None, df

    avg_temp = df['temperature'].mean()
    avg_humidity = df['humidity'].mean()
    return avg_temp, avg_humidity, df

# 🔹 Generate temperature plot
def generate_plot(df):
    if df.empty:
        print("❌ No data available for plotting.")
        return
    
    df['timestamp'] = pd.to_datetime(df['timestamp'])  # Ensure timestamp format is correct
    plt.figure(figsize=(10, 5))
    plt.plot(df['timestamp'], df['temperature'], marker='o', linestyle='-', color='b', label="Temperature")
    
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.title(f'Temperature Over Time - {CITY}')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()

    # Save plot to Downloads folder
    plt.savefig(PLOT_FILE)
    print(f"✅ Temperature plot saved: {PLOT_FILE}")

    # Force display the plot
    plt.show()
    plt.close()

    # Verify file saved
    if os.path.exists(PLOT_FILE):
        print(f"✅ Plot successfully saved: {PLOT_FILE}")
    else:
        print("❌ Error: Plot file was not saved.")

# 🔹 Analyze weather data
def analyze_weather_data():
    data = fetch_past_week_data()
    if not data:
        print("❌ No data available for analysis.")
        return

    avg_temp, avg_humidity, df = compute_averages(data)
    if df.empty:
        print("❌ No valid data for computation.")
        return

    generate_plot(df)

    print(f"📊 Average Temperature (Past 7 Days): {avg_temp:.2f}°C")
    print(f"📊 Average Humidity (Past 7 Days): {avg_humidity:.2f}%")
    print(f"📈 Temperature plot saved in: {PLOT_FILE}")

# 🔹 Schedule the job to run daily at 8:00 AM
schedule.every().day.at("08:00").do(fetch_and_store_weather_data)

# 🔹 Keep the script running
if __name__ == "__main__":
    print("📡 Weather Data Script Running...")
    
    # Run initial fetch
    fetch_and_store_weather_data()
    
    # Run analysis
    analyze_weather_data()
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check for scheduled jobs every 60 seconds

