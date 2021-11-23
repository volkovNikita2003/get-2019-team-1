import spidev
import time
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import numpy as np

directionPin = 27
enablePin = 22
stepPin = 17

spi = spidev.SpiDev()

def initSpiAdc():
    spi.open(0, 0)
    spi.max_speed_hz = 1600000
    print ("SPI for ADC has been initialized")


def deinitSpiAdc():
    spi.close()
    print ("SPI cleanup finished")


def getAdc():
    adcResponse = spi.xfer2([0, 0])
    adc = ((adcResponse[0] & 0x1F) << 8 | adcResponse[1]) >> 1

    return adc


def getMeanAdc(samples):
    sum = 0
    for i in range(samples):
        sum += getAdc()
    
    return int(sum / samples)


def initStepMotorGpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup([directionPin, enablePin, stepPin], GPIO.OUT)
    print ("GPIO for step motor have been initialized")


def deinitStepMotorGpio():
    GPIO.output([directionPin, enablePin, stepPin], 0)
    GPIO.cleanup()
    print ("GPIO cleanup finished")


def step():
    GPIO.output(stepPin, 0)
    time.sleep(0.005)
    GPIO.output(stepPin, 1)
    time.sleep(0.005)
    

def stepForward(n):
    GPIO.output(directionPin, 1)
    GPIO.output(enablePin, 1)

    for i in range(n):
        step()

    GPIO.output(enablePin, 0)


def stepBackward(n):
    GPIO.output(directionPin, 0)
    GPIO.output(enablePin, 1)

    for i in range(n):
        step()

    GPIO.output(enablePin, 0)


def saveMeasures(measures, samplesInMeasure, motorSteps, count):
    filename = 'jet-data {}.txt'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

    with open(filename, "w") as outfile:
        outfile.write('- Jet Lab\n\n')
        outfile.write('- Experiment date = {}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
        outfile.write('- Number of samples in measure = {}\n'.format(samplesInMeasure))
        outfile.write('- Number of motor steps between measures = {}\n'.format(motorSteps))
        outfile.write('- Measures count = {}\n\n'.format(count))
        
        outfile.write('- adc12bit\n')
        np.savetxt(outfile, np.array(measures).T, fmt='%d')


def showMeasures(measures, samplesInMeasure, motorSteps, count):
    print('\nExperiment date = {}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
    print('Number of samples in measure = {}'.format(samplesInMeasure))
    print('Number of motor steps between measures = {}'.format(motorSteps))
    print('Measures count = {}\n'.format(count))
    
    plt.plot(measures)
    plt.show()


def readJetData(filename):
    with open(filename) as f:
        lines = f.readlines()

    steps = 0
    count = 0
    dataLineIndex = 0

    for index, line in enumerate(lines):
        if line[0] != '-' and line[0] != '\n':
            dataLineIndex = index
            break

        if 'steps' in line:
            words = line.split()
            for word in words:
                try:
                    steps = float(word)
                except ValueError:
                    pass

        if 'count' in line:
            words = line.split()
            for word in words:
                try:
                    count = int(word)
                except ValueError:
                    pass

    dataLines = lines[dataLineIndex:]
    data = np.asarray(dataLines, dtype=int)

    return data, steps, count