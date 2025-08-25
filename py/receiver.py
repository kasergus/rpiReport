from machine import Pin, PWM
import dencode as dn
import bit
import sound
import time as t


# showInt: blinks the led num amount of times
def showInt(num, led=Pin(16, Pin.OUT)):
  for n in range(num):
    led.on()
    t.sleep(0.2)
    led.off()
    t.sleep(0.2)

# showText: writes text to file
def showText(text):
  file = open("texts.txt", 'w')
  file.write(text)
  file.close()

# showAudio: plays audio
def showAudio(audio, noise=PWM(Pin(15))):
  sound.play(audio, noise)


element = Pin(14, Pin.IN, Pin.PULL_DOWN)  # photo resistor for receiving information (read report)
noise = PWM(Pin(15))  # buzzer for play melodies
numberLed = Pin(16, Pin.OUT)  # led to display number

# binding display function to appropriate information type
showMsg = {"int": showInt, "text": showText, "audio": showAudio}

# Main cycle
while True:
  binMas = bit.receive(element)
  # Decoding received information based on its type and showing it (based on its type)
  decodedMsg = dn.decode(binMas)
  print("received information: ")
  print(decodedMsg)
  decodedMsgType = dn.getType(binMas)
  showMsg[decodedMsgType](decodedMsg)
