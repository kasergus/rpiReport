import time as t

def intToBin(dec):
  revBin = 1
  while dec > 0:
    rest = dec % 2
    dec //= 2
    revBin = revBin * 10 + rest

  bin = 0
  while revBin > 1:
    bit = revBin % 10
    revBin //= 10
    bin = bin * 10 + bit
  return bin

def intToBinMas(dec):
  mas = []
  bin = intToBin(dec)
  if not bin:
    return [0]

  while bin >= 1:
    bit = bin % 10
    bin //= 10
    mas.append(bit)

  return mas[::-1]

def binMasToInt(binMas):
  dec = 0
  binPower = 0
  index = len(binMas) - 1
  while index >= 0:
    bit = binMas[index]
    dec += bit * 2 ** binPower
    index -= 1
    binPower += 1
  return dec

def textToInt(string):
  integer = 0;
  for char in string:
    integer = integer * 1000 + ord(char)
  return integer

def intToText(integer):
  mas = []
  while integer > 0:
    charCode = integer % 1000
    char = chr(charCode)
    integer //= 1000
    mas.append(char)
  return str(''.join(mas[::-1]))

def audioToText(noteList):
  noteText = ""
  iterList = noteList[:-1]
  for note, duration in iterList:
    noteText += note + "-" + str(duration) + "|"
  noteText += noteList[-1][0] + "-" + str(noteList[-1][1])
  return noteText

def textToAudio(noteText):
  noteMas = noteText.split("|")
  noteList = []
  for element in noteMas:
    note, duration = element.split("-")
    duration = int(duration)
    noteList.append((note, duration))
  return noteList

def send(binMas, led):
  for bit in binMas:
    led.on()
    if bit == 1:
      t.sleep(0.3)
      led.off()
      t.sleep(0.1)
    elif bit == 0:
      t.sleep(0.1)
      led.off()
      t.sleep(0.3)
    t.sleep(0.2)

def receive(receiver):
  binMas = []
  inform = True
  lastTime = -1
  while True:
    if receiver.value():
      t.sleep(0.2)
      if receiver.value():
        binMas.append(1)
      elif not receiver.value():
        binMas.append(0)
      t.sleep(0.2)
      lastTime = t.time()
      print(binMas)
    elif not receiver.value() and lastTime != -1 and t.time() - lastTime > 5:
      break

  return binMas
