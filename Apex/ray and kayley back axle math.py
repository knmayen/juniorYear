# importing shit
import sympy
from sympy import pprint
import numpy as np
import math

#------------------ linear algebra for equilibrium equations-------------------

# first I wanted to find all of the actual forces on the axle. I set up the FBD 
# and then imputed the values of the variables into the script
Ll = 5.1215 # inches
Ml = 7.45 # inches
Rl = 2.6215 # inches
fL = 60  # lbf 
fR = 60  # lbf 


# set up the coefficients to use linear algebra
coeff_matrix = np.array([[1, 1], 
                         [Ll, Ll + Ml]])

constants_matrix = np.array([[fL + fR], 
                             [fR * (Ll + Ml + Rl)]])

result = np.linalg.solve(coeff_matrix, constants_matrix)
# this is the force in lbf on  FB1 and FB2
print(result)



#----------------- sympy for bending moment and FOS----------------------------

# then there was some real meche thinking to get the bending moment

# setting up sympy symbols (dw about this)
fos = sympy.symbols('FOS')
yield_stress = sympy.symbols('sigma_yield')
actual_stress = sympy.symbols('sigma_actual')
bending_stress = sympy.symbols('sigma_bending')
bending_moment = sympy.symbols('M')
radius = sympy.symbols('r')
moment_of_inertia = sympy.symbols('I')
c_moment_of_inertia = sympy.symbols('cI')
r_moment_of_inertia = sympy.symbols('rI')
rect_b = sympy.symbols('b')
rect_d = sympy.symbols('d')



# now actually doing FOS calculations

FOS_eq = sympy.Eq(fos, yield_stress/actual_stress) # the normal factor of saftey equation

bending_eq = sympy.Eq(bending_stress, bending_moment * radius / moment_of_inertia)
circle_MOI_eq = sympy.Eq(c_moment_of_inertia, math.pi * radius ** 4 / 4)
rect_MOI_eq = sympy.Eq(r_moment_of_inertia, rect_b * rect_d ** 3 / 12)
MOI_eq = sympy.Eq(moment_of_inertia, circle_MOI_eq.rhs - rect_MOI_eq.rhs)
pprint(MOI_eq)
# pprint(bending_eq)
# pprint(MOI_eq)

FOS_eq = FOS_eq.subs(actual_stress, bending_eq.rhs)
FOS_eq = FOS_eq.subs(moment_of_inertia, MOI_eq.rhs)
r_eq = sympy.solve(FOS_eq, radius)
r_eq = r_eq[3] # the third option was the only one with a real nonnegative answer
pprint(r_eq)

values_from_problem = {
    fos: 4,
    yield_stress: 54000,
    bending_moment: 307.29,
    rect_b: 5/16,
    rect_d: .35
}

r_solution = r_eq.subs(values_from_problem).evalf()
print(r_solution)