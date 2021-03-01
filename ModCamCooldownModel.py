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
Wloading2=10 #W, loading estimate on the 40 K front shell
t=3600 #s, time for cooldown change estimate
 
#Solving this system of equations

temps1=[tc1i]
temps2=[tc2i]
temps3=[tc3i]

for s in range(10):
	B1=tc1i+Wloading*t/c1
	B2=tc2i+Wloading2*t/c2
	B3=(tc3i+g3*tbath*t/c3)
	
	A11=(g1*t/c1 +1)
	A12=(-g1*t/c1)
	A13=0
	
	A21=0
	A22=(g2*t/c2+1)
	A23=(-g2*t/c2)
	
	A31=0
	A32=0
	A33=(g3*t/c3+1)
	
	A=np.array([[A11,A12,A13],[A21,A22,A23],[A31,A32,A33]])
	B=np.array([B1,B2,B3])
	X=np.linalg.inv(A).dot(B)
	
	print(A)
	print(B)		
	print(X)
		

	temps1.append(X[0])
	temps2.append(X[1])
	temps3.append(X[2])
	
	tc1i=X[0]
	tc2i=X[1]
	tc3i=X[2]
	
	
plt.plot(temps1,'b-',label='40 K Front Plate, 10W shell loading')
plt.plot(temps2,'g-',label='40 K G10 Ring, 10W shell loading')
plt.plot(temps3,'r-',label='40 K Rear Shell, 10W shell loading')

model=np.loadtxt('model.txt',delimiter=',')

plt.plot(model[:,0],'b:',label='40 K Front Plate')
plt.plot(model[:,1],'g:',label='40 K G10 Ring')
plt.plot(model[:,2],'r:',label='40 K Rear Shell')

plt.ylabel('K')
plt.xlabel('Hours')
plt.title('Adding 10 W loading to the 40 K Front Shell')
plt.legend()

plt.show()

#np.savetxt('model_withshellloading.txt',np.array([temps1,temps2,temps3]).T,delimiter=',')
