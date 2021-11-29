import numpy as np
import math
import matplotlib.pyplot as plt

def read(filename):
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

measures0, steps0, lenth0 = read("00 Pa.txt")
measures7, steps7, lenth7 = read("35 Pa.txt")
m07 = np.hstack([measures0, measures7])
y= []
for i in range(lenth0):
    y.append(0)
for i in range(lenth0):
    y.append(35)
P = np.polyfit(y,m07,1) # АЦП от паскалей
print(P)
X = [0, 35]
Y = np.polyval(P,X)
P1 = np.polyfit(m07,y,1)# Паскали от АЦП
#построение графика
w = 16
h = 10
dpi = 400
fig, ax = plt.subplots(figsize=(w,h), dpi=dpi)
ax.plot(X, Y,
        linestyle = '-', linewidth = 2.7 , color = 'red',
        marker = 'o', markersize = 9,
        label = 'P = {:.3f} * N {:.2f} [Па]'.format(P1[0], P1[1])
        )

ax.legend() # легенда
#  Добавляем подписи к осям:
ax.set_xlabel('Давление (Па)')
ax.set_ylabel('Отсчеты АЦП')
#заголовок
ax.set_title("Калибровочный график зависимости показаний АЦП от давления", loc = "center", wrap=True)

# сетка
#  Прежде чем рисовать вспомогательные линии необходимо включить второстепенные деления осей:
ax.minorticks_on()
#  Определяем внешний вид линий основной сетки:
ax.grid(which='major',
        color = 'blue',  #  цвет линий
        linewidth = 1, #  толщина
        linestyle = '-'
        )
#  Определяем внешний вид линий вспомогательной сетки:
ax.grid(which='minor',
        color = 'blue',  #  цвет линий
        linewidth = 0.5, #  толщина
        linestyle = '--'
        )
#сохранение графика
fig.savefig("graph.png")


#калибровка расстояния
k1=0.0056
X1=[0,900]
Y1=[0, 5.04]
#построение графика
w = 8
h = 5
dpi = 400
fig, ax = plt.subplots(figsize=(w,h), dpi=dpi)
ax.plot(X1, Y1,
        linestyle = '-', linewidth = 2.7 , color = 'red',
        marker = 'o', markersize = 9,
        label = 'X = {} * step [м]'.format(k1)
        )

ax.legend() # легенда
#  Добавляем подписи к осям:
ax.set_xlabel('Количиство шагов')
ax.set_ylabel('Перемещение трубки Пито [см]')
#заголовок
ax.set_title("Калибровочный график зависимости перемещения трубки Пито от шага двигателя", loc = "center", wrap=True)
# сетка
#  Прежде чем рисовать вспомогательные линии необходимо включить второстепенные деления осей:
ax.minorticks_on()
#  Определяем внешний вид линий основной сетки:
ax.grid(which='major',
        color = 'blue',  #  цвет линий
        linewidth = 1, #  толщина
        linestyle = '-'
        )
#  Определяем внешний вид линий вспомогательной сетки:
ax.grid(which='minor',
        color = 'blue',  #  цвет линий
        linewidth = 0.5, #  толщина
        linestyle = '--'
        )
#сохранение графика
fig.savefig("distance-calibration.png")


#скорость
def p2v(filename):
    measures, step, leny = read(filename)
    u=[0]*leny
    step= step*k1*10
    Pl = np.polyval(P1,measures)
    steps = [0]*leny
    steps[0]= -step*leny//2
    for i in range(leny):
        if Pl[i]<0:
            Pl[i]=0
        u[i] = math.sqrt(2*Pl[i]/1.2)
        if (i>0):
            steps[i] = step + steps[i-1]
    return u, steps

# def graf(filename,color):
#     u,steps=p2v("jet-starter-kit/data example/{}.txt".format(filename))
#     st = 0
#     if filename!="00 mm" and filename!="10 mm" and filename!="20 mm" and filename!="30 mm":
#         k =max(u)
#         for i in range(len(steps)):
#             if u[i]==k:
#                 st=steps[i]
#                 break
#         for i in range(len(steps)):
#             steps[i]-=st
#     else:
#         for i in range(len(steps)):
#             steps[i]+=1.35
#     ax.plot(steps, u,
#             linestyle='-', linewidth=2.7, color=color,
#             label='Q = {} '.format(filename)
#             )
#     return steps,u,st

