from struct import unpack

def readShort(file):
    b = file.read(2)
    return unpack('>h', b)[0]

def readUShort(file):
    b = file.read(2)
    return unpack('>H',b)[0]
    
def readInt(file):
    b = file.read(4)
    return unpack('>i', b)[0]
    
def readLong(file):
    b = file.read(8)
    return unpack('>l', b)[0]

def readFixed(file):
    b = readInt(file) / 65535.0
    return b
    
    