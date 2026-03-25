import math

#help class that basically deals with the conversion of the raw qiskit output data into something that can be used
# to recreate an image 
class Pixel:
    'keeps track of which pixel has what count'
    def __init__(self,n):
        self.count1=0
        self.count0=0
        self.index=n

class PixelList:
    'class all about managing qiskit output'
    def __init__(self,n):
        self.list = [Pixel(ii) for ii in range(2**(n-1))]
    
    def updatelist(self,stringdict):
        'given a string of qiskit output with color bit last takes and puts the counts in the correct spot'
        for object in stringdict:
            element=object[0]
            binnumber = element[:-1]
            parity=int(element[-1])
            count=object[1]
            wholenumber=int(binnumber,2)
            if parity == 1:
             self.list[wholenumber].count1=int(count)
            elif parity == 0:
             self.list[wholenumber].count0=int(count)
            else:
                print("something has gone wrong")
                return()
        return()
    
    def givepixelvalues(self):
        'given'
        valuelist=[]
        for element in self.list:
            if element.count1==0:
             valuelist.append(0)
            else:
             value=element.count1/(element.count1+element.count0)
             transformedvalue=(1-2*math.acos(math.sqrt(value))/math.pi)*256
             valuelist.append(round(transformedvalue))
        return(valuelist)






