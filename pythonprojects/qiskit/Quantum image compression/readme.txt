The script is inside quantumimage, PixelList is a help class to deal with the output data from qiskit. 

The title here is perhaps a bit misleading, it is technically compression as given a NxN image it uses 2log2(N)+1 Qbits to store the information instead of N^2 classical bits but in it's current state it's not so useful as it heavily obfuscates your data and actually getting it back is a pain. 

The rough summary is it uses FRQI (Flexible Representation for Quantum Images) to encode a black and white image into the probability distribution of the system, more in detail it sets aside 1 qubit to act as a "color" qubit k qubits to act as a "position vector" in bitstring so as an example of k=2 the state 00 is pixel one, 01 pixel two and so on. The circuit first applies hammard gates on all positional qubits to make all states equally likely and then applies a series of several controlled rotation gates on the color qubit with position vector qubits as control qubits to make it so that if your system is in e.g., the position state 01 which represents pixel 2 the probability for the color qubit to be 1 is cos(theta)^2 and 0 sin(theta)^2 where theta is directly related to pixel 2s color.

To recover the image it runs the circuit many times and takes the count for each pixel and averages it out to get an approximation of the original color. 

The parameters you get to tweak yourself easily is the image file, how many shots to do for the simulator and how many pixels of your image you want to run and these should be visible almost at the top of the script.

Not the most elegant with variable names in it's current state and so far noise free but I plan to fix it up a bit more and do more data analysis. 

Bonus addition folder with images of circuits where I've applied a few gates to mess with the image data before constructing it :)

