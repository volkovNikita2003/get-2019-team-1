from bloodFunctions import read
import numpy as np
import matplotlib.pyplot as plt

# определенное руками
rest_pulse_value = 63 # пульс до упражнений
rest_pressure = [118, 79] # верхнее и нижнее давления до упражнений
rest_pressure_time = [10.2, 20.2] # время верхнего и нижнего давлений до упражнений
fitness_pulse_value = 67 # пульс после упражнений
fitness_pressure = [146, 79] # верхнее и нижнее давления после упражнений
fitness_pressure_time = [4.75, 20.2] # время верхнего и нижнего давлений после упражнений


########################################
#   Pressure calibration
########################################

# считываем данные из всех файлов и усредняем значения
pressureADC = np.array( [np.mean(read("{} mmHg.txt".format(i))[0], dtype=int) for i in ["40", "80", "120", "160"]], dtype=int )
pressureHg = np.array( [i for i in ["40", "80", "120", "160"]], dtype=int )

# коэфициенты прямой зависимости давления от АЦП
p_ADC_to_Hg = np.polyfit(pressureADC, pressureHg, 1)
print(p_ADC_to_Hg)

# начало построение калибровочного графика
# w = 8
# h = 5
# dpi = 400
# fig, ax = plt.subplots(figsize=(w,h), dpi=dpi)
#
# ax.scatter(pressureHg, pressureADC,
#            label="Измерения", c="blue", s=40, marker='*', alpha=1)
#
# ax.plot(pressureHg, pressureADC,
#         linestyle='-', linewidth=1.5, color='orange',
#         label="P = {:.3f} * N - {:.2f} [мм.рт.ст.]".format(p_ADC_to_Hg[0], abs(p_ADC_to_Hg[1])),
#         )
#
# ax.legend(loc="upper left") # легенда
#
# # макс и мин занчения по осям
# ax_x_min = min(pressureHg) - 5/100 * (max(pressureHg) - min(pressureHg)) # на 5% длины всего графика вниз от минимума
# ax_x_max = max(pressureHg) + 5/100 * (max(pressureHg) - min(pressureHg)) # на 5% длины всего графика вверх от максимума
# ax_y_min = min(pressureADC) - 5/100 * (max(pressureADC) - min(pressureADC))
# ax_y_max = max(pressureADC) + 5/100 * (max(pressureADC) - min(pressureADC))
# ax.axis( [ax_x_min, ax_x_max, ax_y_min, ax_y_max] )
#
# # Добавляем подписи к осям:
# ax.set_xlabel('Давление [мм.рт.ст.]')
# ax.set_ylabel('Отсчеты АЦП')
#
# # заголовок графика
# ax.set_title("Калибровочный график зависимости показаний АЦП от давления", loc = "center", wrap=True)
#
# # сетка
# ax.minorticks_on()
# # Определяем внешний вид линий основной сетки:
# ax.grid(which='major',
#         color = 'gray',  # цвет линий
#         linewidth = 1, # толщина
#         linestyle = '-'
#         )
# # Определяем внешний вид линий вспомогательной сетки:
# ax.grid(which='minor',
#         color = 'gray',  # цвет линий
#         linewidth = 0.5, # толщина
#         linestyle = '--'
#         )
#
# #сохранение графика
# fig.savefig("pressure-calibration.png")
# конец построения калибровочного графика




########################################
#   Experiment before exercise
########################################

rest_samples_ADC, rest_duration, rest_len = read("rest.txt") # чтение из файла
rest_samples_Hg = np.polyval(p_ADC_to_Hg, rest_samples_ADC) # преобразование АЦП в давление
# rest_time - значения времени проведения соответсвующих измерений, rest_period - период измерений
rest_time, rest_period = np.linspace(0, rest_duration, num=rest_len, endpoint=True, retstep=True)

