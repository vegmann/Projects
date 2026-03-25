from qiskit import QuantumCircuit
import math
from qiskit_aer import AerSimulator
from qiskit.primitives import StatevectorSampler
from PixelList import PixelList 
from PIL import Image
import numpy as np

#parameters that decide how much you want to compress your image, and how many counts to run
sizeparam=50
countsparam=70000

#imports image resizes it and converts it to a nested list and calculates how many qubits are needed
img= Image.open('angel.png').convert('L')
img=img.resize((sizeparam, sizeparam))
img_mini=img
dimensions=np.array(img).shape
matrix = np.array(img).tolist()
n=math.ceil(2*math.log2((len(matrix))))+1

#this takes as input a matrix with black and white image data
#in the form of a nested list and returns a list of angles tied to the brightness of the pixel
angles=[]
for ii in range(len(matrix)):
    values=matrix[ii]
    for ii in range(len(values)):
        angle=(values[ii]/256)*(math.pi/2)
        angles.append(2*angle)



#n is the color qubit this applies an hammard gate to all of the rest
imagecircuit = QuantumCircuit(n)
for ii in range(n-1):
    imagecircuit.h(ii)



positionqubits=[ii for ii in range(n-1)]

for ii in range(len(angles)):
   position= f"{ii:0{n-1}b}"
   positionbits = [int(char) for char in position]
   angle=angles[ii]
   
   for index,bit in enumerate(positionbits):
      if bit==0:
         imagecircuit.x(index)

   imagecircuit.mcry(angles[ii],positionqubits,n-1)

   for index,bit in enumerate(positionbits):
      if bit==0:
         imagecircuit.x(index)


#information for the simulator
imagecircuit.measure_all()

sim = AerSimulator()

sampler = StatevectorSampler()
job = sampler.run([(imagecircuit)], shots=countsparam)
result = job.result()

pub_result = result[0]
counts_dict = pub_result.data.meas.get_counts()

#takes the ordered dictionary outputted and reformats it into a friendlier format
nested_mirrored = [[bitstring[::-1], count] for bitstring, count in counts_dict.items()]

#uses the help class to format the data into something that can be turned back into image data
lista=PixelList(n)
lista.updatelist(nested_mirrored)
values=lista.givepixelvalues()
#formats it into something pillow will accept 
values=values[:dimensions[0]*dimensions[1]]
final_values = np.clip(values, 0, 255)
finalmatrix = np.array(final_values,dtype=np.uint8).reshape(dimensions[0], dimensions[1])
new_img = Image.fromarray(finalmatrix)

#saves images both old and new
img_mini.save('normieangel.png')
new_img.save('quantumangel.png')
print("Im done!!")
#print(nested_mirrored)

