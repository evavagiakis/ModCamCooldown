# get LakeShore temp/res log and plot

from __future__ import print_function
import sys
if len(sys.argv) != 2 and len(sys.argv) !=3:
   # print >>sys.stderr, ' %s <data path> <ctime optional>' % sys.argv[0]
   print(' %s <data path> <ctime optional>' % sys.argv[0],file=sys.stderr)

   sys.exit(2)
   pass

import numpy as np
import matplotlib.pyplot as plt
import copy
import time

dpath = sys.argv[1]

rox1 = []
rox2 = []
rox3 = []
rox4 = []

for l in open(dpath):
	if l.split()[1] == '1':
		rox1.append(l.split())
	if l.split()[1] == '2':
		rox2.append(l.split())
	if l.split()[1] == '3':
		rox3.append(l.split())
	if l.split()[1] == '4':
		rox4.append(l.split())

rox1 = np.asarray(rox1,dtype='float')
rox2 = np.asarray(rox2,dtype='float')
rox3 = np.asarray(rox3,dtype='float')
rox4 = np.asarray(rox4,dtype='float')

def norm_t(t):
	tmp = copy.copy(t)
	tmp-= tmp[0]
	if tmp[-1] - tmp[0] > 30200.0:
		tmp/=3600.0
		print('time in hours')
	else:
		tmp/=60.0
		print('time in minutes')
		unit = 'min'
	return tmp

def get_unit(t):
	tmp = copy.copy(t)
	tmp-= tmp[0]
	if tmp[-1] - tmp[0] > 30200.0:
		tmp/=3600.0
		unit = 'hr'
	else:
		tmp/=60.0
		unit = 'min'
	return unit


# 40K G10 ring	CX-1080	X151125	LS240 - 1
# 40K DR adapter	CX-1080	X151123	LS240 - 2
# 40K front plate	CX-1080	X151127	LS240 - 3
# 40K readout plate	CX-1080	X157222	LS240 - 4

# 4K optics tube mounting ring	CX-1050	X157057	LS372 - 1
# 4K DR adapter	CX-1050	X156842	LS372 - 4
# 4K back plate	CX-1050	X156836	LS372 - 3


# plt.plot((rox1[:,0]-rox1[0,0])/60./60., rox1[:,2], label='40K G10 ring (ch 1)',linewidth=2)
# plt.plot((rox2[:,0]-rox2[0,0])/60./60., rox2[:,2], label='40K DR adapter (ch 2)',linewidth=2)
# plt.plot((rox3[:,0]-rox2[0,0])/60./60., rox3[:,2], label='40K front plate (ch 3)',linewidth=2)
# plt.plot((rox4[:,0]-rox2[0,0])/60./60., rox4[:,2], label='40K readout plate (ch 4)',linewidth=2)

now = time.time()

day = 1

if day:
	plt.plot((rox1[:,0]-now)/60./60./24., rox1[:,2], label='40K G10 ring (ch 1)',linewidth=2)
	plt.plot((rox2[:,0]-now)/60./60./24., rox2[:,2], label='40K DR adapter (ch 2)',linewidth=2)
	plt.plot((rox3[:,0]-now)/60./60./24., rox3[:,2], label='40K front plate (ch 3)',linewidth=2)
	plt.plot((rox4[:,0]-now)/60./60./24., rox4[:,2], label='40K readout plate (ch 4)',linewidth=2)
	plt.xlabel('time [days]', fontsize=16)

else:
	plt.plot((rox1[:,0]-now)/60./60., rox1[:,2], label='40K G10 ring (ch 1)',linewidth=2)
	plt.plot((rox2[:,0]-now)/60./60., rox2[:,2], label='40K DR adapter (ch 2)',linewidth=2)
	plt.plot((rox3[:,0]-now)/60./60., rox3[:,2], label='40K front plate (ch 3)',linewidth=2)
	plt.plot((rox4[:,0]-now)/60./60., rox4[:,2], label='40K readout plate (ch 4)',linewidth=2)
	plt.xlabel('time [hr]', fontsize=16)


model0=np.loadtxt('model_0WFP.txt',delimiter=',')
model10=np.loadtxt('model_10WFP.txt',delimiter=',')
model30=np.loadtxt('model_30WFP.txt',delimiter=',')
model50=np.loadtxt('model_50WFP.txt',delimiter=',')

hours=range(len(model0[:,0]))
diff=11.53

plt.plot([x-diff for x in hours],model0[:,0],'-',label='40 K Front Plate (model, 0 W)',color='g')
plt.plot([x-diff for x in hours],model0[:,1],'-',label='40 K G10 Ring (model, 0 W)',color='b')
plt.plot([x-diff for x in hours],model0[:,2],'-',label='40 K Rear Shell (model, 0 W)',color='r')

plt.plot([x-diff for x in hours],model10[:,0],'-.',label='40 K Front Plate (model, 10 W)',color='g')
plt.plot([x-diff for x in hours],model10[:,1],'-.',label='40 K G10 Ring (model, 10 W)',color='b')
plt.plot([x-diff for x in hours],model10[:,2],'-.',label='40 K Rear Shell (model, 10 W)',color='r')

