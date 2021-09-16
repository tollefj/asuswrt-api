from phue import Bridge
from enum import IntEnum


ON = True
OFF = False

def onoff(state):
  return 'ON' if state else 'OFF'

class Hue:
  def __init__(self, ip):
    self.b = Bridge(ip)
    self.rooms = []
    self.lights = {}

    self.init_valid_groups()
    self.update_lights()

  def init_valid_groups(self):
    groups = self.b.get_group()
    valid_names = "Gangen Kjøkken Stua Soverommet Kontoret".split(" ")
    rooms = []
    for group_id, group_data in self.b.get_group().items():
      if group_data['name'] in valid_names:
        rooms.append(int(group_id))

    self.rooms = rooms

  def get_rooms_with_lights(self):
    parsed_rooms = []
    for room in self.rooms:
      parsed_rooms.append({
        'room': [room, self.b.get_group(room, 'name')],
        'lights': self.get_lights_in_room_by_name(room)
      })
    return parsed_rooms

  def find_room(self, name):
    for room in self.rooms:  # list over valid rooms
      if name.lower() in self.b.get_group(room, 'name').lower():
        print('Found room id: {}'.format(room))
        return room
    print('Found no room based on the name: {}'.format(name))
    return None

  def update_lights(self, key='id'):
    self.lights = self.b.get_light_objects(key)
  
  def get_bridge(self):
    return self.b

  def get_lights_in_room_by_name(self, room):
    room_lights = self.b.get_group(room, 'lights')
    print('room', room_lights)
    light_name = lambda l : self.lights[l].name
    light_names = [[l, light_name(int(l))] for l in room_lights]
    return light_names

  def toggle_group(self, group, state):
    print('info for', group,':',self.b.get_group(group, 'lights'))
    self.b.set_group(group, 'on', state)

  def toggle_light(self, light_id, state):
    self.update_lights()
    if self.lights[light_id].on != state:
      self.lights[light_id].on = state
      light_name = self.lights[light_id].name
      print('[{}] is now {}'.format(light_name, onoff(state)))

  def toggle_room(self, room, state):
    room_lights = self.b.get_group(room, 'lights')
    for light in room_lights:
      self.toggle_light(int(light), state)

  def toggle_all_groups(self, state):
    print(self.rooms)
    for room in self.rooms:
      print('room', room)
      self.toggle_room(room, state)

  def rssi(self, room, rssi, strength=50):
    if rssi < strength:
      self.toggle_room(room, ON)
    else:
      self.toggle_room(room, OFF)
    
  def rssi_higher(self, room, rssi, strength=50):
    if rssi > strength:
      self.toggle_room(room, ON)
    else:
      self.toggle_room(room, OFF)