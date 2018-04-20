import os
import robomodules as rm
from messages import *

SERVER_ADDRESS = os.environ.get("BIND_ADDRESS","192.168.1.81")
SERVER_PORT = os.environ.get("BIND_PORT", 11297)

LOCAL_ADDRESS = os.environ.get("LOCAL_ADDRESS","localhost")
LOCAL_PORT = os.environ.get("LOCAL_PORT", 11293)

SERVER_FREQUENCY = 0
LOCAL_FREQUENCY = 30

class PacbotServerClient(rm.ProtoModule):
    def __init__(self, addr, port, loop):
        self.subscriptions = [MsgType.LIGHT_STATE]
        super().__init__(addr, port, message_buffers, MsgType, SERVER_FREQUENCY, self.subscriptions, loop)
        self.state = None

    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        # This module will connect to server and receive the game state
        if msg_type == MsgType.LIGHT_STATE:
            self.state = msg

    def tick(self):
        return

    def get_state(self):
        return self.state

class PacbotCommsModule(rm.ProtoModule):
    def __init__(self, server_addr, server_port, local_addr, local_port):
        super().__init__(local_addr, local_port, message_buffers, MsgType, LOCAL_FREQUENCY)
        self.server_module = PacbotServerClient(server_addr, server_port, self.loop)
        self.server_module.connect()

    def msg_received(self, msg, msg_type):
        # This gets called whenever any message is received
        return

    def tick(self):
        # Get state from the server
        state = self.server_module.get_state()
        if state != None:
            # Broadcast state to local modules
            self.write(state.SerializeToString(), MsgType.LIGHT_STATE)

def main():
    module = PacbotCommsModule(SERVER_ADDRESS, SERVER_PORT, LOCAL_ADDRESS, LOCAL_PORT)
    module.run()

if __name__ == "__main__":
    main()