plt.plot([x-diff for x in hours],model30[:,0],'--',label='40 K Front Plate (model, 30 W)',color='g')
plt.plot([x-diff for x in hours],model30[:,1],'--',label='40 K G10 Ring (model, 30 W)',color='b')
plt.plot([x-diff for x in hours],model30[:,2],'--',label='40 K Rear Shell (model, 30 W)',color='r')

plt.plot([x-diff for x in hours],model50[:,0],':',label='40 K Front Plate (model, 50 W)',color='g')
plt.plot([x-diff for x in hours],model50[:,1],':',label='40 K G10 Ring (model, 50 W)',color='b')
plt.plot([x-diff for x in hours],model50[:,2],':',label='40 K Rear Shell (model, 50 W)',color='r')

plt.ylabel('Temp [K]', fontsize=16)
plt.legend(loc=0)
plt.grid()
plt.show()
#plt.savefig('ls240_log_latest.png')
plt.clf()


exit()

if  len(sys.argv) == 3:
	ctime = int(sys.argv[2])
	ind = np.where(np.abs(ctime-rox2[:,0])==np.min(np.abs(ctime-rox2[:,0])))[0]
	print("ctime = %i; temp = %.3f K"%(ctime,rox2[ind,5]))
	exit()

	plt.plot(rox2[:,0], rox2[:,5]*1000, label='ch 2')
	plt.axvline(x=ctime, color ='k')

	if np.max(np.abs(rox2[:,5]*1000))>1000:
		plt.ylim(0,np.max(rox2[:,5][rox2[:,5]>0])*1000)
	plt.grid()
	plt.legend()
	plt.ylabel('Temp (K)', fontsize=16)
	plt.xlabel('time [s]', fontsize=16)
	plt.show()

exit()

unit = get_unit(rox2[:,0])

if len(rox2)>2:
	plt.plot(norm_t(rox2[:,0]), rox2[:,5]*1000, label='ch 2')
# if len(rox3)>2:
# 	plt.plot(norm_t(rox3[:,0]), rox3[:,3]*1000, label='ch 3')
# if len(rox4)>2:
# 	plt.plot(norm_t(rox4[:,0]), rox4[:,3]*1000, label='ch 4')


plt.ylabel('Temp (mK)', fontsize=16)
plt.xlabel('time [%s]'%unit, fontsize=16)

plt.legend()
plt.grid()
plt.show()


unit = get_unit(rox2[:,0])

if len(rox2)>2:
	plt.plot(rox2[:,0]-rox2[0,0], rox2[:,5]*1000, label='ch 2')
if len(rox3)>2:
	plt.plot(rox3[:,0]-rox2[0,0], rox3[:,3]*1000, label='ch 3')
if len(rox4)>2:
	plt.plot(rox4[:,0]-rox2[0,0], rox4[:,3]*1000, label='ch 4')


plt.ylabel('Temp (mK)', fontsize=16)
plt.xlabel('time [s]', fontsize=16)

plt.legend()
plt.grid()
plt.show()


lastfew = 1
ind = 4300
unit = get_unit(rox2[-ind:,0])
print(unit)
if lastfew:
	if len(rox2)>2:
		plt.plot(norm_t(rox2[-ind:,0]), rox2[-ind:,5]*1000, label='ch 2')
	# if len(rox3)>2:
	# 	plt.plot(norm_t(rox3[:,0])[-ind:], rox3[:,3][-ind:]*1000, label='ch 3')
	# if len(rox4)>2:
	# 	plt.plot(norm_t(rox4[:,0])[-ind:], rox4[:,3][-ind:]*1000, label='ch 4')

	plt.ylabel('Temp (mK)', fontsize=16)
	plt.xlabel('time [%s]'%unit, fontsize=16)


	plt.legend(loc=2)
	plt.grid()
	plt.show()

exit()

if len(rox2)>2:
	plt.plot(norm_t(rox2[:,0]), rox2[:,4]/1000, label='ch 2')
if len(rox3)>2:
	plt.plot(norm_t(rox3[:,0]), rox3[:,4]/1000, label='ch 3')
if len(rox4)>2:
	plt.plot(norm_t(rox4[:,0]), rox4[:,4]/1000, label='ch 4')

plt.ylabel('Res (kOhm)', fontsize=16)
plt.xlabel('time', fontsize=16)

plt.legend()
plt.grid()
plt.show()


if 'cal' in dpath:

	if len(rox2)>2:
		plt.plot(rox2[:,4]/1000, rox2[:,3]*1000, label='ch 2')
	if len(rox3)>2:
		plt.plot(rox3[:,4]/1000, rox3[:,3]*1000, label='ch 3')
	if len(rox4)>2:
		plt.plot(rox4[:,4]/1000, rox4[:,3]*1000, label='ch 4')

	plt.ylabel('Temp (mK)', fontsize=16)
	plt.xlabel('Res (kOhm)', fontsize=16)

	plt.axis([10,45,40,180])

	plt.legend()
	plt.grid()
	plt.show()
