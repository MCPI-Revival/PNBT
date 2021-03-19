################################################################################
#                                                                              #
#  __  __ _____ ____   ____                 _                                  #
# |  \/  |  ___|  _ \ / ___| __ _ _ __ ___ (_)_ __   __ _                      #
# | |\/| | |_  | | | | |  _ / _` | '_ ` _ \| | '_ \ / _` |                     #
# | |  | |  _| | |_| | |_| | (_| | | | | | | | | | | (_| |                     #
# |_|  |_|_|   |____/ \____|\__,_|_| |_| |_|_|_| |_|\__, |                     #
#                                                    |___/                     #
# Copyright 2021 MFDGaming                                                     #
#                                                                              #
# Permission is hereby granted, free of charge, to any person                  #
# obtaining a copy of this software and associated documentation               #
# files (the "Software"), to deal in the Software without restriction,         #
# including without limitation the rights to use, copy, modify, merge,         #
# publish, distribute, sublicense, and/or sell copies of the Software,         #
# and to permit persons to whom the Software is furnished to do so,            #
# subject to the following conditions:                                         #
#                                                                              #
# The above copyright notice and this permission notice shall be included      #
# in all copies or substantial portions of the Software.                       #
#                                                                              #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR   #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,     #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER       #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING      #
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS #
# IN THE SOFTWARE.                                                             #
#                                                                              #
################################################################################

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

endianess = "<"

def reset_stream():
    stream["data"] = b""
    stream["offset"] = 0

def read_stream(length):
    stream["offset"] += length
    return stream["data"][stream["offset"] - length:stream["offset"]]

def read(data):
    reset_stream()
    stream["data"] = data
    return read_compound_tag()

def read_file(file_path):
    if os.path.isfile(file_path):
        data = open(file_path, "rb").read()
        file_base_name = os.path.splitext(os.path.basename(file_path))[0]
        if file_base_name == "level":
            return read(data[8:])
        if file_base_name == "entities":
            return read(data[12:])
        return read(data)

def read_compound_tag():
    tree = {}
    while not len(stream["data"]) <= stream["offset"]:
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
        return {"type": list_type, "value": tag_value}
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
