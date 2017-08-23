import requests

class PacbotState:
    def __init__(self, host):
        self.STOPPED = 0 
        self.POWER = 1
        self.REGULAR = 2 
        self.inky = (-1,-1) # (x,y) coordinates
        self.blinky = (-1,-1) # (x,y) coordinates
        self.pinky = (-1,-1) # (x,y) coordinates
        self.clyde = (-1,-1) # (x,y) coordinates
        self.pacbot = (-1,-1) # (x,y) coordinates 
        self.state = self.STOPPED
        self.powerCounter = 0
        self.host = host

    def poll(self):
        return
        resp = requests.get('{}/pac-bot'.format(host))

        if 'stop' in resp.json():
            self.state = self.STOPPED
            return
        
        self.blinky[0] = int(resp.json()['ghost1']['x'])
        self.blinky[1] = int(resp.json()['ghost1']['y'])
        self.pinky[0] = int(resp.json()['ghost2']['x'])
        self.pinky[1] = int(resp.json()['ghost2']['y'])
        self.clyde[0] = int(resp.json()['ghost3']['x'])
        self.clyde[1] = int(resp.json()['ghost3']['y'])
        self.inky[0] = int(resp.json()['ghost4']['x'])
        self.inky[1] = int(resp.json()['ghost4']['y'])
        self.pacbot[0] = int(resp.json()['pacbot']['x'])
        self.pacbot[1] = int(resp.json()['pacbot']['y'])
        if 'specialTimer' in resp.json():
            self.powerCounter = int(resp.json()['sepcialTimer'])
            self.state = self.POWER
        else:
            self.state = self.REGULAR
