 class Application:
        def __init__(self, app_name, start_time, end_time, app_id):
                self.app_name = app_name
                self.start_time = start_time
                self.end_time = end_time
                self.app_id = app_id

                
class Order:
        def __init__(self, order_id, income, session_id, time):
                self.order_id = order_id
                self.income = income
                self.session_id = session_id
                self.time = time
              

class Link:
        def __init__(self, app_id, session_id, place_id, app_name):
                self.app_id = app_id
                self.session_id = session_id
                self.place_id = place_id
                self.app_name = app_name


class SortedOrder:
        def __init__(self, app_name, revenue):
                self.app_name = app_name
                self.revenue = revenue

                
# Creating empty lists for filling                
apps = []
orders = []
links = []
sapps = []

# Using pandas library, getting data from scv-files in dataframe's
import pandas as pd

a1 = pd.read_csv('apps.csv', parse_dates=['StartTime','EndTime'])       # Parsing input StartTime, EndTime for
o1 = pd.read_csv('orders.csv')                                          # better representation
l1 = pd.read_csv('link_data.csv')

# Переносим данные из dataframe'ов в списки
a2 = a1.get_values()
o2 = o1.get_values()
l2 = l1.get_values()

for row in a2:
    apps.append(Application(row[0], row[1], row[2], row[3]))

for row in o2:
    orders.append(Order(row[0], row[1], row[2], row[3]))

for row in l2:
    links.append(Link(row[0], row[1], row[2], row[3]))

# Сортируем список orders по убыванию
sorted_by_income = sorted(orders, key = lambda session: session.income, reverse = True)

# Связываем между собой данные из списков apps, links, orders.
for s in sorted_by_income:
        for c in links:
                if str.upper(c.session_id) == str.upper(s.session_id):
                        for a in apps:
                                if str.upper(a.app_id) == str.upper(c.app_id):
                                        # Выполняем подсчёт времени выполнения приложений.
                                        dif = str(a.end_time - a.start_time)
                                        time_hours = dif.split(' ')[0]
                                        time_minutes = dif.split(':')[1]
                                        time_seconds = dif.split(':')[2]
                                        time_to_seconds = float(time_hours)*3600 + float(time_minutes)*60 + float(time_seconds)
                                        if time_to_seconds == 0:
                                                continue
                                        # Считаем прибыль/сек, и переводим её в прибыль/час
                                        revenue = round(s.income / time_to_seconds * 3600, 2)
                                        sapps.append(SortedOrder(a.app_name, revenue))

# Сортируем список sapps(сокр. от sortedapps)
sorted_by_revenue = sorted(sapps, key = lambda x: x.revenue, reverse = True)


# Подготавливаем переменные и список для конечного вывода
i = 0
print('Input the number of apps you want to show')
n = input()
n = int(n)
remember = '0'
final = []

for sa in sorted_by_revenue:
        name = sa.app_name.split('.')[2]
        if i == n:
                break
        if final.count(name) > 0:
                continue
        i = i + 1
        final.append(name)

print('For next hour, the most suitable apps are:')
for f in final:
        print('"' + f + '"')
input()
# Конец файла
