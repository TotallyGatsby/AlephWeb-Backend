from utils.bigendian import *

EntryData = { 
  "LINS": {
    "entryLen": 32,
    "packString": ">hhhhhhxxxxxxxxxxxxxxxxxxxx",
    # Not entirely sure what all these do, variable names lifted from Aleph One
    "varNames": "p0 p1 flg len hAdjFlr lAdjCei"
  },
  "EPNT" : {
    "entryLen": 16,
    "packString": ">hhhhhxxxxxx",
    "varNames": "flg hAdjFlr lAdjFlr vertx verty"
  },
  "SIDS" : {
    "entryLen": 64,
    "packString": ">hhhhhhhhhhhxxxxxxxxxxxxxxxxxxxxxxxxxxhhhhhxxxxxx",
    # type flags primaryTextureX primaryTextureY primaryTextureMaterial 
    # secondaryTexture x/y/material transparent texture x/y/material
    # polygonIndex lineIndex
    "varNames" : "type flags px py pmat sx sy smat tx ty tmat polyidx lineidx plite slite tlite"
  },
  "PLAT" : {
    "entryLen": 140,
    "packString": ">hIhhhhhhh74xh44x",
    "varNames" : "type flags speed delay minFloorHeight maxFloorHeight minCeilHeight maxCeilHeight polyidx"
   }
}

MaxVertices = 8

#TODO: A lot could be done to send only the data that is actually used. For example, in a SIDS entry,
# it is typical to only use the primary material, but all 3 materials are currently sent
#TODO: Settle on brevity (and thus smaller filesize) or descriptive variable names
class Chunk:
    def read(self, file):
        self.tag = file.read(4)
        self.next = readInt(file)
        self.length = readInt(file)
        # NOTE: Padding in the file, I believe
        file.seek(4, 1)
        
        self.entries = []
        
        if self.tag in EntryData:
            info = EntryData[self.tag]
            for i in range(0, self.length / info["entryLen"]):
                record = file.read(info["entryLen"])
                val = {k:v for k,v in zip(info["varNames"].split(), unpack(info["packString"], record))}
                self.entries.append(val)

        elif self.tag == "POLY":
            self.readPoly(file)
        elif self.tag == "LITE":
            self.readLite(file)
    
    def readLite(self, file):
        for i in range(0, self.length/100):
            val = {}
            val["type"] = readShort(file) #2
            val["flags"] = readUShort(file) #4
            val["phase"] = readShort(file) #6
            val["pAct"] = self.readLightFunction(file) #20
            val["sAct"] = self.readLightFunction(file) #34
            val["bAct"] = self.readLightFunction(file) #48
            val["pInact"] = self.readLightFunction(file) #62
            val["sInact"] = self.readLightFunction(file) #76
            val["bInact"] = self.readLightFunction(file) #90
            val["tagID"] =readShort(file) #92
            file.read(8) #100
            
            self.entries.append(val)
            
    
    def readLightFunction(self, file):
        result = {}
        result["func"] = readShort(file)
        result["period"] = readShort(file)
        result["deltaperiod"] = readShort(file)
        result["intensity"] = readInt(file)
        result["deltaintensity"] = readInt(file)
        return result
    
    def readPoly(self, file): #See map.h line 686
        for i in range(0, self.length / 128):
            val = {}
            val["type"] = readShort(file) # 2
            val["flags"] = readUShort(file) #4
            val["permutation"] = readShort(file) #6
            val["vertexCount"] = readUShort(file) #8
            
            val["endpointIndices"] = []
            val["lineIndices"] = []
            
            for j in range(0, MaxVertices):
                if (j < val["vertexCount"]):
                    val["endpointIndices"].append(readShort(file)) #24
                else:
                    readShort(file)
                
            for j in range(0, MaxVertices):
                if (j < val["vertexCount"]):
                    val["lineIndices"].append(readShort(file)) #40
                else:
                    readShort(file)
                
            val["floorTexture"] = readUShort(file) #42
            val["ceilingTexture"] = readUShort(file) #44
            val["floorHeight"] = readShort(file) #46
            val["ceilingHeight"] = readShort(file) #48
            val["floorLightIndex"] = readShort(file) #50
            val["ceilingLightIndex"] = readShort(file)#52
            val["area"] = readInt(file) #56

            #TODO read the remaining bits
            # Discard the exclusion zone information
            file.read(12) #68
            
            val["neighbors"] = []            
            for j in range(0, MaxVertices):
                val["neighbors"].append(readShort(file)) #84
            
            file.read(8)
            val["sideIndices"] = []
            for j in range(0, MaxVertices):
                if (j < val["vertexCount"]):
                    val["sideIndices"].append(readShort(file)) #108
                else:
                    readShort(file)
            val["floorX"] = readShort(file) #110
            val["floorY"] = readShort(file) #112
            val["ceilingX"] = readShort(file) #114
            val["ceilingY"] = readShort(file) #116
            val["mediaIndex"] = readShort(file) #118
            file.read(10)
            
            
            self.entries.append(val)