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
