import os
from struct import unpack, pack, calcsize
import sys

class PyNBT:
    root = {}
    TAG_END = 0
    TAG_BYTE = 1
    TAG_SHORT = 2
    TAG_INT = 3
    TAG_LONG = 4
    TAG_FLOAT = 5
    TAG_DOUBLE = 6
    TAG_BYTE_ARRAY = 7
    TAG_STRING = 8
    TAG_LIST = 9
    TAG_COMPOUND = 10
    TAG_INT_ARRAY = 11
    TAG_LONG_ARRAY = 12
    
    BIG_ENDIAN = 0x00
    LITTLE_ENDIAN = 0x01
    ENDIANNESS = BIG_ENDIAN if sys.byteorder == "big" else LITTLE_ENDIAN
    
    endianess = ""
    
    @staticmethod
    def checkLength(data: bytes, expect: int):
        length = len(data)
        assert (length == expect), 'Expected ' + str(expect) + 'bytes, got ' + str(length)
        
    @staticmethod
    def sign(num, bitlen):
        bits = bitlen - 1
        x = num & (2 ** bitlen - 1)
        a = x & (2 ** bits - 1)
        b = x & (2 ** bits)
        return (~(2 ** bits - 1) & (-1) | a) if b else a
        
    @staticmethod
    def signByte(value: int):
        if calcsize('P') == 8:
            return PyNBT.sign(value, 56)
        else:
            return PyNBT.sign(value, 24)
        
    @staticmethod
    def unsignByte(value: int):
        return value & 0xff
        
    @staticmethod
    def signShort(value: int):
        if calcsize('P') == 8:
            return PyNBT.sign(value, 48)
        else:
            return PyNBT.sign(value, 16)

    @staticmethod
    def unsignShort(value: int):
        return value & 0xffff
    
    @staticmethod
    def signInt(value: int):
        return PyNBT.sign(value, 32)

    @staticmethod
    def unsignInt(value: int):
        return value & 0xffffffff
    
    @staticmethod
    def readTriad(endianess: str, data: bytes) -> int:
        PyNBT.checkLength(data, 3)
        assert endianess == ("<" or ">"), "Invalid Endianess"
        if endianess == ">":
            newData = b'\x00' + data
        else:
            newData = data + b'\x00'
        return unpack(endianess + 'L', newData)[0]
    
    @staticmethod
    def writeTriad(endianess: str, value: int) -> bytes:
        assert endianess == ("<" or ">"), "Invalid Endianess"
        if endianess == ">":
            data = pack(endianess + 'L', value)[1:]
        else:
            data = pack(endianess + 'L', value)[0:-1]
        return data
    
    @staticmethod
    def readBool(data: bytes) -> bool:
        return unpack('?', data)[0]

    @staticmethod
    def writeBool(value: bool) -> bytes:
        return b'\x01' if value else b'\x00'
    
    @staticmethod
    def readByte(data: bytes) -> int:
        PyNBT.checkLength(data, 1)
        return ord(data)
    
    @staticmethod
    def readSignedByte(data: bytes) -> int:
        PyNBT.checkLength(data, 1)
        return PyNBT.signByte(PyNBT.readByte(data))

    @staticmethod
    def writeByte(value: int) -> bytes:
        return chr(value).encode()
    
    @staticmethod
    def readShort(endianess: str, data: bytes) -> int:
        PyNBT.checkLength(data, 2)
        assert endianess == ("<" or ">"), "Invalid Endianess"
        return unpack(endianess + 'H', data)[0]
    
    @staticmethod
    def readSignedShort(endianess: str, data: bytes) -> int:
        PyNBT.checkLength(data, 2)
        return PyNBT.signShort(PyNBT.readShort(endianess, data))

    @staticmethod
    def writeShort(endianess: str, value: int) -> bytes:
        assert endianess == ("<" or ">"), "Invalid Endianess"
        return pack(endianess + 'H', value)
    
    @staticmethod
    def readInt(endianess: str, data: bytes) -> int:
        PyNBT.checkLength(data, 4)
        assert endianess == ("<" or ">"), "Invalid Endianess"
        value = unpack(endianess + 'L', data)[0]
        if calcsize('P') == 8:
            value = PyNBT.signInt(value)
        return value

    @staticmethod
    def writeInt(endianess: str, value: int) -> bytes:
        assert endianess == ("<" or ">"), "Invalid Endianess"
        return pack(endianess + 'L', value)
    
    @staticmethod
    def readFloat(endianess: str, data: bytes) -> int:
        PyNBT.checkLength(data, 4)
        assert endianess == ("<" or ">"), "Invalid Endianess"
        return unpack(endianess + 'f', data)[0]
    
    @staticmethod
    def readRoundedFloat(endianess: str, data, accuracy):
        return round(PyNBT.readFloat(endianess, data), accuracy)

    @staticmethod
    def writeFloat(endianess: str, alue: int) -> bytes:
        assert endianess == ("<" or ">"), "Invalid Endianess"
        return pack(endianess + 'f', value)
    
    @staticmethod
    def printFloat(value):
        return match(r"/(\\.\\d+?)0+$/", "" + value).group(1)
    
    @staticmethod
    def readDouble(endianess: str, data: bytes) -> int:
        PyNBT.checkLength(data, 8)
        assert endianess == ("<" or ">"), "Invalid Endianess"
        return unpack(endianess + 'd', data)[0]

    @staticmethod
    def writeDouble(endianess: str, value: int) -> bytes:
        assert endianess == ("<" or ">"), "Invalid Endianess"
        return pack(endianess + 'd', value)
    
    @staticmethod
    def readLong(endianess: str, data: bytes) -> int:
        PyNBT.checkLength(data, 8)
        assert endianess == ("<" or ">"), "Invalid Endianess"
        return unpack(endianess + 'Q', data)[0]
    
    @staticmethod
    def writeLong(endianess: str, value: int) -> bytes:
        assert endianess == ("<" or ">"), "Invalid Endianess"
        return pack(endianess + 'Q', value)
    
    def __init__(self, endianess: str):
        self.endianess = endianess
        
    def loadFile(self, filename: str):
        if os.path.isfile(filename):
            fp = open(filename, "rb")
        else:
            print("First parameter must be a filename")
            return False
        bname = os.path.splitext(os.path.basename(filename))[0]
        if bname == 'level':
            version = self.readInt(self.endianess, fp.read(4))
            lenght = self.readInt(self.endianess, fp.read(4))
        elif bname == 'entities':
            fp.read(12)
        self.traverseTag(fp, self.root)
        return self.root[list(self.root.keys())[-1]]
   
    def traverseTag(self, fp, tree: dict):
        tagType = self.readType(fp, self.TAG_BYTE)
        if not tagType == self.TAG_END:
            tagName = self.readType(fp, self.TAG_STRING)
            tagData = self.readType(fp, tagType)
            tree[tagName] = {'type': tagType, 'name': tagName, 'value': tagData}
            return True
        else:
            return False
     
    def readType(self, fp, tagType):
        if tagType == self.TAG_BYTE:
            return self.readByte(fp.read(1))
        elif tagType == self.TAG_SHORT:
            return self.readShort(self.endianess, fp.read(2))
        elif tagType == self.TAG_INT:
            return self.readInt(self.endianess, fp.read(4))
        elif tagType == self.TAG_LONG:
            return self.readLong(self.endianess, fp.read(8))
        elif tagType == self.TAG_FLOAT:
            return self.readFloat(self.endianess, fp.read(4))
        elif tagType == self.TAG_DOUBLE:
            return self.readDouble(self.endianess, fp.read(8))
        elif tagType == self.TAG_BYTE_ARRAY:
            arrayLength = self.readType(fp, self.TAG_INT)
            arr = []
            i = 0
            while i < arrayLength:
                arr.append(self.readType(fp, self.TAG_BYTE))
                i += 1
                return arr
        elif tagType == self.TAG_STRING:
            stringLength = self.readType(fp, self.TAG_SHORT)
            if not stringLength:
                return ""
            string = fp.read(stringLength)
            return string
        elif tagType == self.TAG_LIST:
            tagID = self.readType(fp, self.TAG_BYTE)
            listLength = self.readType(fp, self.TAG_INT)
            dictlist = {'type': tagID, 'value': []}
            i = 0
            while i < listLength:
                dictlist["value"].append(self.readType(fp, tagID))
                i += 1
            return dictlist
        elif tagType == self.TAG_COMPOUND:
            tree = {}
            while self.traverseTag(fp, tree): pass
            return tree
        elif tagType == self.TAG_INT_ARRAY:
            arrayLength = self.readType(fp, self.TAG_INT)
            arr = []
            i = 0
            while i < arrayLength:
                arr.append(self.readType(fp, self.TAG_INT))
                i += 1
                return arr
        elif tagType == self.TAG_LONG_ARRAY:
            arrayLength = self.readType(fp, self.TAG_INT)
            arr = []
            i = 0
            while i < arrayLength:
                arr.append(self.readType(fp, self.TAG_LONG))
                i += 1
                return arr