#рабочий вариант функции
# def graf(filename,color):
#     u,steps=p2v("{}.txt".format(filename))
#     id_min = id_max = 0
#     for i in range(u.index(max(u)), len(steps), 1):
#         if u[i] == 0:
#             id_max = i
#             break
#     for i in range(u.index(max(u)), -1, -1):
#         if u[i] == 0:
#             id_min = i
#             break
#     id_average = (id_min + id_max)//2
#     middle = steps[id_average]
#     for i in range(len(steps)):
#         steps[i] -= middle
#
#     ax.plot(steps, u,
#             linestyle='-', linewidth=2.7, color=color,
#             label='Q = {} '.format(filename)
#             )
#
#     return steps,u,id_min, id_max

def graf(filename,color):
    u,steps=p2v("{}.txt".format(filename))
    id_min = id_max = 0
    for i in range(len(steps), 0, -1):
        if u[i-1] != 0:
            id_max = i
            break
    for i in range(len(steps)-1):
        if u[i+1] != 0:
            id_min = i
            break
    id_average = (id_min + id_max)//2
    middle = steps[id_average]
    for i in range(len(steps)):
        steps[i] -= middle

    ax.plot(steps, u,
            linestyle='-', linewidth=2.7, color=color,
            label='Q = {} '.format(filename)
            )

    return steps,u,id_min, id_max
#построение графика
w = 16
h = 10
dpi = 400
fig, ax = plt.subplots(figsize=(w,h), dpi=dpi)
# steps,u,st=graf("00 mm","red")
# steps,u,st=graf("10 mm","gold")
# steps,u,st=graf("20 mm","navy")
# steps,u,st=graf("30 mm","black")
# steps,u,st=graf("40 mm","gray")
# steps,u,st=graf("50 mm","orange")
# steps,u,st=graf("60 mm","maroon")
# steps,u,id_min,id_max=graf("70 mm","peru")
#steps,u,st=graf("80 mm","y")
#steps,u,st=graf("90 mm","tomato")
#steps,u,st=graf("100 mm","lime")


# def leg(steps,u):
#     r=100
#     Q=0
#     Q1=0
#     Q2=0
#     for i in range(len(steps)//2):
#         if u[len(steps)//2-i]==0:
#             r=int(steps[len(steps)//2-i])
#             break
#     if r!=100:
#         for i in range(abs(r)):
#             Q1=steps[len(steps)//2-i]*u[len(steps)//2-i]/1000+Q1
#             Q2=steps[len(steps)//2+i]*u[len(steps)//2+i]/1000+Q2
#     Q=3.14*1.2*1000*0.00056*(abs(Q2)+abs(Q1))*10
#     print(Q1,Q2)
#     print(r)
#     return Q
def leg(steps,u):
    Q1 = 0
    Q2 = 0
    Q = 0
    for i in range(steps.index(0), id_max, 1):
        Q1=steps[i]*u[i]/1000+Q1
    for i in range(id_min, steps.index(0), 1):
        Q2 = steps[i] * u[i] / 1000 + Q2
    Q=3.14*1.2*1000*0.00056*(abs(Q2)+abs(Q1))*10
    # print(Q1,Q2)
    # print("Q = ", Q)
    return Q

filenames = ["00 mm", "10 mm", "20 mm", "30 mm", "40 mm", "50 mm", "60 mm", "70 mm"]
colors = ["red", "gold", "navy","black","gray","orange","maroon","peru"]
Q = []
for i in range(len(filenames)):
    steps,u,id_min,id_max = graf(filenames[i], colors[i])
    Q.append(leg(steps, u))
    print(filenames[i], Q[i])

# Q=leg(steps,u)
# print(Q)
ax.legend() # легенда
#  Добавляем подписи к осям:
ax.set_xlabel('Положение трубки Пито относительно центра струи [мм]')
ax.set_ylabel('Скорость воздуха [м/с]')
#заголовок
ax.set_title("Скорость потока воздуха в сечении затопленной струи", loc = "center", wrap=True)

# сетка
#  Прежде чем рисовать вспомогательные линии необходимо включить второстепенные деления осей:
ax.minorticks_on()
#  Определяем внешний вид линий основной сетки:
ax.grid(which='major',
        color = 'blue',  #  цвет линий
        linewidth = 1, #  толщина
        linestyle = '-'
        )
#  Определяем внешний вид линий вспомогательной сетки:
ax.grid(which='minor',
        color = 'blue',  #  цвет линий
        linewidth = 0.5, #  толщина
        linestyle = '--'
        )
#сохранение графика
fig.savefig("velocity-outgo.png")