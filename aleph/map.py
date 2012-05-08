from utils.bigendian import *
from level import AlephLevel
import jsonpickle

class AlephMap:
    def __init__(self, fileName):
        self.readScea(fileName)

    def readScea(self, fileName):
        file = open(fileName, "rb")
        self.readHeader(file)
        self.readLevels(file)

    def readLevels(self, file):
        self.levels = []
        for i in range(0, self.levelCount):
            print "loading level"
            file.seek(self.headerLength + (i * 84));
            
            level = AlephLevel()
            level.readHeader(file)
            level.readChunks(file)
            self.levels.append(level)
        
    def readHeader(self, file):
        self.version  = readShort(file)
        self.dataVersion = readShort(file)
        self.mapName  = file.read(64).strip('\0')
        self.checkSum = readInt(file)
        self.headerLength   = readInt(file)
        self.levelCount = readShort(file)
        self.appDirSize = readShort(file)
        self.isMergedFile = self.appDirSize == 0x4a
        self.chunkHeaderSize = readShort(file)
        self.parentChecksum = readInt(file)
        
    def getJSON(self):
        # TODO: Don't serialize all the data, only
        # serialize what is relevant to the game
        #jsonpickle.set_preferred_backend('simplejson')
        #jsonpickle.set_encoder_options('simplejson', sort_keys=False, indent=2)
        return jsonpickle.encode(self, unpicklable=False)