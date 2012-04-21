from struct import unpack

def readShort(file):
    b = file.read(2)
    return unpack('>h', b)[0]
    
def readInt(file):
    b = file.read(4)
    return unpack('>i', b)[0]
    
def readLong(file):
    b = file.read(8)
    return unpack('>l', b)[0]