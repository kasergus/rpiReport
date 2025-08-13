from time import sleep

def play(notesList, snd, volume=40000):
  snd.duty_u16(volume)
  for note, duration in notesList:
    snd.freq(notes[note])
    sleep(duration / 1000)
    snd.freq(notes["_"])
    sleep(0.05)
  snd.duty_u16(0)

notes = {
  "C": 2093,
  "C#": 2217,
  "D": 2349,
  "D#": 2489,
  "E": 2637,
  "F": 2793,
  "F#": 2960,
  "G": 3136,
  "G#": 3332,
  "A": 3440,
  "B": 3729,
  "H": 3951,
  "_": 20000
}
