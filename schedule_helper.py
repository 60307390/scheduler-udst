from collections.abc import MutableMapping
#from openpyxl import Workbook
import itertools
import numpy
import pandas as pd

def flatten_dict(d: MutableMapping, sep: str= '.') -> MutableMapping:
    [flat_dict] = pd.json_normalize(d, sep=sep).to_dict(orient='records')
    return flat_dict

# def avg_of_two(N):
#     return sum(N)/2

def matrix_transpose(A):
    'Returns the transpose Aᵀ, given a matrix A'
    A_T = []
    for i in range(len(A[0])):  # Given A is a rectangular matrix
        A_T.append([])

    for i in range(len(A)):
        for j in range(len(A[i])):
            A_T[j].append(A[i][j])
    return A_T

DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]

def get_schedule_as_dict():
    schedule_dict = {}

    # "class" : {section_no: [ {"Sunday"}:[start, end]}, {"Monday"}:[start,end] ] } ]
    with open('schedules.txt', 'r') as f:
        lines = f.readlines()
        current_class = ""
        current_section = 0
        
        for i in range(len(lines)):
            # "class"
            line = lines[i].strip()
            if len(line) == 9 and line[:4].isalpha() and line[5:].isdigit():    # If it fits format for class code
                class_name = line[:4] + line[5:]
                schedule_dict[class_name] = {}
                current_class = class_name
            
            # section_no
            if len(line) <= 2 and line.isdigit():
                current_section = int(line)
                schedule_dict[current_class][current_section] = []
                

            # append time per day of week
            if line in DAYS:
                times = []
                day = line
                for i in lines[i+1].strip().split(' to '):
                    time = int(i[:-5])
                    if ':30' in i:
                        time += .5
                    if 'PM' in i and time < 12:
                        times.append(time+12)
                    else:
                        times.append(time)

                schedule_dict[current_class][current_section].append({day: [times[0], times[1]]})  
    # print(schedule_dict)
    return schedule_dict

def depreciated_get_compatible_combinations(schedules):
    course_options = []
    k = 0
    for i in schedules:
        course_options.append([])
        course_options[k].extend(list(schedules[i]))
        k += 1
    
    comb_list = []
    comb_tuple = []
    cartesian_product = itertools.product(*course_options)
    for i in cartesian_product:
        day_matrix = []
        schedule_opts = {}
        for j in schedules:
            # Appending product
            temp_row = [0,0,0,0,0]
            keyIndex = list(schedules.keys()).index(j)
            schedule = schedules[j][i[keyIndex]]
            for n in schedule:
                for m in range(len(DAYS)):
                    if DAYS[m] in n:
                        temp_row[m] = sum(n[DAYS[m]])/2
            day_matrix.append(temp_row)
            schedule_opts[j] = {}
            schedule_opts[j][i[keyIndex]] = schedule
        # Compatibility logic
        day_matrix_T = matrix_transpose(day_matrix)
        compatible = True
        for j in day_matrix_T:
            j = list(sorted(j))
            for k in range(len(j)-1):
                if 0 < abs(j[k+1]-j[k]) <= 1:
                    compatible = False
                    break
        if compatible:
            comb_tuple.append(i)
            comb_list.append(schedule_opts)
    return comb_list, comb_tuple

def is_compatible(section1, section2):
    for i in section1:
        for j in section2:
            day1 = list(i.keys())[0]
            day2 = list(j.keys())[0]
            if day1 == day2:
                s1, e1 = i[day1][0], i[day1][1]
                s2, e2 = j[day2][0], j[day2][1]
                if (e1 > s2) and (e2 > s1):
                    return False
    return True

def get_compatible_combinations(schedules):
    courses = list(schedules)
    sections = [list(schedules[course].keys()) for course in courses]
    
    cartesian_combinations = list(itertools.product(*sections))

    comb_list = []
    comb_tuple = []
    for comb in cartesian_combinations:
        compatible = True
        for i in range(len(comb)):
            for j in range(i+1, len(comb)):
                section1 = schedules[courses[i]][comb[i]]
                section2 = schedules[courses[j]][comb[j]]
                if not is_compatible(section1, section2):
                    compatible = False
                    break
        if compatible:
            comb_tuple.append(comb)
            comb_opts = {}
            for i in range(len(comb)):
                comb_opts[courses[i]] = {}
                comb_opts[courses[i]][comb[i]] = schedules[courses[i]][comb[i]]
            comb_list.append(comb_opts)
    return comb_list, comb_tuple

def get_schedule_matrix(schedule):
    sch_matrix = numpy.zeros((12*2+1,5), dtype=numpy.int8).tolist()
    flatenned_schedule = flatten_dict(schedule)
    for i in flatenned_schedule:
        sch_index = list(schedule).index(i[:8])
        for timings in flatenned_schedule[i]:
            for day in DAYS:
                if day in timings:
                    col = DAYS.index(day)
                    s_i, e_i = timings[day][0], timings[day][1]
                    for j in range(int(2*s_i), int(2*e_i)):
                        row = int(2*((j/2)-8))
                        #print(row, col)
                        sch_matrix[row][col] = sch_index+1
    return sch_matrix


if __name__ == "__main__":
    schedules = get_schedule_as_dict()
    comb_list,comb_tuple = get_compatible_combinations(schedules)
    for schedule in comb_list:
        schedule_matrix = get_schedule_matrix(schedule)

    print('-'*50)
    print("Number of compatible combinations: " + str(len(comb_list)))
    print("Compatible combinations: " + str(comb_tuple))
    print('-'*50)
