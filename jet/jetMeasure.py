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
    f.initStepMotorGpio()
    f.stepBackward(500)
    s = []
    samp = 15
    count = 100
    step = 10
    for i in range(count):
        s.append(f.getMeanAdc(samp))
        f.stepForward(step)
    f.saveMeasures(s, samp, step, count)
    plt.plot(s)
    plt.show()
    f.stepBackward(500)
finally:
    f.deinitSpiAdc()
    f.deinitStepMotorGpio()