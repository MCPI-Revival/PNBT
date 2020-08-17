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
    def readTriad(data: bytes) -> int:
        PyNBT.checkLength(data, 3)
        return unpack('>L', b'\x00' + data)[0]
    
    @staticmethod
    def writeTriad(value: int) -> bytes:
        return pack('>L', value)[1:]
    
    @staticmethod
    def readLTriad(data: bytes) -> int:
        PyNBT.checkLength(data, 3)
        return unpack('<L', data + b'\x00')[0]

    @staticmethod
    def writeLTriad(value: int) -> bytes:
        return pack('<L', value)[0:-1]
    
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
    def readShort(data: bytes) -> int:
        PyNBT.checkLength(data, 2)
        return unpack('>H', data)[0]
    
    @staticmethod
    def readSignedShort(data: bytes) -> int:
        PyNBT.checkLength(data, 2)
        return PyNBT.signShort(PyNBT.readShort(data))

    @staticmethod
    def writeShort(value: int) -> bytes:
        return pack('>H', value)
    
    @staticmethod
    def readLShort(data: bytes) -> int:
        PyNBT.checkLength(data, 2)
        return unpack('<H', data)[0]
    
    @staticmethod
    def readSignedLShort(data: bytes) -> int:
        PyNBT.checkLength(data, 2)
        return PyNBT.signShort(PyNBT.readLShort(data))

    @staticmethod
    def writeLShort(value: int) -> bytes:
        return pack('<H', value)
    
    @staticmethod
    def readInt(data: bytes) -> int:
        PyNBT.checkLength(data, 4)
        if calcsize('P') == 8:
            value = PyNBT.signInt(unpack('>L', data)[0])
        else:
            value = unpack('>L', data)[0]
        return value

    @staticmethod
    def writeInt(value: int) -> bytes:
        return pack('>L', value)

    @staticmethod
    def readLInt(data: bytes) -> int:
        PyNBT.checkLength(data, 4)
        if calcsize('P') == 8:
            value = PyNBT.signInt(unpack('<L', data)[0])
        else:
            value = unpack('<L', data)[0]
        return value

    @staticmethod
    def writeLInt(value: int) -> bytes:
        return pack('<L', value)
    
    @staticmethod
    def readFloat(data: bytes) -> int:
        PyNBT.checkLength(data, 4)
        return unpack('>f', data)[0]
    
    @staticmethod
    def readRoundedFloat(data, accuracy):
        return round(PyNBT.readFloat(data), accuracy)

    @staticmethod
    def writeFloat(value: int) -> bytes:
        return pack('>f', value)

    @staticmethod
    def readLFloat(data: bytes) -> int:
        PyNBT.checkLength(data, 4)
        return unpack('<f', data)[0]
    
    @staticmethod
    def readRoundedLFloat(data, accuracy):
        return round(PyNBT.readLFloat(data), accuracy)

    @staticmethod
    def writeLFloat(value: int) -> bytes:
        return pack('<f', value)
    
    @staticmethod
    def printFloat(value):
        return match(r"/(\\.\\d+?)0+$/", "" + value).group(1)
    
    @staticmethod
    def readDouble(data: bytes) -> int:
        PyNBT.checkLength(data, 8)
        return unpack('>d', data)[0]

    @staticmethod
    def writeDouble(value: int) -> bytes:
        return pack('>d', value)

    @staticmethod
    def readLDouble(data: bytes) -> int:
        PyNBT.checkLength(data, 8)
        return unpack('<d', data)[0]

    @staticmethod
    def writeLDouble(value: int) -> bytes:
        return pack('<d', value)
    
    @staticmethod
    def readLong(data: bytes) -> int:
        PyNBT.checkLength(data, 8)
        return unpack('>Q', data)[0]
    
    @staticmethod
    def writeLong(value: int) -> bytes:
        return pack('>Q', value)

    @staticmethod
    def readLLong(data: bytes) -> int:
        PyNBT.checkLength(data, 8)
        return unpack('<Q', data)[0]

    @staticmethod
    def writeLLong(value: int) -> bytes:
        return pack('<Q', value)
 
    @staticmethod
    def loadFile(filename):
        if os.path.isfile(filename):
            fp = open(filename, "rb")
        else:
            print("First parameter must be a filename")
            return False
        bname = os.path.splitext(os.path.basename(filename))[0]
        if bname == 'level':
            version = PyNBT.readLInt(fp.read(4))
            lenght = PyNBT.readLInt(fp.read(4))
        elif bname == 'entities':
            fp.read(12)
        PyNBT.traverseTag(fp, PyNBT.root)
        return PyNBT.root
   
    @staticmethod
    def traverseTag(fp, tree: dict):
        tagType = PyNBT.readType(fp, PyNBT.TAG_BYTE)
        if not tagType == PyNBT.TAG_END:
            tagName = PyNBT.readType(fp, PyNBT.TAG_STRING)
            tagData = PyNBT.readType(fp, tagType)
            tree.update({'type': tagType, 'name': tagName, 'value': tagData})
            return True
        else:
            return False
     
    @staticmethod
    def readType(fp, tagType):
        if tagType == PyNBT.TAG_BYTE:
            return PyNBT.readByte(fp.read(1))
        elif tagType == PyNBT.TAG_SHORT:
            return PyNBT.readLShort(fp.read(2))
        elif tagType == PyNBT.TAG_INT:
            return PyNBT.readLInt(fp.read(4))
        elif tagType == PyNBT.TAG_LONG:
            return PyNBT.readLLong(fp.read(8))
        elif tagType == PyNBT.TAG_FLOAT:
            return PyNBT.readLFloat(fp.read(4))
        elif tagType == PyNBT.TAG_DOUBLE:
            return PyNBT.readLDouble(fp.read(8))
        elif tagType == PyNBT.TAG_BYTE_ARRAY:
            arrayLength = PyNBT.readType(fp, PyNBT.TAG_INT)
            arr = []
            i = 0
            while i < arrayLength:
                arr.append(PyNBT.readType(fp, PyNBT.TAG_BYTE))
                i += 1
                return arr
        elif tagType == PyNBT.TAG_STRING:
            stringLength = PyNBT.readType(fp, PyNBT.TAG_SHORT)
            if not stringLength:
                return ""
            string = fp.read(stringLength)
            return string
        elif tagType == PyNBT.TAG_LIST:
            tagID = PyNBT.readType(fp, PyNBT.TAG_BYTE)
            listLength = PyNBT.readType(fp, PyNBT.TAG_INT)
            dictlist = {'type': tagID, 'value': []}
            i = 0
            while i < listLength:
                dictlist["value"].append(PyNBT.readType(fp, tagID))
                i += 1
            return dictlist
        elif tagType == PyNBT.TAG_COMPOUND:
            tree = {}
            while PyNBT.traverseTag(fp, tree): pass
            return tree
        elif tagType == PyNBT.TAG_INT_ARRAY:
            arrayLength = PyNBT.readType(fp, PyNBT.TAG_INT)
            arr = []
            i = 0
            while i < arrayLength:
                arr.append(PyNBT.readType(fp, PyNBT.TAG_INT))
                i += 1
                return arr
        elif tagType == PyNBT.TAG_LONG_ARRAY:
            arrayLength = PyNBT.readType(fp, PyNBT.TAG_INT)
            arr = []
            i = 0
            while i < arrayLength:
                arr.append(PyNBT.readType(fp, PyNBT.TAG_LONG))
                i += 1
                return arr
