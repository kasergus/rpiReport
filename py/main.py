from machine import Pin, PWM
import time as t
import dencode as dn
import bit
import sound
import nw
import urequests as requests
from pack import pack, unpack


def showInt(num, led=Pin(16, Pin.OUT)):
  for n in range(num):
    led.on()
    t.sleep(0.2)
    led.off()
    t.sleep(0.2)

def showText(text):
  file = open("texts.txt", 'w')
  file.write(text)
  file.close()

def showAudio(audio, noise=PWM(Pin(15))):
  sound.play(audio, noise)

ssid = "Tele2_F6FDB6"
password = "fcbvdu7t"

print(nw.connect(ssid, password))

element = Pin(14, Pin.IN, Pin.PULL_DOWN)
noise = PWM(Pin(15))
numberLed = Pin(16, Pin.OUT)

megalovania = [
  ("C", 100), ("C", 100), ("B", 100), ("_", 50),
  ("A", 100), ("_", 50),
  ("_", 50), ("G#", 100),("_", 50),
  ("G", 100), ("_", 50), ("F", 200),
  ("D", 100), ("F", 100), ("G", 100)
]

encoded = dn.encodeAudio(megalovania)
packed = pack(encoded)

url = "https://keyboards-cleveland-fantastic-zoning.trycloudflare.com/rpitopic"
headers = {"Content-Type": "application/json"}


while True:
  decodeType = {"int": showInt, "text": showText, "audio": showAudio}
  print("[#] Success before receive")
  binMas = bit.receive(element)
  print("[#] Success after receive")
  decodedMsg = dn.decode(binMas)
  decodedMsgType = dn.getType(binMas)
  decodeType[decodedMsgType](decodedMsg)
