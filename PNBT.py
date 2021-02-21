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

def read_compound_tag():
    tree = {}
    while True:
        tag_type = struct.unpack("B", read_stream(1))[0]
        if tag_type == tag["end"]:
            break
        tag_name = read_type(tag["string"])
        tag_value = read_type(tag_type)
        tree[tag_name] = {"type": tag_type, "value": tag_value}
    return tree
        

def read_type(nbt_type):
    if nbt_type == tag["byte"]:
        return struct.unpack("b", read_stream(1))[0]
    elif nbt_type == tag["short"]:
        return struct.unpack(endianess + "h", read_stream(2))[0]
    elif nbt_type == tag["int"]:
        return struct.unpack(endianess + "l", read_stream(4))[0]
    elif nbt_type == tag["long"]:
        return struct.unpack(endianess + "q", read_stream(8))[0]
    elif nbt_type == tag["float"]:
        return struct.unpack(endianess + "f", read_stream(4))[0]
    elif nbt_type == tag["double"]:
        return struct.unpack(endianess + "d", read_stream(8))[0]
    elif nbt_type == tag["byte_array"]:
        byte_count = struct.unpack(endianess + "l", read_stream(4))[0]
        tag_value = []
        for i in range(0, byte_count):
            tag_value.append(struct.unpack("b", read_stream(1))[0])
        return tag_value
    elif nbt_type == tag["string"]:
        string_length = struct.unpack(endianess + "H", read_stream(2))[0]
        return read_stream(string_length).decode()
    elif nbt_type == tag["list"]:
        list_type = struct.unpack("B", read_stream(1))[0]
        list_item_count = struct.unpack(endianess + "l", read_stream(4))[0]
        tag_value = []
        for i in range(0, list_item_count):
            tag_value.append(read_type(list_type))
        return tag_value
    elif nbt_type == tag["compound"]:
        return read_compound_tag()
    elif nbt_type == tag["int_array"]:
        int_count = struct.unpack(endianess + "l", read_stream(4))[0]
        tag_value = []
        for i in range(0, int_count):
            tag_value.append(struct.unpack("L", read_stream(4))[0])
        return tag_value
    elif nbt_type == tag["long_array"]:
        long_count = struct.unpack(endianess + "l", read_stream(4))[0]
        tag_value = []
        for i in range(0, long_count):
            tag_value.append(struct.unpack("Q", read_stream(8))[0])
        return tag_value
