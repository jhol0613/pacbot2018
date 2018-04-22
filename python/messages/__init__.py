from enum import Enum
from .lightState_pb2 import LightState
from .ultrasonicArray_pb2 import UltrasonicArray
from .bumper_pb2 import Bumper
from .twist_pb2 import Twist
from .encoderControl_pb2 import EncoderControl
from .encoderReport_pb2 import EncoderReport

class MsgType(Enum):
    LIGHT_STATE = 0
    ULTRASONIC_ARRAY = 1
    BUMPER = 2
    TWIST = 3
    ENCODER_CONTROL = 4
    ENCODER_REPORT = 5

message_buffers = {
    MsgType.LIGHT_STATE: LightState,
    MsgType.ULTRASONIC_ARRAY: UltrasonicArray,
    MsgType.BUMPER: Bumper,
    MsgType.TWIST: Twist,
    MsgType.ENCODER_CONTROL: EncoderControl,
    MsgType.ENCODER_REPORT: EncoderReport
}


__all__ = ['MsgType', 'message_buffers', 'LightState', 'UltrasonicArray', 'Bumper', 'Twist', 'EncoderControl', 'EncoderReport']
