import json
import pandas as pd
import os


def main():
    # choosing a file with entered subject
    for (i, file_name) in enumerate(os.listdir('subjects')):
        print(i, '. ', file_name[0:len(file_name) - 5])

    file = int(input('Enter subject index: '))
    db = open('subjects/' + os.listdir('subjects')[file])
    dict_db = json.load(db)

    commands = '\n1.View the whole grading\n' \
               '2.Grades for only one student\n' \
               '3.The best / worst student\n' \
               '4.Student names who have better average\n' \
               '5.Average for all tests\n' \
               '6.Average for a given test\n' \
               '7.Adding new grades\n' \
               '8.Sorting students\n' \
               '9.Exit\n'

    print(commands)
    cmd = input("Choose a command: ")

    while cmd != "9":
        if cmd == "1":
            print(whole_grading(dict_db))
        elif cmd == "2":
            one_student(dict_db)
        elif cmd == "3":
            best_worst(dict_db)
        elif cmd == "4":
            better_student(dict_db)
        elif cmd == "5":
            avg(dict_db)
        elif cmd == "6":
            avg_for_one_test(dict_db)
        elif cmd == "7":
            adding_test(dict_db, file)
        elif cmd == "8":
            sorting(dict_db)
        else:
            print("No such command! Try again")

        print(commands)
        cmd = input("Choose a command: ")


# shows whole grading for whole class
def whole_grading(dict_db):
    students = []
    for student in dict_db['students']:
        sub_array = {}
        sub_array['name'] = student['name']
        for (i, grade) in enumerate(student['grades']):
            sub_array['Grade: ' + str(i)] = grade
        students.append(sub_array)

    return pd.DataFrame(students)


# shows all grades for one student
def one_student(dict_db):
    student_name = input("Enter student's name: ")
    students = list(filter(lambda x: student_name in x["name"], dict_db['students']))
    if len(students):
        student = students[0]
        result = {'name': student['name']}
        for (i, grade) in enumerate(student['grades']):
            result['Grade: ' + str(i)] = grade
        df = pd.DataFrame([result])
        print(df)
    else:
        print('Not found')


# shows best/worst student
def best_worst(dict_db):
    best = max(dict_db['students'], key=lambda student: mean(student['grades']))
    worst = min(dict_db['students'], key=lambda student: mean(student['grades']))
    print('Best student: ', best['name'])
    print('Worst student: ', worst['name'])


# shows student with better scores
def better_student(dict_db):
    num = int(input("Enter a grade: "))
    result = [student['name'] for student in dict_db['students'] if num < mean(student['grades'])]
    print('Students who have better average:')
    for item in result:
        print(item)


# shows average for all tests
def avg(dict_db):
    average = mean([mean(student['grades']) for student in dict_db['students']])
    print('Average for the whole class across all tests: ', round(average, 1))


# shows average for all one tests
def avg_for_one_test(dict_db):
    chose_test = int(input("Enter index of a text (starting from 0): "))
    grades = [student['grades'][chose_test] for student in dict_db['students'] if chose_test < len(student['grades'])]
    if len(grades):
        print(f'Average for the whole class for a {chose_test} test')
        print(mean(grades))
    else:
        print("No such test")


# adds grade for a new test
def adding_test(dict_db, file):
    print("Enter grades for a new test")
    for student in dict_db['students']:
        new_grade = int(input(student['name'] + ": "))
        student['grades'].append(new_grade)
    with open('subjects/' + os.listdir('subjects')[file], "w") as file:
        json.dump(dict_db, file)


# sorts students based on their grades
def sorting(dict_db):
    df = whole_grading(dict_db)
    num = input('Enter a sorting grade: ')
    grade_key = "Grade: " + num
    if grade_key in df.columns:
        result = df.sort_values(by=grade_key, ascending=False)
        print(result)
    else:
        print("No such grade")


# function for average
def mean(array):
    return sum(array) / len(array)


if __name__ == '__main__':
    main()
