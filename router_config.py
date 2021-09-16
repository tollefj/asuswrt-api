from config_loader import Config
from asuswrt import AsusWRT

class AsusRouter:
  def __init__(self):
    self.last_clients = []
    self.config = Config()
    self.init_router()
    self.show_info()

  def init_router(self):
    self.router = AsusWRT(
      url=self.config.get('router', 'url'),
      username=self.config.get('admin', 'id'),
      password=self.config.get('admin', 'pw'))
    
  def show_info(self):
    sys = self.router.get_sys_info()
    print('Model: %s' % sys['model'])
    print('Firmware: %s' % sys['firmware'])


  def clients(self):
    return self.router.get_online_clients()

  def show_clients(self):
    for client in self.clients():
      print(client)
    
  def find_client(self, name):
    for client in self.clients():
      if name.lower() in client.name.lower():
        return client
    return None

  def is_on_wifi(self, name):
    client = self.find_client(name)
    if client != None:
      on_wifi = 'GHz' in client.interface
      if on_wifi:
        print('{} connected'.format(client.name))
        return True
      else:
        print('{} disconnected'.format(client.name))
        return False
    return False

  def get_client_diff(self):
    _old = self.last_clients
    _new = self.clients()
    diff = [c['name'] for c in _new if c not in _old]
    self.last_clients = _new
    return diff

  def get_router(self):
    return self.router
