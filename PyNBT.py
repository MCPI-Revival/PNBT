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

def read(data, endianess = "<"):
    nbt = {}
    offset = 0
    while not len(data) <= offset:
        tag_type = struct.unpack("b", data[offset:offset + 1])[0]
        offset += 1
        if tag_type == tag["end"]:
            break
        tag_name_length = struct.unpack(endianess + "H", data[offset:offset + 2])[0]
        offset += 2
        tag_name = data[offset:offset + tag_name_length]
        if nbt_type == tag["byte"]:
            tag_value = struct.unpack("b", data[offset:offset + 1])[0]
            offset += 1
            nbt[tag_name] = {"type": tag_type, "value": tag_value}
        elif nbt_type == tag["short"]:
            tag_value = struct.unpack(endianess + "h", data[offset:offset + 2])[0]
            offset += 2
            nbt[tag_name] = {"type": tag_type, "value": tag_value}
        elif nbt_type == tag["int"]:
            tag_value = struct.unpack(endianess + "l", data[offset:offset + 4])[0]
            offset += 4
            nbt[tag_name] = {"type": tag_type, "value": tag_value}
        elif nbt_type == tag["long"]:
            tag_value = struct.unpack(endianess + "q", data[offset:offset + 8])[0]
            offset += 8
            nbt[tag_name] = {"type": tag_type, "value": tag_value}
        elif nbt_type == tag["float"]:
            tag_value = struct.unpack(endianess + "f", data[offset:offset + 4])[0]
            offset += 4
            nbt[tag_name] = {"type": tag_type, "value": tag_value}
        elif nbt_type == tag["double"]:
            tag_value = struct.unpack(endianess + "d", data[offset:offset + 8])[0]
            offset += 8
            nbt[tag_name] = {"type": tag_type, "value": tag_value}
        elif nbt_type == tag["byte_array"]:
            byte_count = struct.unpack(endianess + "l", data[offset:offset + 4])[0]
            offset += 4
            tag_value = []
            for i in range(0, byte_count):
                tag_value.append(struct.unpack("b", data[offset:offset + 1])[0])
                offset += 1  
            nbt[tag_name] = {"type": tag_type, "value": tag_value}
        return nbt
