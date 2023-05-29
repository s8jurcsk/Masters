import sqlite3
from datetime import datetime

con = sqlite3.connect("timedata.db")
cur = con.cursor()

# Create tables for camera1 and camera2
cur.execute('''CREATE TABLE IF NOT EXISTS CameraOneMonitors (
                    timestamp TEXT,
                    monitor TEXT,
                    on_person INTEGER,
                    on_no_person INTEGER,
                    off_person INTEGER
                )''')

cur.execute('''CREATE TABLE IF NOT EXISTS CameraTwoMonitors (
                    timestamp TEXT,
                    monitor TEXT,
                    on_person INTEGER,
                    on_no_person INTEGER,
                    off_person INTEGER
                )''')

#cur.execute("DELETE FROM CameraOneMonitors")
#cur.execute("DELETE FROM CameraTwoMonitors")
#con.commit()


# Select data from CameraOneMonitors table
cur.execute("SELECT * FROM CameraOneMonitors")
rows = cur.fetchall()
# Print the selected data with column names
print('Camera 1')
print("{:<20} {:<10} {:<10} {:<15} {:<10}".format("Timestamp", "Monitor", "On Person", "On No Person", "Off Person"))
for row in rows:
    print("{:<20} {:<10} {:<10} {:<15} {:<10}".format(row[0], row[1], row[2], row[3], row[4]))

# Select data from CameraTwoMonitors table
cur.execute("SELECT * FROM CameraTwoMonitors")
rows = cur.fetchall()
# Print the selected data with column names
print('Camera 2')
print("{:<20} {:<10} {:<10} {:<15} {:<10}".format("Timestamp", "Monitor", "On Person", "On No Person", "Off Person"))
for row in rows:
    print("{:<20} {:<10} {:<10} {:<15} {:<10}".format(row[0], row[1], row[2], row[3], row[4]))


# Close the database connection
con.close()