# обрезание графика
rest_samples_Hg = rest_samples_Hg[:rest_len//2]
rest_time = rest_time[:rest_len//2]

# начало построения графика давления до упражнений
# w = 8
# h = 5
# dpi = 400
# fig, ax = plt.subplots(figsize=(w, h), dpi=dpi)
#
# # маркеры далений
# ax.scatter(rest_pressure_time, rest_pressure,
#            marker='*', c="red", s=10, alpha=1, zorder=2)
#
# # подписи маркеров
# ax.text(rest_pressure_time[0]*1.05, rest_pressure[0]*1.05, "Systole",
#         color='black', fontsize=10)
# ax.text(rest_pressure_time[1]*1.05, rest_pressure[1]*1.05, "Diastole",
#         color='black', fontsize=10)
#
# ax.plot(rest_time, rest_samples_Hg,
#         linestyle='-', linewidth=1.5, color='blue', zorder=1,
#         label="Давление - {}/{} [мм.рт.ст.]".format(rest_pressure[0], rest_pressure[1])
#         # label="P = {:.3f} * N - {:.2f} [мм.рт.ст.]".format(p_ADC_to_Hg[0], abs(p_ADC_to_Hg[1])),
#         )
#
# ax.legend(loc="upper right") # легенда
#
# # макс и мин занчения по осям
# ax_x_min = min(rest_time) - 5/100 * (max(rest_time) - min(rest_time)) # на 5% длины всего графика вниз от минимума
# ax_x_max = max(rest_time) + 5/100 * (max(rest_time) - min(rest_time)) # на 5% длины всего графика вверх от максимума
# ax_y_min = min(rest_samples_Hg) - 5/100 * (max(rest_samples_Hg) - min(rest_samples_Hg))
# ax_y_max = max(rest_samples_Hg) + 5/100 * (max(rest_samples_Hg) - min(rest_samples_Hg))
# ax.axis( [ax_x_min, ax_x_max, ax_y_min, ax_y_max] )
#
# # Добавляем подписи к осям:
# ax.set_xlabel('Время [с]')
# ax.set_ylabel('Давление [мм.рт.ст.]')
#
# # заголовок графика
# ax.set_title("Артериальное давление до физической нагрузки", loc = "center", wrap=True)
#
# # сетка
# ax.minorticks_on()
# # Определяем внешний вид линий основной сетки:
# ax.grid(which='major',
#         color = 'gray',  # цвет линий
#         linewidth = 1, # толщина
#         linestyle = '-'
#         )
# # Определяем внешний вид линий вспомогательной сетки:
# ax.grid(which='minor',
#         color = 'gray',  # цвет линий
#         linewidth = 0.5, # толщина
#         linestyle = '--'
#         )
#
# #сохранение графика
# fig.savefig("rest-pressure.png")
# конец построения графика давления до упражнений

# график пульса
f = 25 # количество измерений в секунду на графике пульса
step = int(rest_len/rest_duration/f)
rest_pulse = [ rest_samples_Hg[i+step] - rest_samples_Hg[i] for i in range(0, len(rest_samples_Hg)-step, step) ]
rest_time_pulse = [rest_time[i+step] for i in range(0, len(rest_samples_Hg)-step, step)]

# начало построения графика пульса до упражнений
# w = 8*2
# h = 5
# dpi = 400
# fig, ax = plt.subplots(figsize=(w, h), dpi=dpi)
#
# ax.plot(rest_time_pulse, rest_pulse,
#         linestyle='-', linewidth=1.5, color='blue',
#         label="Пульс - {} [уд/мин]".format(rest_pulse_value)
#         # label="P = {:.3f} * N - {:.2f} [мм.рт.ст.]".format(p_ADC_to_Hg[0], abs(p_ADC_to_Hg[1])),
#         )
#
# ax.legend(loc="upper right") # легенда
#
# # макс и мин занчения по осям
# # ax_x_min = min(rest_time) - 5/100 * (max(rest_time) - min(rest_time)) # на 5% длины всего графика вниз от минимума
# # ax_x_max = max(rest_time) + 5/100 * (max(rest_time) - min(rest_time)) # на 5% длины всего графика вверх от максимума
# # ax_y_min = min(rest_pulse) - 5/100 * (max(rest_pulse) - min(rest_pulse))
# # ax_y_max = max(rest_pulse) + 5/100 * (max(rest_pulse) - min(rest_pulse))
# ax_x_min = 0
# ax_x_max = 30
# ax_y_min = -1.5
# ax_y_max = 1.5
# ax.axis( [ax_x_min, ax_x_max, ax_y_min, ax_y_max] )
#
# # Добавляем подписи к осям:
# ax.set_xlabel('Время [с]')
# ax.set_ylabel('Изменение давления в артерии [мм.рт.ст.]')
#
# # заголовок графика
# ax.set_title("Пульс до физической нагрузки", loc = "center", wrap=True)
#
# # сетка
# ax.minorticks_on()
# # Определяем внешний вид линий основной сетки:
# ax.grid(which='major',
#         color = 'gray',  # цвет линий
#         linewidth = 1, # толщина
#         linestyle = '-'
#         )
# # Определяем внешний вид линий вспомогательной сетки:
# ax.grid(which='minor',
#         color = 'gray',  # цвет линий
#         linewidth = 0.5, # толщина
#         linestyle = '--'
#         )
#
# #сохранение графика
# fig.savefig("rest-pulse.png")
# конец построения графика пульса до упражнений





########################################
#   Experiment after exercise
########################################

fitness_samples_ADC, fitness_duration, fitness_len = read("fitness.txt") # чтение из файла
fitness_samples_Hg = np.polyval(p_ADC_to_Hg, fitness_samples_ADC) # преобразование АЦП в давление
# fitness_time - значения времени проведения соответсвующих измерений, fitness_period - период измерений
fitness_time = np.linspace(0, fitness_duration, num=fitness_len, endpoint=True, retstep=False)

# обрезание графика
fitness_samples_Hg = fitness_samples_Hg[:rest_len//2]
fitness_time = fitness_time[:rest_len//2]

# начало построения графика давления после упражнений
w = 8
h = 5
dpi = 400
fig, ax = plt.subplots(figsize=(w, h), dpi=dpi)

# маркеры далений
ax.scatter(fitness_pressure_time, fitness_pressure,
           marker='*', c="red", s=10, alpha=1, zorder=2)

# подписи маркеров
ax.text(fitness_pressure_time[0]*1.05, fitness_pressure[0]*1.05, "Systole",
        color='black', fontsize=10)
ax.text(fitness_pressure_time[1]*1.05, fitness_pressure[1]*1.05, "Diastole",
        color='black', fontsize=10)

ax.plot(fitness_time[:rest_len//2], fitness_samples_Hg[:rest_len//2],
        linestyle='-', linewidth=1.5, color='orange', zorder=1,
        label="Давление - {}/{} [мм.рт.ст.]".format(fitness_pressure[0], fitness_pressure[1])
        # label="P = {:.3f} * N - {:.2f} [мм.рт.ст.]".format(p_ADC_to_Hg[0], abs(p_ADC_to_Hg[1])),
        )

ax.legend(loc="upper right") # легенда

# макс и мин занчения по осям
ax_x_min = min(fitness_time) - 5/100 * (max(fitness_time) - min(fitness_time)) # на 5% длины всего графика вниз от минимума
ax_x_max = max(fitness_time) + 5/100 * (max(fitness_time) - min(fitness_time)) # на 5% длины всего графика вверх от максимума
ax_y_min = min(fitness_samples_Hg) - 5/100 * (max(fitness_samples_Hg) - min(fitness_samples_Hg))
ax_y_max = max(fitness_samples_Hg) + 5/100 * (max(fitness_samples_Hg) - min(fitness_samples_Hg))
ax.axis( [ax_x_min, ax_x_max, ax_y_min, ax_y_max] )

# Добавляем подписи к осям:
ax.set_xlabel('Время [с]')
ax.set_ylabel('Давление [мм.рт.ст.]')

# заголовок графика
ax.set_title("Артериальное давление до физической нагрузки", loc = "center", wrap=True)

# сетка
ax.minorticks_on()
# Определяем внешний вид линий основной сетки:
ax.grid(which='major',
        color = 'gray',  # цвет линий
        linewidth = 1, # толщина
        linestyle = '-'
        )
# Определяем внешний вид линий вспомогательной сетки:
ax.grid(which='minor',
        color = 'gray',  # цвет линий
        linewidth = 0.5, # толщина
        linestyle = '--'
        )

#сохранение графика
fig.savefig("fitness-pressure.png")
# конец построения графика давления до упражнений


# график пульса
f = 25 # количество измерений в секунду на графике пульса
step = int(fitness_len/fitness_duration/f)
fitness_pulse = [ fitness_samples_Hg[i+step] - fitness_samples_Hg[i] for i in range(0, len(fitness_samples_Hg)-step, step) ]
fitness_time_pulse = [fitness_time[i+step] for i in range(0, len(fitness_samples_Hg)-step, step)]

# начало построения графика пульса до упражнений
w = 8*2
h = 5
dpi = 400
fig, ax = plt.subplots(figsize=(w, h), dpi=dpi)

ax.plot(fitness_time_pulse, fitness_pulse,
        linestyle='-', linewidth=1.5, color='orange',
        label="Пульс - {} [уд/мин]".format(fitness_pulse_value)
        # label="P = {:.3f} * N - {:.2f} [мм.рт.ст.]".format(p_ADC_to_Hg[0], abs(p_ADC_to_Hg[1])),
        )

ax.legend(loc="upper right") # легенда

# макс и мин занчения по осям
# ax_x_min = min(fitness_time) - 5/100 * (max(fitness_time) - min(fitness_time)) # на 5% длины всего графика вниз от минимума
# ax_x_max = max(fitness_time) + 5/100 * (max(fitness_time) - min(fitness_time)) # на 5% длины всего графика вверх от максимума
# ax_y_min = min(fitness_pulse) - 5/100 * (max(fitness_pulse) - min(fitness_pulse))
# ax_y_max = max(fitness_pulse) + 5/100 * (max(fitness_pulse) - min(fitness_pulse))
ax_x_min = 0
ax_x_max = 30
ax_y_min = -3
ax_y_max = 3
ax.axis( [ax_x_min, ax_x_max, ax_y_min, ax_y_max] )

# Добавляем подписи к осям:
ax.set_xlabel('Время [с]')
ax.set_ylabel('Изменение давления в артерии [мм.рт.ст.]')

# заголовок графика
ax.set_title("Пульс до физической нагрузки", loc = "center", wrap=True)

# сетка
ax.minorticks_on()
# Определяем внешний вид линий основной сетки:
ax.grid(which='major',
        color = 'gray',  # цвет линий
        linewidth = 1, # толщина
        linestyle = '-'
        )
# Определяем внешний вид линий вспомогательной сетки:
ax.grid(which='minor',
        color = 'gray',  # цвет линий
        linewidth = 0.5, # толщина
        linestyle = '--'
        )

#сохранение графика
fig.savefig("fitness-pulse.png")
# конец построения графика пульса до упражнений