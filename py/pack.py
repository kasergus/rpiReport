import bit as b

def removeLast(mas):
  return mas[:-1]

def pack(binMas):
  packed = b""
  eightBits = []
  for bit in binMas:
    eightBits.append(bit)
    if len(eightBits) == 8:
      byteInt = b.binMasToInt(eightBits)
      byte = bytes([byteInt])
      packed += byte
      eightBits = []

  if len(eightBits):
    byte = b.binMasToInt(eightBits)
    packed += bytes([byte])
    eightBits = []

  return packed.hex()

def unpack(byteMas):
  bitMas = []
  for byte in removeLast(byteMas):
    currentByte = b.intToBinMas(byte)
    eightBits = [0] * (8 - len(currentByte)) + currentByte
    bitMas += eightBits
  lastByte = byteMas[-1]
  restBits = b.intToBinMas(lastByte)
  bitMas += restBits
  return bitMas
