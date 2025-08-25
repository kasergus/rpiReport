import gpiozero as g
import dencode as dn
import bit
import requests
from time import sleep


url = "http://localhost:8080/rpitopic"

# Binding encoding function for appropriate data type
encodeType = {"int": dn.encodeInt, "text": dn.encodeText, "audio": dn.encodeTextedAudio}

currentState = -1  # state will be swaped every time when new message is posted
infoLed = g.LED(17)  # information LED for sending
statusLed = g.LED(18)  # status LED turns on when sender is sending information

# Main cycle
infoLed.off()
while True:
  # Sending request and formatting response
  response = requests.post(url, json={"model": "RPi5"}, headers={"Content-Type": "application/json"})
  data = response.json()
  succeed = data["succeed"]

  statusLed.off()
  # Checking if response was succeed and if state of RPi and topic are different
  if succeed and (posting := data["posting"]) != currentState:
    # If current state is -1, then RPi was recently turned on, so
    # we are synchronizing stages and sending cycle to the next iteration
    if (currentState == -1):
      currentState = posting
      continue
    # Turning on status led, because information was earned
    statusLed.on()
    # Encoding information based on its type
    msgType = data["msg_type"]
    msgContent = data["msg_content"]
    if msgType == "int":
      msgContent = int(msgContent)
    encoded = encodeType[msgType](msgContent)
    # Sending encoded information
    bit.send(encoded, infoLed)
    # synchronizing state with topic
    currentState = posting
  elif not succeed:
    print("[!] Error: something went wrong (are you assigned this model to topic?)")
  sleep(1)


# # Example of initializing multiple RPi models
# models = [ "lamp", "space", "hedgehog", "dust", "mirror", "water", "key", "spring", "flute", "path" ]
# for model in models:
#   response = requests.post(url, json={"model": model}, headers=headers)
#   print(response.text)
#   response.close()

# # Example of initializing one RPi model
# response = requests.post(url, json={"model": "picow"}, headers=headers)
# print(response.json())
# response.close()


# # Just example of how song must be written
# megalovania = [
#   ("C", 100), ("C", 100), ("B", 100), ("_", 50),
#   ("A", 100), ("_", 50),
#   ("_", 50), ("G#", 100),("_", 50),
#   ("G", 100), ("_", 50), ("F", 200),
#   ("D", 100), ("F", 100), ("G", 100)
# ]
