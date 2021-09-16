import sys
import yaml

class Config:
  def __init__(self):
    with open("config.yml", "r") as config_file:
      try:
        self.config = yaml.safe_load(config_file)
      except yaml.YAMLError as ex:
        print(ex)
        sys.exit(0)

    if not self.config:
      print("No config file found. Does 'config.yml' exist?")
      sys.exit(0)

  def get(self, key, subkey):
    if subkey:
      return self.config.get(key).get(subkey)
    else:
      return self.config.get(key)