#importing the needed packages and libraries
import numpy as np  #to set the array of time,x(t),and frequencies
import matplotlib.pyplot as plt #to plot the graph of x(t) versus t
import sounddevice as sd #to play the sound generated
from scipy.fftpack import fft #to get the fourier transform 

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
plt.xlabel("time")
plt.ylabel("x(t)")
plt.title("x(t) before adding noise")
plt.plot(t, x)

#sd.play(x, 3 *1024)

#generating random noise frequencies
fn1 = np.random.randint(0,512,1)
fn2 = np.random.randint(0,512,1)
noise=(np.sin(2*fn1*np.pi*t))+(np.sin(2*fn2*np.pi*t))

#adding noise to the original signal x
xn=x+noise
#sd.play(xn, 3 *1024)
plt.figure()
plt.xlabel("time")
plt.ylabel("xn(t)")
plt.title("x(t) after adding noise")
plt.plot(t,xn)
#fourier transforms
N=3*1024
f=np.linspace(0, 512,int(N/2))

#fourier transform of x & plotting it
x_f=fft(x)
x_f= 2/N * np.abs(x_f[0:int(N/2)])
plt.figure()
plt.xlabel("frequency")
plt.ylabel("X(F)")
plt.title("X(F) before adding noise")
plt.plot(f,x_f)

#fourier transform of xn (signal containing noise) & plotting it
x_fn=fft(xn)
x_fn= 2/N * np.abs(x_fn[0:int(N/2)])
plt.figure()
plt.xlabel("frequency")
plt.ylabel("Xn(F)")
plt.title("Xn(F) after adding noise")
plt.plot(f,x_fn)


#finding the maximum frequency (peak) of the original signal transform (x)
i=0
maximum=x_f[0]
while i<len(x_f):
    if(x_f[i]>maximum):
        maximum=x_f[i]
    i+=1


#comparing the peaks of the signal containig noise to the maximum of the original
#to get the indices corresponding to noise
noise_indices = [] #array to store the target indices
i=0
while (i<len(x_fn)):
    if(x_fn[i]>maximum+1): #maximum+1 to avoid including the maximum due to double precision errors 
        noise_indices+=[i]
    i+=1
    
#rounding the corresponding frequencies to the nearest integer
#because we are generating random integer noises (random.randint)
noise1=np.round(f[noise_indices[0]])
noise2=np.round(f[noise_indices[1]])    

#removing the noise from the signal containing noise (xn) & plotting it to compare with the original
xfilter = xn-(np.sin(2*np.pi*noise1*t)+np.sin(2*np.pi*noise2*t))   
plt.figure()
plt.xlabel("time")
plt.ylabel("xfilter(t)")
plt.title("xfilter(t) after removing noise")
plt.plot(t, xfilter) 

x_ffilter=fft(xfilter)
x_ffilter= 2/N * np.abs(x_ffilter[0:int(N/2)])
plt.figure()
plt.xlabel("frequency")
plt.ylabel("Xfilter(F)")
plt.title("Xfilter(F) after removing noise")
plt.plot(f,x_ffilter)
#playing the filtered signal to check it is the same as the original   
sd.play(xfilter,3*1024)    
        