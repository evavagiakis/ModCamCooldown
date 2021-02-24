#Initial three block cooldown model EMV 2/24/2021

import numpy as np
import matplotlib.pyplot as plt

tc1i=175 #Kelvin, initial T of 40 K front plate
tc2i=170 #Kelvin, initial T of 40 K front shell + G10 ring
tc3i=168 #Kelvin, initial T of 40 K rear shell

tg1i=170 #Kelvin, initial T of 40 K front shell for conductivity 
tg2i=168 #Kelvin, initial T of 40 K rear shell for conductivity 
tg3i=135 #Kelvin, initial T of 40 K DR adapter for conductivity 

tbath=63.5 #Kelvin, t=0 temperature of the 40 K DR plate 

c=900 #J/kg*K, specific heat capacity of 6063-T5 Al
k=195 #W/m*K, thermal conductivity of each link (can be improved by using formula instead of this same val for all)

mc1=4 #kg, mass of 40 K front plate
mc2=26 #kg, mass of 40 K front shell + G10 ring 
mc3=33 #kg, mass of 40 K rear shell 

al1=0.15 #m, A/l of the front shell 
al2=0.12 #m, A/l of the rear shell
al3=0.016 #m, A/l of the DR adapter 

c1=c*mc1 #J/K
c2=c*mc2 #J/K
c3=c*mc3 #J/K

g1=k*al1 #W/K
g2=k*al2 #W/K
g3=k*al3 #W/K

Wloading=26 #W, loading estimate on the 40 K front plate 
t=3600 #s, time for cooldown change estimate

#See overleaf document for algebra; in the future, want to do this in python. 
#Solving this system of equations
A=np.array([[30.25,-29.25,0],[0,4.6,-3.6],[0,0,1.38]])
B=np.array([201,170,192])
X=np.linalg.inv(A).dot(B)

print(X)

