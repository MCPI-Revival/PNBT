import os

class PyNBT:
    root = []
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
    
    def checkLength(string, expect):
        length = len(string)
        assert (length == expect), 'Expected ' + str(expect) + 'bytes, got ' + str(length)
        
    def readTriad(str: bytes) -> int:
        PyNBT.checkLength(str, 3)
        return unpack('>L', b'\x00' + str)[0]

    def writeTriad(value: int) -> bytes:
        return pack('>L', value)[1:]

    def readLTriad(str: bytes) -> int:
        PyNBT.checkLength(str, 3)
        return unpack('<L', b'\x00' + str)[0]

    def writeLTriad(value: int) -> bytes:
        return pack('<L', value)[0:-1]
    
    def readBool(b: bytes) -> int:
        return unpack('?', b)[0]

    def writeBool(b: int) -> bytes:
        return b'\x01' if b else b'\x00'
  
    def readByte(c: bytes) -> int:
        PyNBT.checkLength(c, 1)
        return unpack('>B', c)[0]
    
    def readSignedByte(c: bytes) -> int:
        PyNBT.checkLength(c, 1)
        return unpack('>b', c)[0]

    def writeByte(c: int) -> bytes:
        return pack(">B", c)
    
    def readShort(str: bytes) -> int:
        PyNBT.checkLength(str, 2)
        return unpack('>H', str)[0]

    def writeShort(value: int) -> bytes:
        return pack('>H', value)
    
    def readLShort(str: bytes) -> int:
        PyNBT.checkLength(str, 2)
        return unpack('<H', str)[0]

    def writeLShort(value: int) -> bytes:
        return pack('<H', value)
    
    def readInt(str: bytes) -> int:
        PyNBT.checkLength(str, 4)
        return unpack('>L', str)[0]

    def writeInt(value: int) -> bytes:
        return pack('>L', value)

    def readLInt(str: bytes) -> int:
        PyNBT.checkLength(str, 4)
        return unpack('<L', str)[0]

    def writeLInt(value: int) -> bytes:
        return pack('<L', value)

    def readFloat(str: bytes) -> int:
        PyNBT.checkLength(str, 4)
        return unpack('>f', str)[0]

    def writeFloat(value: int) -> bytes:
        return pack('>f', value)

    def readLFloat(str: bytes) -> int:
        PyNBT.checkLength(str, 4)
        return unpack('<f', str)[0]

    def writeLFloat(value: int) -> bytes:
        return pack('<f', value)

    def readDouble(str: bytes) -> int:
        PyNBT.checkLength(str, 8)
        return unpack('>d', str)[0]

    def writeDouble(value: int) -> bytes:
        return pack('>d', value)

    def readLDouble(str: bytes) -> int:
        PyNBT.checkLength(str, 8)
        return unpack('<d', str)[0]

    def writeLDouble(value: int) -> bytes:
        return pack('<d', value)

    def readLong(str: bytes) -> int:
        PyNBT.checkLength(str, 8)
        return unpack('>L', str)[0]

    def writeLong(value: int) -> bytes:
        return pack('>L', value)

    def readLLong(str: bytes) -> int:
        PyNBT.checkLength(str, 8)
        return unpack('<L', str)[0]

    def writeLLong(value: int) -> bytes:
        return pack('<L', value)
    
    def loadFile(self, filename):
        if os.path.isfile(filename)
            fp = open('filename')
        else:
            print("First parameter must be a filename")
            return False
            bname = os.path.splitext(os.path.basename(filename))[0]
            if bname == level:
                version = self.readLInt(fp.read(4))
                lenght = self.readLInt(fp.read(4))
            elif(bname == entities):
                fp.read(12)
            self.traverseTag(self, fp, self.root)
            return self.root[-1]
            
    def traverseTag(self, fp, tree):
        tagType = self.readType(self, fp, self.TAG_BYTE)
        if tagType == self.TAG_END:
            return False
        else:
            tagName = self.readType(self, fp, self.TAG_STRING)
            tagData = self.readType(self, fp, tagType)
            tree = []
            tree.append({'type': tagType, 'name': tagName, 'value': tagData})
            return True
        
    def readType(self, fp, tagType):
        if tagType == self.TAG_BYTE:
            return self.readByte(fp.read(1))
        elif tagType == self.TAG_SHORT:
            return self.readLShort(fp.read(2))
        elif tagType == self.TAG_INT:
            return self.readLInt(fp.read(4))
        elif tagType == self.TAG_LONG:
            return self.readLLong(fp.read(8))
        elif tagType == self.TAG_FLOAT:
            return self.readLFloat(fp.read(4))
        elif tagType == self.TAG_DOUBLE:
            return self.readLDouble(fp.read(8))
        elif tagType == self.TAG_BYTE_ARRAY:
            arrayLength = self.readType(self, fp, self.TAG_INT)
            arr = []
            i = 0
            while i < arrayLength:
                i += 1
                arr = self.readType(self, fp, self.TAG_BYTE)
                return arr
        elif tagType == self.TAG_STRING:
            stringLength = self.readType(self, fp, self.TAG_SHORT)
            if not stringLength:
                return ""
            string = fp.read(stringLength)
            return string
        elif tagType == self.TAG_LIST:
            tagID = self.readType(self, fp, self.TAG_BYTE)
            listLength = self.readType(self, fp, self.TAG_INT)
            list = {'type': tagID, 'value': []}
            i = 0
            while i < listLength:
                i += 1
                list["value"].append(self.readType(self, fp, tagID))
            return list
        elif tagType == self.TAG_COMPOUND:
            tree = []
            while traverseTag(self, fp, tree): pass
            return tree
