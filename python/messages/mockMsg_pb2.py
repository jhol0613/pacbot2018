# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mockMsg.proto

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
  name='mockMsg.proto',
  package='gamePlayer',
  syntax='proto2',
  serialized_pb=_b('\n\rmockMsg.proto\x12\ngamePlayer\")\n\x07MockMsg\x12\x0e\n\x06xValue\x18\x01 \x02(\x05\x12\x0e\n\x06yValue\x18\x02 \x02(\x05')
)




_MOCKMSG = _descriptor.Descriptor(
  name='MockMsg',
  full_name='gamePlayer.MockMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='xValue', full_name='gamePlayer.MockMsg.xValue', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='yValue', full_name='gamePlayer.MockMsg.yValue', index=1,
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
  serialized_start=29,
  serialized_end=70,
)

DESCRIPTOR.message_types_by_name['MockMsg'] = _MOCKMSG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MockMsg = _reflection.GeneratedProtocolMessageType('MockMsg', (_message.Message,), dict(
  DESCRIPTOR = _MOCKMSG,
  __module__ = 'mockMsg_pb2'
  # @@protoc_insertion_point(class_scope:gamePlayer.MockMsg)
  ))
_sym_db.RegisterMessage(MockMsg)


# @@protoc_insertion_point(module_scope)