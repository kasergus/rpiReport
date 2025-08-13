import network, machine
from time import sleep

wlan = network.WLAN()

def connect(ssid, password):
  wlan.active(True)
  wlan.connect(ssid, password)
  while not wlan.isconnected():
    print("[#]")
    sleep(1)
  return wlan.ipconfig("addr4")
