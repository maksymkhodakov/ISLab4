from data import *

data = Data()
classes = data.classes

# масив чисел від 0 до 29
meeting_times = data.get_domains()

DOMAINS = "DOMAINS"
VARIABLES = "VARIABLES"
CONSTRAINTS = "CONSTRAINTS"
FAILURE = "FAILURE"


# перевіряє, чи всі змінні мають значення
def is_complete(assignment):
    return None not in (assignment.values())


# вибирає непризначену змінну зі списку змінних
def select_unassigned_variable(variables, assignment):
    for var in variables:
        if assignment[var] is None:
            return var


# перевіряє, чи поточне assignment задовольняє всі обмеження constraints
def is_consistent(assignment, constraints):
    for constraint_violated in constraints:
        if constraint_violated(assignment):
            return False
    return True


def equal(a, b): return a is not None and b is not None and a == b


# Повертає список класів, які мають призначені значення
def get_var(assignment):
    arr = []
    for i in assignment.keys():
        newClass = i
        if assignment[i] is not None:
            arr.append(newClass)
    return arr


# функції обмежень

# Однаковий викладач, різні класи і однаковий meeting-time - до побачення
def same_teacher(assignment):
    arr = get_var(assignment)
    if len(arr) == 1:
        return False
    for i in arr:
        for j in arr:
            if equal(i._teacher, j._teacher) and i != j and assignment[i] == assignment[j]:
                return True
    return False


# якщо однакові спеціальності, різні класи, однаковий meeting time і хоча б один з класів - лекція - не проходить
# тому що для однієї спеціальності лекції не можуть пропускатися.
#  Не може бути двох лекцій одночасно або практика під час лекції
def same_spec(assignment):
    arr = get_var(assignment)
    if len(arr) == 1:
        return False
    for i in arr:
        for j in arr:
            if equal(i._speciality._name, j._speciality._name) and i != j and assignment[i] == assignment[j] and (
                    (i._type_of_class == "lecture") or (j._type_of_class == "lecture")):
                return True
    return False


# якщо однаковий тип занять, різні класи і однаковий час - то не проходить
def groups_conflict(assignment):
    arr = get_var(assignment)
    if len(arr) == 1:
        return False
    for i in arr:
        for j in arr:
            if equal(i._type_of_class, j._type_of_class) and i != j and assignment[i] == assignment[j]:
                return True
    return False


my_csp = {VARIABLES: classes,
          DOMAINS: meeting_times,
          CONSTRAINTS: [same_teacher, same_spec, groups_conflict]}
