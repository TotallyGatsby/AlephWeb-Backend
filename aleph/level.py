from utils.bigendian import *
from collections import namedtuple
from chunk import Chunk

from struct import calcsize
class AlephLevel:
    def readHeader(self, file):
        self.offset = readInt(file)
        self.length = readInt(file)
    
    def readChunks(self, file):
        file.seek(self.offset)
        
        self.chunks = {}
        
        done = False
        # Marathon maps are made of many types of 'chunks'
        # Lines, points, sides, mission info, etc
        while not done:            
            chunk = Chunk()
            chunk.read(file)
            
            
                    
                    
            file.seek(chunk.next + self.offset)
            
            if chunk.next == 0:
                done = True
            
            self.chunks[chunk.tag] = chunk
            