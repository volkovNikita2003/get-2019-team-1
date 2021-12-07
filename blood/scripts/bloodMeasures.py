import bloodFunctions as b
import time
import matplotlib.pyplot as plt
def calibration(mm):
    print("Калибровка " + str(mm))
    data = []
    start = time.time()
    finish = start
    while (finish - start) < 10:
        data.append(b.getAdc())
        finish = time.time()
    b.save(data, start, finish)
    plt.plot(data)
    plt.show()
    print("Калибровка завершена\n")

def experiment():
    print("Эксперимент")
    data = []
    start = time.time()
    finish = start
    while (finish - start) < 60:
        data.append(b.getAdc())
        finish = time.time()
    b.save(data, start, finish)
    plt.plot(data)
    plt.show()
    print("Эксперимент завершен\n")

b.initSpiAdc()
try:
    input("Нажмите кнопку")
    experiment()
    # Mm =, 80, 120, 160]
    # for i in range(4):
    #     input("Нажмите кнопку")
    #     calibration(Mm[i])
    # for i in range(2):
    #     input("Нажмите кнопку")
    #     experiment()
finally: 
    b.deinitSpiAdc()