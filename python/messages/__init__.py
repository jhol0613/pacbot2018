from enum import Enum
from .lightState_pb2 import LightState
from .ultrasonicArray_pb2 import UltrasonicArray

class MsgType(Enum):
    LIGHT_STATE = 0
    MOCK_MSG = 1
    ULTRASONIC_ARRAY = 2

message_buffers = {
    MsgType.LIGHT_STATE: LightState,
    MsgType.ULTRASONIC_ARRAY: UltrasonicArray
}


__all__ = ['MsgType', 'message_buffers', 'LightState', 'UltrasonicArray']
