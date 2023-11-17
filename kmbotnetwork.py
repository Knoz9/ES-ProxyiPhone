import socket
import threading
import time
import paho.mqtt.client as mqtt
import kmbotos as kmos

uplink_lock = threading.Lock()

ADAFRUIT_IO_USERNAME = ""
ADAFRUIT_IO_KEY = ()
broker = "io.adafruit.com"
port = 1883


def is_connected():
    s = None
    try:
        # Try to establish a socket connection to Google's public DNS server
        s = socket.create_connection(("8.8.8.8", 53), timeout=1)
        return True
    except OSError:
        pass
    finally:
        if s:
            s.close()
    return False


def is_connected_stably():
    if is_connected():
        time.sleep(1)
        if is_connected():
            time.sleep(1)
            if is_connected():
                return True
    return False


def uplink_safe(data, topic):
    with uplink_lock:
        # Existing uplink logic here
        uplink(data, topic)


def on_connect(client, userdata, flags, rc):
    if rc != 0:
        print(f"Failed to connect, return code {rc}")


def on_publish(client, userdata, mid):
    print("Toggled Airplane flag!")


def uplink(text, topic):
    MAX_RETRIES = 5
    retries = 0

    while retries < MAX_RETRIES:
        try:
            client = mqtt.Client(client_id="69")
            client.on_connect = on_connect
            if topic == "ddd":
                client.on_publish = on_publish
            client.username_pw_set(ADAFRUIT_IO_USERNAME, password=ADAFRUIT_IO_KEY)
            client.connect(broker, port)
            client.loop_start()
            client.publish(f"{ADAFRUIT_IO_USERNAME}/feeds/{topic}", payload=text)
            time.sleep(1)  # Give it some time to publish
            client.loop_stop()
            client.disconnect()
            return  # Exit the function if uplink succeeds
        except Exception as e:
            retries += 1
            print(f"Uplink failed! Attempt {retries} of {MAX_RETRIES}. Error: {e}")
            time.sleep(3)
            client.disconnect()

    # If the function has failed 5 times, then restart the program.
    kmos.restart_program()
