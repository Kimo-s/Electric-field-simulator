import math

def findOrginial(initial,terminal):
    if len(initial) == 2 or len(terminal) == 2:
        return Vector(terminal[0]-initial[0],terminal[1]-initial[1],0)
    else:
        return Vector(terminal[0]-initial[0],terminal[1]-initial[1],terminal[2]-initial[2])

class Vector:

    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        self.len = self.findLen(x,y,z)

    def findLen(self,x,y,z):
        return abs(math.sqrt(x**2+y**2+z**2))

    def scaleVector(self,scaler):
        return Vector(scaler*self.x,scaler*self.y,scaler*self.z)

    def dotProduct(self,v2):
        return self.x*v2.x+self.y*v2.y+self.z*v2.z

    def cross(self,v2):
        i_comp = self.y*v2.z-self.z*v2.y
        j_comp = -(self.x*v2.z-self.z*v2.x)
        k_comp = self.x*v2.y-self.y*v2.x

        return Vector(i_comp,j_comp,k_comp)

    def normal(self):
        if self.len == 0:
            return Vector(0,0,0)
        
        return Vector(self.x/self.len,self.y/self.len,self.z/self.len)

    def add(self,v2):
        return Vector(v2.x+self.x,v2.y+self.y,v2.z+self.z)

    def __str__(self):
        return f"Vector: <{self.x},{self.y},{self.z}>"
    
    def equal(self, v):
        if self.x == v.x and self.y == v.y and self.z == v.z:
            return True
        else:
            return False