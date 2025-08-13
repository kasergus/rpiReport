import bit
import sound

INT = [0, 0]
TEXT = [0, 1]
AUDIO = [1, 0]

def encodeInt(dec):
  encoded = INT + bit.intToBinMas(dec)
  return encoded

def decodeInt(binMas):
  if getInfoBits(binMas) != INT:
    raise TypeError("Can't decode data as integer.")

  rawBinMas = rmInfoBits(binMas)
  decoded = bit.binMasToInt(rawBinMas)
  return decoded

def encodeText(text):
  dec = bit.textToInt(text)
  encoded = TEXT + bit.intToBinMas(dec)
  return encoded

def decodeText(binMas):
  if getInfoBits(binMas) != TEXT:
    raise TypeError("Can't decode data as text.")

  rawBinMas = rmInfoBits(binMas)
  textDec = bit.binMasToInt(rawBinMas)
  decoded = bit.intToText(textDec)
  return decoded

def encodeTextedAudio(noteText):
  noteDec = bit.textToInt(noteText)
  encoded = AUDIO + bit.intToBinMas(noteDec)
  return encoded

def encodeAudio(notesList):
  noteText = bit.audioToText(notesList)
  return encodeTextedAudio(noteText)

def decodeAudio(binMas):
  if getInfoBits(binMas) != AUDIO:
    raise TypeError("Can't decode data as audio.")

  rawBinMas = rmInfoBits(binMas)
  textDec = bit.binMasToInt(rawBinMas)
  noteText = bit.intToText(textDec)

  decoded = bit.textToAudio(noteText)
  return decoded

def decode(binMas):
  decodedType = {str(INT): decodeInt, str(TEXT): decodeText, str(AUDIO): decodeAudio}
  infoBits = getInfoBits(binMas)
  if (infoBits not in [INT, TEXT, AUDIO]):
    raise TypeError("Unkown data type")
  return decodedType[str(infoBits)](binMas)

def getType(binMas):
  types = {str(INT): "int", str(TEXT): "text", str(AUDIO): "audio"}
  return types[str(getInfoBits(binMas))]

def rmInfoBits(binMas):
  return binMas[2:]

def getInfoBits(binMas):
  return binMas[0:2]
