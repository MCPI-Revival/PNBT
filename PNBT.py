import struct
import os

tag = {
    "end": 0,
    "byte": 1,
    "short": 2,
    "int": 3,
    "long": 4,
    "float": 5,
    "double": 6,
    "byte_array": 7,
    "string": 8,
    "list": 9,
    "compound": 10,
    "int_array": 11,
    "long_array": 12
}

stream = {
    "data": b"",
    "offset": 0
}

nbt = {}
endianess = "<"

def read_stream(length):
    stream["offset"] += length
    return stream["data"][offset - length:offset]

def read_type(nbt_type):
    if nbt_type == tag["byte"]:
        tag_value = struct.unpack("b", read_stream(1))[0]
        nbt[tag_name] = {"type": tag_type, "value": tag_value}
    elif nbt_type == tag["short"]:
        tag_value = struct.unpack(endianess + "h", read_stream(2))[0]
        nbt[tag_name] = {"type": tag_type, "value": tag_value}
    elif nbt_type == tag["int"]:
        tag_value = struct.unpack(endianess + "l", read_stream(4))[0]
        nbt[tag_name] = {"type": tag_type, "value": tag_value}
    elif nbt_type == tag["long"]:
        tag_value = struct.unpack(endianess + "q", read_stream(8))[0]
        nbt[tag_name] = {"type": tag_type, "value": tag_value}
    elif nbt_type == tag["float"]:
        tag_value = struct.unpack(endianess + "f", read_stream(4))[0]
        nbt[tag_name] = {"type": tag_type, "value": tag_value}
    elif nbt_type == tag["double"]:
        tag_value = struct.unpack(endianess + "d", read_stream(8))[0]
        nbt[tag_name] = {"type": tag_type, "value": tag_value}
    elif nbt_type == tag["byte_array"]:
        byte_count = struct.unpack(endianess + "l", read_stream(4))[0]
        tag_value = []
        for i in range(0, byte_count):
            tag_value.append(struct.unpack("b", read_stream(1))[0])
        nbt[tag_name] = {"type": tag_type, "value": tag_value}
    elif nbt_type == tag["string"]:
        string_length = struct.unpack(endianess + "H", read_stream(2))[0]
        tag_value = read_stream(string_length)
        nbt[tag_name] = {"type": tag_type, "value": tag_value}
