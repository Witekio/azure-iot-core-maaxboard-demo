import os
import time
from pin import Pin
from azure.iot.device import IoTHubDeviceClient

conn_str = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")
device_client = IoTHubDeviceClient.create_from_connection_string(STRING)

PIN_NUMBER = '11' # REPLACE WITH YOUR PIN NUMBER if different
configured_pin = Pin(PIN_NUMBER)

# Connect the IoTHub client
device_client.connect()

# Get the device twin document
twin = device_client.get_twin()
print("Initial twin document:")
print("{}".format(twin))


def report_light_state(state):
    reported_properties = {"light": state}
    print("Setting reported light state to {}".format(reported_properties["light"]))
    device_client.patch_twin_reported_properties(reported_properties)

# Initalize the light as off in reported properties:
report_light_state("OFF")


while True:
    request = input('Enter ON, OFF, or CLEAR: ')
    if request == "CLEAR":
        pin.tear_down()
        report_light_state("OFF")
        device_client.disconnect()
        break
    if request == "OFF":
        pin.turn_off()
        report_light_state("OFF")
    if request == "ON":
        pin.turn_on()
        report_light_state("ON")
