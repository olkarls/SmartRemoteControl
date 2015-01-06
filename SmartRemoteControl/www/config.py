import os
import json

# Change to directory of script so relative file references work.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Name of configuration file.
DATA_FILE_NAME = 'commands.json'

def get_commands():
  data = None

  with open(DATA_FILE_NAME) as data_file:
    data = json.load(data_file)
  return data