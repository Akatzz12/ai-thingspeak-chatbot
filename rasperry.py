import time
import board
import busio
import adafruit_bmp280
import requests

# Setup I2C and BMP280
i2c = busio.I2C(board.SCL, board.SDA)
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76)

# Read sensor data
temp_c = bmp280.temperature
temp_f = (temp_c * 9 / 5) + 32

# ThingSpeak API parameters
THINGSPEAK_API_KEY = 'Your ThingSpeak API Key'
THINGSPEAK_URL = 'https://api.thingspeak.com/update'

# Data payload
payload = {
    'api_key': THINGSPEAK_API_KEY,
    'field1': temp_f
}

# Send the data to ThingSpeak
try:
    response = requests.post(THINGSPEAK_URL, data=payload, timeout=5)
    if response.status_code == 200 and response.text != '0':
        print("Data sent to ThingSpeak successfully!")
    else:
        print("Failed to send data. Response:", response.text)
except requests.exceptions.RequestException as e:
    print("Error sending data:", e)
 