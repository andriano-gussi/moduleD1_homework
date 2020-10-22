import sys
import requests

auth_params = {
  'key': "299f82365f2c347c66b068c851281dfe",
  'token': "e41bb1b5126b7d237bf6a440476b0043887dbdbbed2adf782e558c605ad3e16e",}

base_url = "https://api.trello.com/1/{}"

board_id = "MuMkzKqZ"

def read():
  column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

  for column in column_data:
    task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
    # рядом с именем колонки выводим количество задач, записанных в ней
    print("\n{} ({}):".format(column['name'], len(task_data)))
    if not task_data:
      print('\t' + 'нет задач')
      continue
    for task in task_data:
      print(' -' + task['name'] + ';')

def create(name, column_name):
  """ создает новую задачу в конкретной колонке """
  column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
  for column in column_data:
    if column['name'] == column_name:
      requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
      break
  print("Задача успешно добавлена!")

def create_column(name):
  """ создает новую колонку """
  requests.post(base_url.format('boards') + '/' + board_id + '/lists', data={'name': name, 'idBoard': board_id, 'pos': 'bottom', **auth_params})
  print("Колонка успешно создана!")

def move(name, column_name):
  """ перемещает существующую задачу в конкретную существующую колонку """
  column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
  list_column_names = [] 
  same_tasks = [] # переменная для хранения данных по задачам, имя которых аналогично переданному имени в функцию
  for column in column_data:
    column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
    list_column_names.append(column['name']) # создание списка наименований всех колонок

    # если есть задача, имя которой совпадает с именем задачи, переданной в функцию, то
    # добавляем в same_tasks кортеж из имени колонки, задачи и id этой задачи: 
    for task in column_tasks:
      if task['name'] == name:
         same_tasks.append((column['name'], task['name'], task['id']))
  
  # проверка переданных в функцию данных на валидность:
    # если переданное имя не найдено среди имеющихся задач:
  if not same_tasks:
    print("Невозможно переместить задачу, которой не существует! (проверьте введенные данные или создайте задачу с таким именем)")
    return
    # если  переданное имя колонки не найдено в списке существующих колонок:
  elif column_name not in list_column_names:
    print("Невозможно переместить задачу в колонку, которая не существует! (проверьте введенные данные или создайте колонку с таким именем)")
    return
    # если имеется больше одной задачи с именем, совпадающем с переданным в функцию
  elif len(same_tasks) > 1:
    print("Таких задач несколько:")
    for key, item in enumerate(same_tasks):
      print('{}. колонка "{}": задача "{}" (id = {})'.format((key + 1), item[0], item[1], item[2] ))
    # сохраняем выбор пользователя в переменную:
    choise = int(input("Выберите порядковый номер необходимой задачи из списка: "))-1
  else:
    # если задача одна, то в переменную записываем ссылку на первый элемент списка same_tasks:
    choise = 0

  # находим необходимую колонку и перемещаем в нее задачу:
  for column in column_data:
    if column['name'] == column_name:
      requests.put(base_url.format('cards') + '/' + same_tasks[choise][2] + '/idList', data={'value': column['id'], **auth_params})
      break
  print("Перемещение задачи выполнено успешно!")

if __name__ == "__main__":
  if len(sys.argv) <= 2:
    read()
  elif sys.argv[1] == 'create':
    create(sys.argv[2], sys.argv[3])
  elif sys.argv[1] == 'move':
    move(sys.argv[2], sys.argv[3])
  elif sys.argv[1] == 'create_column':
    create_column(sys.argv[2])