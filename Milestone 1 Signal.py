#importing the needed packages and libraries
import numpy as np  #to set the array of time,x(t),and frequencies
import matplotlib.pyplot as plt #to plot the graph of x(t) versus t
import sounddevice as sd #to play the sound generated

#setting the time t as the x-axis
t=np.linspace(0, 3,12*1024)

#naming the frequencies from the 4th octave as varibles to be called easily
c4 = 261.62
d4 = 293.66
e4 = 329.62
f4 = 349.23
g4 = 392
a4 = 440
b4 = 493.88

#two arrays to represent the frequencies
F=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
f=[0,a4,c4,d4,0,d4,e4,f4,0,f4,0,f4,g4,e4,0,e4,0,d4,c4,d4,c4]


N=len(f)-1 #setting the umber of pairs N as the length of the frequency array
ti=0
tf=(60/(140*4)) #setting the period of each note to be quarter a beat


x=0 #variable x to represent x(t) as the y-axis
i=1

#accumulating x(t) in a loop
while(i<=N):
    x=x+np.reshape((np.sin(2*f[i]*np.pi*t)+np.sin(2*F[i]*np.pi*t))*[t>=ti]*[t<=tf],np.shape(t))
    i=i+1
    ti+=(60/(140*4))
    tf+=(60/(140*4))

#plotting x(t) versus t
plt.plot(t, x)
plt.xlabel("time")
plt.ylabel("x(t)")

#playing the sound
sd.play(x,3*1024)

