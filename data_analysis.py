import psycopg2
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

# Configure the connection
def create_connection():
    return psycopg2.connect(
        host="localhost",
        port="5433",
        database="weather_forecast",
        user="postgres",
        password="3Dm@rpostgresql"
    )

# Function to fetch weather data for the past 7 days
def fetch_past_week_data():
    connection = create_connection()
    cursor = connection.cursor()
    query = '''
    SELECT city, temperature, humidity, weather_description, timestamp
    FROM weather_data
    WHERE timestamp >= NOW() - INTERVAL '7 days'
    ORDER BY timestamp
    '''
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

# Function to compute average temperature and humidity
def compute_averages(data):
    df = pd.DataFrame(data, columns=['city', 'temperature', 'humidity', 'weather_description', 'timestamp'])
    avg_temp = df['temperature'].mean()
    avg_humidity = df['humidity'].mean()
    return avg_temp, avg_humidity, df

# Function to generate and save plot
def generate_plot(df):
    plt.figure(figsize=(10, 5))
    plt.plot(df['timestamp'], df['temperature'], marker='o', linestyle='-', color='b')
    plt.xlabel('Timestamp')
    plt.ylabel('Temperature (°C)')
    plt.title('Temperature Over Time (Past 7 Days)')
    plt.grid(True)
    plt.savefig('temperature_plot.png')
    plt.close()

# Main function to perform the tasks
def main():
    data = fetch_past_week_data()
    if not data:
        print("No data available for the past 7 days.")
        return

    avg_temp, avg_humidity, df = compute_averages(data)
    generate_plot(df)

    print(f"Average Temperature (Past 7 Days): {avg_temp:.2f}°C")
    print(f"Average Humidity (Past 7 Days): {avg_humidity:.2f}%")
    print("Temperature plot saved as 'temperature_plot.png'.")

if __name__ == "__main__":
    main()