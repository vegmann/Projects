This is a simple non-lossless image compression algorithm using singular value decomposition. It's more to show off the theory behind it so it doesn't actually return a smaller file as when you display it it's converted back into a normal image file. The point is to show that the algorithm cuts out data in such a way the largest details in the picture are preserved and you can cut out surprisingly much before it shows. 

For regular compression set the lower limit to 1 and the upper limit to whatever you want it to be as long as its smaller than the width of the picture. Smaller upper limit compresses more. 

The folder has some images I've made by mixing up the data of several pictures in different way:)