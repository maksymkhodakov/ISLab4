from csp_initializer import *
csp = my_csp

counter = 0
var_domains = {}
degree_values = {}

#init empty assignment
def init_assignment_default(csp):
  global var_domains

  #відстеження кількості ітерацій алгоритму
  global counter
  counter = 0
  assignment = {}
  #для кожного класу
  for var in csp[VARIABLES]:
    assignment[var] = None
    #список доменів для кожного класу
    var_domains[var] = csp[DOMAINS].copy()
  return assignment


def getRoom(csp, assignment,var, value):
  rooms = data._rooms
  #сортуємо за кількістю студентів які можуть поміститися в порядку зростання 
  rooms.sort(key=lambda c: c[1])
  
  for r in rooms:
    # Перевірка, чи кількість студентів, яку може вмістити кімната, 
    # не менша за кількість студентів, які повинні відвідувати клас
    if (r[1] >= var._number_of_students):
      free = True
      #перебираємо всі класи
      for k in csp[VARIABLES]:
        #якщо змінна вже призначена
        if (assignment[k] is not None):
          #перевіряємо, чи дана кімната є вже зайнятою
          if (k._room == r and assignment[k] == value):
            free = False
      #повертається перша вільна підходяща кімната
      if free:
       return r

#recursive backtracking
#рекурсивно вибирає та призначає значення для кожної змінної у відповідності до заданих обмежень.
def backtracking(assignment, csp, heuristic):
  global counter
  while True:
    #Якщо призначення повне (кожна змінна має значення), тоді повертається це призначення
    if is_complete(assignment):
      return assignment
    for value in csp[DOMAINS]:
      #Використовується евристика для вибору наступної змінної для призначення.
      var = heuristic(assignment)
      assignment[var] = value

      #відправляємо словник 
      # csp = {VARIABLES: classes,
      #    DOMAINS: meeting_times,
      #    CONSTRAINTS: [same_teacher, same_spec, groups_conflict]
      #    }
      # assigment - словник із класів та доменів
      # var - перший непризначений клас
      # value - поточний meeting_time
      var._room = getRoom(csp,assignment, var, value)

      counter+=1

      # Перевіряється, чи поточне призначення відповідає всім обмеженням. Якщо так, вихід з циклу.
      if is_consistent(assignment, csp[CONSTRAINTS]):    
        break
      else: 
        #Якщо поточне призначення не є сумісним з обмеженнями,
        # скасовується призначення і пробуємо знову
        assignment[var] = None
        var._room = None
  return FAILURE



def backtracking_recursive(assignment, csp, heuristic):
    global counter
    
    # Якщо призначення повне (кожна змінна має значення), тоді повертається це призначення
    if is_complete(assignment):
        return assignment

    # Використовуємо евристику для вибору наступної змінної для призначення.
    var = heuristic(assignment)

    for value in csp[DOMAINS]:
        assignment[var] = value
        var._room = getRoom(csp, assignment, var, value)
        counter += 1

        # Перевіряємо, чи поточне призначення відповідає всім обмеженням. Якщо так, викликаємо рекурсію.
        if is_consistent(assignment, csp[CONSTRAINTS]):
            result = backtracking_recursive(assignment, csp, heuristic)
            if result is not FAILURE:
                return result

        # Якщо поточне призначення не є сумісним з обмеженнями,
        # скасовуємо призначення і пробуємо наступне значення.
        assignment[var] = None
        var._room = None

    return FAILURE




def get_counter_default():
  global counter
  return counter



#simple search 
#вибирає першу непризначену змінну для призначення.
def default_heuristic(assignment):
  res = []
  for i in csp[VARIABLES]:
    if (assignment[i] is None):
      res.append(i)
  return res[0] 
