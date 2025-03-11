from opcua import Server
import mysql.connector
import adafruit_dht
import board
import time

# Initialize AM2301 sensor (connected to GPIO4, modify if needed)
dht_device = adafruit_dht.DHT22(board.D4)

# Connect to MariaDB
db = mysql.connector.connect(
    host="192.168.4.3",
    user="zohaib",
    password="opcuaserver",
    database="opcua_test_db"
)

cursor = db.cursor()

# Create OPC UA Server
server = Server()
server.set_endpoint("opc.tcp://192.168.4.3:4840/freeopcua/server/")
uri = "http://example.org/freeopcua"
idx = server.register_namespace(uri)

# Create OPC UA Object and Variables
obj = server.nodes.objects.add_object(idx, "MyObject")
temp_var = obj.add_variable(idx, "temperatura", 0.0)  # Temperature variable
temp_var.set_writable()
humidity_var = obj.add_variable(idx, "humedad", 0.0)  # Humidity variable
humidity_var.set_writable()

# Start Server
server.start()
print("OPC UA Server started at opc.tcp://192.168.4.3:4840/freeopcua/server/")

try:
    while True:
        try:
            # Read temperature and humidity from AM2301
            temperature = dht_device.temperature
            humidity = dht_device.humidity

            if temperature is not None and humidity is not None:
                print(f"Temperature: {temperature}°C, Humidity: {humidity}%")

                # Update OPC UA variables
                temp_var.set_value(temperature)
                humidity_var.set_value(humidity)

                # Store Data in MariaDB
                sql = "INSERT INTO sensor_data (temperatura, humedad) VALUES (%s, %s)"
                cursor.execute(sql, (temperature, humidity))
                db.commit()

        except RuntimeError as e:
            print(f"Sensor error: {e}")

        time.sleep(2)  # Delay to prevent sensor overheating

except KeyboardInterrupt:
    server.stop()
    cursor.close()
    db.close()
    print("Server stopped.")
