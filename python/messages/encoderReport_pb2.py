# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: encoderReport.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='encoderReport.proto',
  package='gamePlayer',
  syntax='proto2',
  serialized_pb=_b('\n\x13\x65ncoderReport.proto\x12\ngamePlayer\",\n\rEncoderReport\x12\x0c\n\x04left\x18\x01 \x02(\x05\x12\r\n\x05right\x18\x02 \x02(\x05')
)




_ENCODERREPORT = _descriptor.Descriptor(
  name='EncoderReport',
  full_name='gamePlayer.EncoderReport',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='left', full_name='gamePlayer.EncoderReport.left', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='right', full_name='gamePlayer.EncoderReport.right', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=35,
  serialized_end=79,
)

DESCRIPTOR.message_types_by_name['EncoderReport'] = _ENCODERREPORT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

EncoderReport = _reflection.GeneratedProtocolMessageType('EncoderReport', (_message.Message,), dict(
  DESCRIPTOR = _ENCODERREPORT,
  __module__ = 'encoderReport_pb2'
  # @@protoc_insertion_point(class_scope:gamePlayer.EncoderReport)
  ))
_sym_db.RegisterMessage(EncoderReport)


# @@protoc_insertion_point(module_scope)