class Obj(object):
    nameA =""
    nameB =""
    z =""
    # The class "constructor" - It's actually an initializer 
    def __init__(self, nameA, nameB, z):
        self.nameA = nameA
        self.nameB = nameB
        self.z=z
    def makeObj(nameA, nameB, z):
        obj = Obj(nameA, nameB, z)
        return obj
    
    
    def addNameA(self,nameA):
        self.nameA=nameA
    def addNameB(self,nameB):
        self.nameB=nameB
    def addZ(self,z):
        self.z=z

    def getNameA(self):
        return self.nameA
    def getNameB(self):
        return self.nameB
    def getZ(self):
        return self.z
