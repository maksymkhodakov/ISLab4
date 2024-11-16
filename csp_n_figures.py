class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        self.solution = None
        self.path_cost = 0  # Ініціалізація вартості шляху

    def solve(self):
        assignment = {}
        self.solution = self.backtrack(assignment)
        return self.solution

    def backtrack(self, assignment):
        if len(assignment) == len(self.variables):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                self.path_cost += 1  # Збільшення вартості шляху
                result = self.backtrack(assignment)
                if result is not None:
                    return result
                del assignment[var]
        return None

    def select_unassigned_variable(self, assignment):
        # Евристика MRV (мінімальна кількість решти значень)
        unassigned_vars = [v for v in self.variables if v not in assignment]
        # Отримуємо розміри доменів
        domain_sizes = {var: len(self.domains[var]) for var in unassigned_vars}
        min_size = min(domain_sizes.values())
        # Змінні з мінімальним доменом
        mrv_vars = [var for var in unassigned_vars if len(self.domains[var]) == min_size]
        if len(mrv_vars) == 1:
            return mrv_vars[0]
        else:
            # Ступенева евристика
            max_degree = -1
            selected_var = None
            for var in mrv_vars:
                degree = sum(1 for neighbor in self.variables if neighbor != var and neighbor not in assignment)
                if degree > max_degree:
                    max_degree = degree
                    selected_var = var
            return selected_var

    def order_domain_values(self, var, assignment):
        # Евристика з найменш обмежувальним значенням
        def count_conflicts(value):
            count = 0
            for other_var in self.variables:
                if other_var not in assignment and other_var != var:
                    for other_value in self.domains[other_var]:
                        if not self.constraints(var, value, other_var, other_value):
                            count += 1
            return count

        values = list(self.domains[var])
        values.sort(key=count_conflicts)
        return values

    def is_consistent(self, var, value, assignment):
        for other_var in assignment:
            if not self.constraints(var, value, other_var, assignment[other_var]):
                return False
        return True


def n_queens_constraints(var1, val1, var2, val2):
    # Перевірка на те, чи атакують два ферзі один одного
    if val1 == val2:
        return False  # Той самий стовпець
    if abs(var1 - var2) == abs(val1 - val2):
        return False  # Та сама діагональ
    return True


# Кількість ферзів
N = 8

# Змінні: рядки від 0 до N-1
variables = list(range(N))

# Домени: можливі стовпці для кожного рядка
domains = {var: list(range(N)) for var in variables}

# Ініціалізація CSP
csp = CSP(variables, domains, n_queens_constraints)

# Розв'язання CSP
solution = csp.solve()

# Виведення рішення
if solution:
    board = [['.' for _ in range(N)] for _ in range(N)]
    for row in solution:
        col = solution[row]
        board[row][col] = 'Q'
    for row in board:
        print(' '.join(row))
    print(f"Вартість шляху: {csp.path_cost}")
else:
    print("Рішення не знайдено.")
