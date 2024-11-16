import prettytable
from csp import *
from constraint_propagation import *
from lcv import *
from mrv import *
import sys


# Клас Tee для дублювання виводу
class Tee(object):
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)

    def flush(self):
        for f in self.files:
            f.flush()


# Виконуємо основну функцію при запуску скрипта
if __name__ == "__main__":
    # Відкриваємо файл 'schedule.txt' для запису виходу
    with open('schedule.txt', 'w') as f:
        # Зберігаємо оригінальний stdout
        original_stdout = sys.stdout
        # Перенаправляємо stdout на консоль і файл одночасно
        sys.stdout = Tee(sys.stdout, f)
        try:
            # Вибір змінної: Застосовується простий вибір змінної, який обирає першу невирішену змінну в порядку, в якому вони з'являються в задачі.
            # Вибір значення: Застосовується простий вибір значення, яке є першим можливим значенням у домені змінної.
            result_default = backtracking(init_assignment_default(my_csp), my_csp, default_heuristic)
            print("Counter for default backtracking: " + str(get_counter_default()))

            result_rec = backtracking_recursive(init_assignment_default(my_csp), my_csp, default_heuristic)
            print("Counter for recursive backtracking: " + str(get_counter_default()))
            # Вибір змінної: Застосовується простий вибір змінної, як у звичайному backtracking.
            # Вибір значення: Використовує стратегію LCV для вибору значення.
            #  LCV вибирає значення, яке призводить до найменшого кількості обмежень для інших змінних.
            result_lcv = backtracking_lcv(init_assignment_lcv(my_csp), my_csp, lcv_heuristic)
            print("Counter for backtracking with LCV: " + str(get_counter_lcv()))

            # Вибір змінної: Використовує стратегію MRV для вибору змінної.
            # MRV вибирає змінну, у якої залишилося найменше кількість можливих значень (найменший розмір домену).
            # Вибір значення: Застосовується простий вибір значення, як у звичайному backtracking.
            result_mrv = mrv_backtracking(init_assignment_mrv(my_csp), my_csp)
            print("Counter for backtracking with MRV: " + str(get_counter_mrv()))

            # Вибір змінної: Використовується власна стратегія вибору змінної з обмеженнями.
            # Вибір значення: Застосовується "поширення обмежень" для вибору значення,
            # здатного досягти найменшої кількості конфліктів з іншими змінними.
            # Замість того, щоб чекати до кінця алгоритму, "поширення обмежень"
            #  відкидає неприпустимі значення з доменів змінних під час виконання алгоритму.
            # Це робиться за допомогою правил, визначених обмеженнями (constraints).
            result_constraint_propagation = constraint_propagation(init_assignment_con(my_csp), my_csp)
            print("Counter for backtracking with Constraint Propagation: " + str(get_counter_con()))

            result = result_constraint_propagation

            monday, tuesday, wednesday, thursday, friday = [], [], [], [], []
            days = [monday, tuesday, wednesday, thursday, friday]
            for i in result.keys():
                if result[i] < 6:
                    monday.append((i, result[i]))
                elif result[i] < 12 and result[i] >= 6:
                    tuesday.append((i, result[i] - 6))
                elif result[i] < 18 and result[i] >= 12:
                    wednesday.append((i, result[i] - 12))
                elif result[i] < 24 and result[i] >= 18:
                    thursday.append((i, result[i] - 18))
                elif result[i] >= 24:
                    friday.append((i, result[i] - 24))


            def print_day(day, l):
                r = ""
                for d, n in day:
                    if (l == n):
                        r += str(d) + "\n"
                return r


            table = prettytable.PrettyTable(['Lesson Time', 'Monday', 'Tuesday', 'Wednesday'])
            k = 0
            for i in range(len(MEETING_TIMES)):
                table.add_row([MEETING_TIMES[i], print_day(monday, k), print_day(tuesday, k), print_day(wednesday, k)])
                k += 1
            print(table)

            table2 = prettytable.PrettyTable(['Lesson Time', 'Thursday', 'Friday'])
            k = 0
            for i in range(len(MEETING_TIMES)):
                table2.add_row([MEETING_TIMES[i], print_day(thursday, k), print_day(friday, k)])
                k += 1
            print(table2)
        finally:
            # Відновлюємо оригінальний stdout
            sys.stdout = original_stdout
