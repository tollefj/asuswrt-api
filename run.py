from win32com.client import Dispatch
import sys
import flask
from flask import request, jsonify
from speech import TTS
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

from router_config import AsusRouter
from hue import Hue
from speech import TTS

import time

tts = TTS()

from enum import IntEnum

class Signal(IntEnum):
  GOOD = 50
  DECENT = 55
  OK = 62
  WEAK = 70
  NOT_HOME = 80

try:
  router = AsusRouter()
  print([c.name.lower() for c in router.clients()])

  hue_ip = router.find_client('hue').ip
  hue = Hue(hue_ip)
  print('Hue bridge connected on ip', hue_ip)

except Exception as e:
  print(e)
  print('No hue bridge found, exiting...')
  sys.exit(0)

app = flask.Flask(__name__)
GET = ['GET']
POST = ['POST']

@app.route('/', methods=GET)
def root():
  print(request.query_string)
  print(request.args)
  arg = request.args
  print(arg['name'])
  return request.query_string
  
@app.route('/clients/', methods=GET)
def clients():
  return jsonify([c.values() for c in router.clients()])

@app.route('/client/<name>', methods=GET)
def client(name=""):
  return jsonify(router.find_client(name))


@app.route('/rooms/', methods=GET)
def rooms():
  return jsonify(hue.get_rooms_with_lights())

@app.route('/room/<room_id>', methods=GET)
def room_lights(room_id=1):
  return jsonify(hue.get_lights_in_room_by_name(int(room_id)))
  return jsonify("ok")

if __name__ == '__main__':
  phones = ['Kristinone11Pro', 'Kristinplewatch', 'Tollefphone']

  def someone_home():
    active_phones = [router.is_on_wifi(phone) for phone in phones]
    return any(active_phones)
  
  def bridge_scheduler(hue):
    tollef = router.is_on_wifi('Tollefphone')
    kristine = router.is_on_wifi('Kristinone11Pro')

    if tollef:
      hue.toggle_room(1, True)
      hue.toggle_room(7, True)
    elif tollef or kristine:
      hue.toggle_all_groups(True)
    else:
      hue.toggle_all_groups(False)
    
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

  def wifi_signal(phone, strength=Signal.OK, *rooms):
    client = router.find_client(phone)
    if client:
      rssi = abs(int(client.rssi))
      print('{}: {}dbm'.format(phone, rssi))
      for room in rooms:
        hue.rssi(room, rssi, strength)
    else:
      for room in rooms:
        hue.toggle_room(room, False)

  kontor = hue.find_room('kontor')
  stua = hue.find_room('stu')
  kjokken = hue.find_room('kjøkken')

  def tollef_in_office():
    wifi_signal('tollefphone', Signal.GOOD, kontor)

  def kristine_is_somewhere():
    wifi_signal('11pro', Signal.DECENT, stua)

  scheduler = BackgroundScheduler()
  try:
    # scheduler.add_job(func=tollef_in_office, trigger='interval', seconds=2, id='1')
    # scheduler.add_job(func=kristine_is_somewhere, trigger='interval', seconds=3, id='2')

    scheduler.start()

    atexit.register(lambda: scheduler.shutdown())
  except:
    print('Toggler not found')

  app.run(debug=False)