import gpiozero as g
import dencode as dn
import bit
import requests
from time import sleep

megalovania = [
  ("C", 100), ("C", 100), ("B", 100), ("_", 50),
  ("A", 100), ("_", 50),
  ("_", 50), ("G#", 100),("_", 50),
  ("G", 100), ("_", 50), ("F", 200),
  ("D", 100), ("F", 100), ("G", 100)
]

url = "http://localhost:8080/rpitopic"
# url = "https://miss-insured-sheep-bargains.trycloudflare.com/rpitopic"

encodeType = {"int": dn.encodeInt, "text": dn.encodeText, "audio": dn.encodeTextedAudio}

currentState = -1
infoLed = g.LED(17)
statusLed = g.LED(18)
encoded = dn.encodeAudio(megalovania)


infoLed.off()
# infoLed.on()
while True:
  response = requests.post(url, json={"model": "RPi5"}, headers={"Content-Type": "application/json"})
  data = response.json()
  succeed = data["succeed"]

  statusLed.off()
  if succeed and (posting := data["posting"]) != currentState:
    if (currentState == -1):
      currentState = posting
      continue
    print("Information earned")
    statusLed.on()
    msgType = data["msg_type"]
    msgContent = data["msg_content"]
    if msgType == "int":
      msgContent = int(msgContent)
    encoded = encodeType[msgType](msgContent)
    print("encoded =", encoded)
    bit.send(encoded, infoLed)
    currentState = posting
  elif not succeed:
    print("[!] Error: something went wrong (are you assigned this model to topic?)")
  sleep(1)

# Example of initializing multiple models
# models = [ "lamp", "space", "hedgehog", "dust", "mirror", "water", "key", "spring", "flute", "path" ]
# for model in models:
#   response = requests.post(url, json={"model": model}, headers=headers)
#   print(response.text)
#   response.close()

# Example of initializing one model
# response = requests.post(url, json={"model": "picow"}, headers=headers)
# print(response.json())
# response.close()
