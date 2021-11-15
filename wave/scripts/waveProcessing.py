import numpy as np
import matplotlib.pyplot as plt
def readWaveData(filename):
    with open(filename) as f:
        lines = f.readlines()

    duration = 0
    count = 0
    dataLineIndex = 0

    for index, line in enumerate(lines):
        if line[0] != '-' and line[0] != '\n':
            dataLineIndex = index
            break

        if 'duration' in line:
            words = line.split()
            for word in words:
                try:
                    duration = float(word)
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
    
    return data, duration, count
x = []
y = []
def masxy(filename, h):
    data, duration, count = readWaveData(filename)
    for n in range(count):
        x.append(h)
        y.append(data[n])

masxy("20mm.txt", 20)
masxy("40mm.txt", 40)
masxy("60mm.txt", 60)
masxy("80mm.txt", 80)
masxy("100mm.txt", 100)
masxy("112mm.txt", 112)

koaf = np.polyfit(x, y, 3)
print(koaf)
x1 = []
for n in np.arange (0.0, 121.0, 0.1):
    x1.append(n)
array = np.polyval(koaf, x1)

#строим график
w = 16
h = 10
dpi = 300
fig, ax = plt.subplots(figsize=(w,h), dpi=dpi)
ax.plot(x1, array, 
        linestyle = '-', linewidth = 3, color = 'blue',
        label = "Калибровочная ф-ия",
        marker = '*', markersize = 20, markevery=[200, 400, 600, 800, 1000, 1120]
        )
ax.legend() # легенда
ax_x_min = 10
ax_x_max = 130
ax_y_min = 1000
ax_y_max = 3000
ax.axis( [ax_x_min, ax_x_max, ax_y_min, ax_y_max] ) # макс и мин занчения по осям
#  Добавляем подписи к осям:
ax.set_xlabel('Высота (мм)')
ax.set_ylabel('Отсчеты АЦП')
#заголовок
ax.set_title("Калибровочный график з-ти АЦП от у-ня воды", loc = "center", wrap=True)

# сетка
ax.minorticks_on()
#  Определяем внешний вид линий основной сетки:
ax.grid(which='major',
        color = 'gray',  #  цвет линий
        linewidth = 1, #  толщина
        linestyle = '-'
        )
#  Определяем внешний вид линий вспомогательной сетки:
ax.grid(which='minor',
        color = 'gray',  #  цвет линий
        linewidth = 0.5, #  толщина
        linestyle = '--'
        )



#сохранение графика
fig.savefig("calib.png")


# def srznach(filename):
#     data, duration, count = readWaveData(filename)
#     sr = 0
#     for n in range(count):
#         sr += data[n]
#     return sr / count
# zn = []
# zn.append(srznach("40 mm.txt"))
# zn.append(srznach("60 mm.txt"))
# zn.append(srznach("80 mm.txt"))
# zn.append(srznach("100 mm.txt"))
# zn.append(srznach("120 mm.txt"))

data, duration, count = readWaveData("example/wave.txt")

# flag = True
# d = 0
# k = 0
# for i in range(len(array) - 1):
#     if(array[i] > array[i + 1]):
#         flag = False
#         d += 1
#         if (array[i] - array[i + 1] > k):
#             k = array[i] - array[i + 1]
# print (flag, d, k)

# value = int(input()) -- data
def bin(i):
    mid = len(array) // 2
    low = 0
    high = len(array) - 1
    
    while array[mid] != data[i] and low <= high:
        if data[i] > array[mid]:
            low = mid + 1
        else:
            high = mid - 1
        mid = (low + high) // 2
    return mid
vysota = []
t = []
for n in range(count // 6):
    vysota.append(x1[bin(n)])
for n in range(count // 6):
    if n == 0:
        t.append(0)
    else:
        t.append(t[n - 1] + duration / count)
plt.plot(t, vysota)
w = 16
h = 10
dpi = 300
fig, ax = plt.subplots(figsize=(w,h), dpi=dpi)
ax.plot(t[:587], vysota[:587], 
        linestyle = '-', linewidth = 3, color = 'blue',
        label = "Ожидание волны"
        )
ax.plot(t[587:], vysota[587:], 
        linestyle = '-', linewidth = 3, color = 'red',
        label = "Уровень воды в кювете"
        )
ax.legend() # легенда
ax_x_min = 0
ax_x_max = 5
ax_y_min = 20
ax_y_max = 130
ax.axis( [ax_x_min, ax_x_max, ax_y_min, ax_y_max] ) # макс и мин занчения по осям
#  Добавляем подписи к осям:
ax.set_xlabel('Время (с)')
ax.set_ylabel('Высота (мм)')
#заголовок
ax.set_title("Уровень воды в кювете после открытия торцевой дверцы", loc = "center", wrap=True)

# сетка
ax.minorticks_on()
#  Определяем внешний вид линий основной сетки:
ax.grid(which='major',
        color = 'gray',  #  цвет линий
        linewidth = 1, #  толщина
        linestyle = '-'
        )
#  Определяем внешний вид линий вспомогательной сетки:
ax.grid(which='minor',
        color = 'gray',  #  цвет линий
        linewidth = 0.5, #  толщина
        linestyle = '--'
        )

#добавление текста
xtext = (ax_x_max - ax_x_min)/100*1
ytext = (ax_y_max - ax_y_min)/100*60
ax.text(xtext, ytext, "L = 0,71м \nt = 0,56c \nV = 1,27 м/с",
        color = 'black',    #  цвет шрифта
        fontsize = 14)
ax.vlines(t[587], ax_y_min, ax_y_max,
          color = 'orange',    #  цвет
          linewidth = 3,    #  ширина
          linestyle = ':')    #  начертание

#сохранение графика
fig.savefig("graph.png")
#plt.show()


#plt.show()