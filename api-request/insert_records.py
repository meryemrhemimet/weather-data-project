
import os
import psycopg2
from api_request import fetch_data


def connect_to_db():
    print("Connecting to the database...")

    try:
        conn = psycopg2.connect(
            host=os.environ["POSTGRES_HOST"],
            port=os.environ["POSTGRES_PORT"],
            dbname=os.environ["POSTGRES_DB"],
            user=os.environ["POSTGRES_USER"],
            password=os.environ["POSTGRES_PASSWORD"]
        )
        return conn

    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        raise


def create_table(conn):
    print("Creating table...")

    try:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE SCHEMA IF NOT EXISTS dev;

            CREATE TABLE IF NOT EXISTS dev.raw_weather_data (
                id SERIAL PRIMARY KEY,
                city TEXT,
                country TEXT,
                temperature FLOAT,
                weather_description TEXT,
                wind_speed FLOAT,
                time TIMESTAMP,
                inserted_at TIMESTAMP DEFAULT now(),
                utc_offset TEXT
            );
        """)

        conn.commit()
        cursor.close()

        print("Table created successfully.")

    except psycopg2.Error as e:
        print(f"Table creation error: {e}")
        raise


def get_weather_description(code):
    descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Freezing drizzle",
        57: "Freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Freezing rain",
        67: "Freezing rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Thunderstorm with heavy hail"
    }

    return descriptions.get(code, "Unknown weather")


def insert_records(conn, data):
    print("Inserting hourly weather records...")

    try:
        cursor = conn.cursor()

        hourly = data["hourly"]
        times = hourly["time"]

        for i in range(len(times)):

            # Avoid inserting the same hourly observation twice
            cursor.execute("""
                DELETE FROM dev.raw_weather_data
                WHERE city = %s AND time = %s
            """, ("Rabat", times[i]))

            cursor.execute("""
                INSERT INTO dev.raw_weather_data
                (
                    city,
                    country,
                    temperature,
                    weather_description,
                    wind_speed,
                    time,
                    inserted_at,
                    utc_offset
                )
                VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s)
            """, (
                "Rabat",
                "Morocco",
                hourly["temperature_2m"][i],
                get_weather_description(hourly["weather_code"][i]),
                hourly["wind_speed_10m"][i],
                times[i],
                str(data["utc_offset_seconds"] / 3600)
            ))

        conn.commit()
        cursor.close()

        print(f"Successfully inserted {len(times)} hourly records for Rabat.")

    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error inserting records: {e}")
        raise


def main():
    conn = None

    try:
        data = fetch_data()

        conn = connect_to_db()

        create_table(conn)

        insert_records(conn, data)

    except Exception as e:
        print(f"An error occurred: {e}")
        raise

    finally:
        if conn:
            conn.close()
            print("Database connection closed.")


if __name__ == "__main__":
    main()
