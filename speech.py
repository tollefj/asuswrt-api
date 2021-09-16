import pyttsx3

class TTS:
  def __init__(self, rate=180, volume=1.0, gender='female'):
    self.rate = rate
    self.volume = volume
    self.gender = gender

    self.engine = pyttsx3.init()
    self.engine.setProperty('rate', self.rate)
    self.engine.setProperty('volume', self.volume)

    voices = self.engine.getProperty('voices')
    gender_idx = 1 if self.gender == 'female' else 0
    self.engine.setProperty('voice', voices[gender_idx].id)
  
  def get_engine(self):
    return self.engine
  
  def say(self, s):
    self.engine.say(s)
    self.engine.runAndWait()
    self.engine.stop()
  