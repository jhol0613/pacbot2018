# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: twist.proto

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
  name='twist.proto',
  package='gamePlayer',
  syntax='proto2',
  serialized_pb=_b('\n\x0btwist.proto\x12\ngamePlayer\"(\n\x05Twist\x12\x10\n\x08velocity\x18\x01 \x02(\x05\x12\r\n\x05omega\x18\x02 \x02(\x05')
)




_TWIST = _descriptor.Descriptor(
  name='Twist',
  full_name='gamePlayer.Twist',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='velocity', full_name='gamePlayer.Twist.velocity', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='omega', full_name='gamePlayer.Twist.omega', index=1,
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
  serialized_start=27,
  serialized_end=67,
)

DESCRIPTOR.message_types_by_name['Twist'] = _TWIST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Twist = _reflection.GeneratedProtocolMessageType('Twist', (_message.Message,), dict(
  DESCRIPTOR = _TWIST,
  __module__ = 'twist_pb2'
  # @@protoc_insertion_point(class_scope:gamePlayer.Twist)
  ))
_sym_db.RegisterMessage(Twist)


# @@protoc_insertion_point(module_scope)
