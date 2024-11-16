import copy
import random
import sys

sys.setrecursionlimit(10000)

from collections import defaultdict

from genetic_algo import TIMESLOTS, WEEK_TYPE, Event, Schedule


class CSP:
    def __init__(self, variables, domains, constraints):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        self.assignment = {}
        self.path_cost = 0

    def is_complete(self, assignment):
        return len(assignment) == len(self.variables)

    def is_consistent(self, var, value, assignment):
        return self.constraints(var, value, assignment)

    def select_unassigned_variable(self, assignment):
        unassigned_vars = [v for v in self.variables if v not in assignment]
        min_domain_size = min(len(self.domains[v]) for v in unassigned_vars)
        mrv_vars = [v for v in unassigned_vars if len(self.domains[v]) == min_domain_size]
        if len(mrv_vars) == 1:
            return mrv_vars[0]
        max_degree = -1
        selected_var = None
        for var in mrv_vars:
            degree = sum(1 for v in unassigned_vars if v != var)
            if degree > max_degree:
                max_degree = degree
                selected_var = var
        return selected_var

    def order_domain_values(self, var, assignment):
        def count_conflicts(value):
            conflicts = 0
            for neighbor in self.variables:
                if neighbor != var and neighbor not in assignment:
                    for neighbor_value in self.domains[neighbor]:
                        if not self.constraints(var, value, {neighbor: neighbor_value}):
                            conflicts += 1
            return conflicts

        return sorted(self.domains[var], key=count_conflicts)

    def backtrack(self, assignment):
        if self.is_complete(assignment):
            print("Знайдено повне присвоєння.")
            return assignment
        var = self.select_unassigned_variable(assignment)
        print(f"Вибрана змінна: {var}")
        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                print(f"Присвоюємо змінній {var} значення {value}")
                assignment[var] = value
                self.path_cost += 1
                result = self.backtrack(assignment)
                if result:
                    return result
                print(f"Видаляємо присвоєння змінної {var}")
                del assignment[var]
        return None

    def solve(self):
        print("Початок розв'язання CSP...")
        result = self.backtrack({})
        print("Завершення розв'язання CSP.")
        return result


def generate_csp_variables(subjects, groups):
    variables = []
    for subj in subjects:
        weeks = [subj['WeekType']] if subj['WeekType'] in WEEK_TYPE else WEEK_TYPE
        for week in weeks:
            for _ in range(subj['NumLectures']):
                variables.append({
                    'subject': subj,
                    'event_type': 'Лекція',
                    'week_type': week
                })
            for _ in range(subj['NumPracticals']):
                if subj['RequiresSubgroups']:
                    for subgroup_id in groups[subj['GroupID']]['Subgroups']:
                        variables.append({
                            'subject': subj,
                            'event_type': 'Практика',
                            'week_type': week,
                            'subgroup_id': subgroup_id
                        })
                else:
                    variables.append({
                        'subject': subj,
                        'event_type': 'Практика',
                        'week_type': week
                    })
    return variables


def generate_csp_domains(variables, lecturers, auditoriums, groups):
    domains = {}
    for idx, var in enumerate(variables):
        subj = var['subject']
        week_type = var['week_type']
        event_type = var['event_type']

        possible_timeslots = [t for t in TIMESLOTS if t.startswith(week_type)]

        suitable_lecturers = [
            lid for lid, l in lecturers.items()
            if subj['SubjectID'] in l['SubjectsCanTeach'] and event_type in l['TypesCanTeach']
        ]
        if not suitable_lecturers:
            continue

        total_group_size = groups[subj['GroupID']]['NumStudents']
        if event_type == 'Практика' and subj['RequiresSubgroups']:
            total_group_size = total_group_size // 2
        suitable_auditoriums = [
            aid for aid, cap in auditoriums.items() if cap >= total_group_size
        ]
        if not suitable_auditoriums:
            continue

        domain = []
        for timeslot in possible_timeslots:
            for lecturer_id in suitable_lecturers:
                for auditorium_id in suitable_auditoriums:
                    domain.append({
                        'timeslot': timeslot,
                        'lecturer_id': lecturer_id,
                        'auditorium_id': auditorium_id
                    })
        domains[idx] = domain
        print(f"Змінна {idx}: Розмір домену = {len(domain)}")
    return domains


def csp_constraints(var_idx, value, assignment, variables, lecturers, groups):
    var = variables[var_idx]
    subj = var['subject']
    event_type = var['event_type']
    group_id = subj['GroupID']
    subgroup_id = var.get('subgroup_id')

    # Викладач не повинен перевищувати максимальне навантаження
    lecturer_hours = defaultdict(float)
    for other_var_idx, other_value in assignment.items():
        other_var = variables[other_var_idx]
        if other_value['lecturer_id'] == value['lecturer_id']:
            week = value['timeslot'].split(' - ')[0]
            lecturer_hours[week] += 1.5
    max_hours = lecturers[value['lecturer_id']]['MaxHoursPerWeek']
    if any(hours > max_hours for hours in lecturer_hours.values()):
        return False

    for other_var_idx, other_value in assignment.items():
        other_var = variables[other_var_idx]
        other_subj = other_var['subject']
        other_event_type = other_var['event_type']
        other_group_id = other_subj['GroupID']
        other_subgroup_id = other_var.get('subgroup_id')

        # Перевірка часових конфліктів
        if value['timeslot'] == other_value['timeslot']:
            if value['lecturer_id'] == other_value['lecturer_id']:
                return False
            if value['auditorium_id'] == other_value['auditorium_id']:
                return False
            if group_id == other_group_id:
                if event_type == 'Практика' and subgroup_id:
                    if subgroup_id == other_subgroup_id:
                        return False
                else:
                    return False
    return True


def csp_algorithm(groups, subjects, lecturers, auditoriums):
    variables = generate_csp_variables(subjects, groups)
    domains = generate_csp_domains(variables, lecturers, auditoriums, groups)
    csp = CSP(
        variables=list(domains.keys()),
        domains=domains,
        constraints=lambda var, val, assignment: csp_constraints(var, val, assignment, variables, lecturers, groups)
    )
    solution = csp.solve()

    if solution:
        schedule = Schedule()
        for var_idx, value in solution.items():
            var = variables[var_idx]
            subj = var['subject']
            event = Event(
                timeslot=value['timeslot'],
                group_ids=[subj['GroupID']],
                subject_id=subj['SubjectID'],
                subject_name=subj['SubjectName'],
                lecturer_id=value['lecturer_id'],
                auditorium_id=value['auditorium_id'],
                event_type=var['event_type'],
                subgroup_ids={subj['GroupID']: var.get('subgroup_id')} if var.get('subgroup_id') else None,
                week_type=var['week_type']
            )
            schedule.add_event(event)
        return schedule
    else:
        print("Не вдалося знайти рішення.")
        return None
