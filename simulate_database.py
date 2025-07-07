import sqlite3
import random
import time
from datetime import datetime, timedelta

# Create database and table
conn = sqlite3.connect('sensor_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS sensor_readings (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
             speed FLOAT,
             rpm INTEGER,
             temp FLOAT,
             tension FLOAT,
             power FLOAT)''')
conn.commit()

def generate_sample_data(num_hours=24, interval_sec=2): 
    """Generate 24 hours of historical data"""
    now = datetime.now()
    start_time = now - timedelta(hours=num_hours)
    
    current = start_time
    while current <= now:
        c.execute('''INSERT INTO sensor_readings (timestamp, speed, rpm, temp, tension, power)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (current.isoformat(),
                   random.randint(0, 120),
                   random.randint(800, 5000),
                   round(random.uniform(60.0, 110.0), 1),
                   round(random.uniform(0.0, 5.0), 4),
                   round(random.uniform(0.0, 100.0), 2)))
        current += timedelta(seconds=interval_sec)
    conn.commit()
    print(f"Generated {num_hours} hours of historical data")

def simulate_real_time_data():
    """Continuously add new readings"""
    print("Simulating real-time sensor data...")
    try:
        while True:
            c.execute('''INSERT INTO sensor_readings (speed, rpm, temp, tension, power)
                         VALUES (?, ?, ?, ?, ?)''',
                      (random.randint(0, 120),
                       random.randint(800, 5000),
                       round(random.uniform(60.0, 110.0), 1),
                       round(random.uniform(0.0, 5.0), 4),
                       round(random.uniform(0.0, 100.0), 2)))
            conn.commit()
            time.sleep(3)  # Add data every 3 seconds
    except KeyboardInterrupt:
        conn.close()

if __name__ == "__main__":
    generate_sample_data()  # Create historical data
    simulate_real_time_data()  # Start real-time simulation