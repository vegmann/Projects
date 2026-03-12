This project is several smaller problems.
Labb3_1d is an implementation of several iterative methods for solving the kepler problem and studying the difference in accuracy between them.
Wavefunc is a tool to solve the one dimensional wave equation with Dirichlet conditions, it does this by first spatially discretizing in the x-dimension and turning the resulting second order system into a first order system and implementing symplectic euler to solve it.
Wavefuncneumann is the same problem but now with neumann conditions instead.

As this was coded mostly with numerical results in mind it is not extremely user friendly, to see the plots you have to decomment the lines where the plots are. 