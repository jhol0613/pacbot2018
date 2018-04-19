
import robomodules
import os
from messages import MsgType

ADDRESS = os.environ.get("BIND_ADDRESS","localhost")
PORT = os.environ.get("BIND_PORT", 8080)

def main():
    #print("Address: ", ADDRESS)
    # print("Port: ", PORT)
    server = robomodules.Server(ADDRESS, PORT, MsgType)
    server.run()

if __name__ == "__main__":
    main()