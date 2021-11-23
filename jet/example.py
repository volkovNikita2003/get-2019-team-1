import spidev
import jetFunctions as f
import time
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import numpy as np

directionPin = 27
enablePin = 22
stepPin = 17

spi = spidev.SpiDev()
try:
    f.initSpiAdc()
    s = []
    samp = 10
    count = 500
    for i in range(count):
        s.append(f.getMeanAdc(samp))
    f.saveMeasures(s, samp, 0, count)
    plt.plot(s)
    plt.show()
finally:
    f.deinitSpiAdc()
    
