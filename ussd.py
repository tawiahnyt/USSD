import requests
import pandas as pd
import json

USSD_URL = 'http://127.0.0.1:5000'
USSD_SHORTCODE = '*123*112#'
API_TOKEN = None

short_code = input('Enter shortcode: ')
student_id = None
password = ''

if short_code == USSD_SHORTCODE:
    print("Welcome to GCTU SIP USSD.\nLogin with your credentials to proceed")
    user = True
    while user:
        student_id = int(input('Student ID: '))
        df = pd.read_csv('indexes.csv')
        student_list = df['student_id'].tolist()
        if student_id not in student_list:
            print('Student ID not found. Please try again')
            user = True
        else:
            user = False

    is_password = True
    while is_password:
        password = input('Password: ')

        data = {'username': student_id, 'password': password}
        login_response = requests.post(f'{USSD_URL}/', json=data)

        if login_response.status_code != 200:
            print('Password is incorrect. Please try again')
            is_password = True
        else:
            is_password = False
            API_TOKEN = login_response.json().get('access_token')

    home_response = requests.get(f'{USSD_URL}/home', headers={'Authorization': f'Bearer {API_TOKEN}'})
    print(f"Welcome {home_response.json().get('first_name')}! What would you like to do today?")
    user_response = int(input('1. My Account\n2. Check Results\n3. Register Courses\n4. Time Table\n5. School  '
                              'Calendar\n6. Log Out\nEnter an option to  proceed: '))

    if user_response == 1:
        account_response = requests.get(f'{USSD_URL}/account', headers={'Authorization': f'Bearer {API_TOKEN}'})
        account_details = account_response.json()
        print(f"Name: {account_details.get('first_name')} {account_details.get('last_name')} {account_details.get('other_names')}\n"
              f"Student ID: {account_details.get('student_id')}\n"
              f"Programme: {account_details.get('degree_programmes')}\n"
              f"Level: {account_details.get('level')}\n"
              f"Email: {account_details.get('email')}\n"
              f"Phone: {account_details.get('phone')}\n"
              f"Student's Email: {account_details.get('student_email')}\n"
              f"Date of Birth: {account_details.get('date_of_birth')}\n"
              f"Gender: {account_details.get('gender')}\n"
              f"Enrollment Date: {account_details.get('enrollment_date')}\n"
              f"Graduation Date: {account_details.get('graduation_date')}\n"
              f"Student Type: {account_details.get('student_type')}\n")

    elif user_response == 2:
        result_response = requests.get(f'{USSD_URL}/results', headers={'Authorization': f'Bearer {API_TOKEN}'})
        print(result_response.raise_for_status())
        result_details = result_response.json()

        with open('courses.json') as file:
            data = json.load(file)

        l100_first_semester = data['BSc. Information Technology']['100']['first_semester']
        l100_second_semester = data['BSc. Information Technology']['100']['second_semester']
        l200_first_semester = data['BSc. Information Technology']['200']['first_semester']
        l200_second_semester = data['BSc. Information Technology']['200']['second_semester']
        l300_first_semester = data['BSc. Information Technology']['300']['first_semester']
        l300_second_semester = data['BSc. Information Technology']['300']['second_semester']

        if result_details.get('level') == 100:
            print('No results to show')
        elif result_details.get('level') == 200:
            choice = int(input('Select a result to view\n1. Level  100 First Semester\n2. Level 100 Second Semester'))
            if choice == 1:
                print(f'Level 100 First Semester Results\n\n')
                for course in l100_first_semester:
                    course_code = course.course_code
                    print(f"{course.course_code} - {course.course_title} - {result_details[course_code.replace('-', '_')]}")
            elif choice == 2:
                print(f'Level 100 Second Semester Results\n\n')
                for course in l100_second_semester:
                    course_code = course.course_code
                    print(
                        f"{course.course_code} - {course.course_title} - {result_details[course_code.replace('-', '_')]}")
        elif result_details.get('level') == 300:
            choice = int(input('Select a result to view\n1. Level  100 First Semester\n2. Level 100 Second Semester'
                               '\n3. Level 200 First Semester \n4. Level 200 Second Semester'))
            if choice == 1:
                print(f'Level 100 First Semester Results\n\n')
                for course in l100_first_semester:
                    course_code = course.course_code
                    print(
                        f"{course.course_code} - {course.course_title} - {result_details[course_code.replace('-', '_')]}")
            elif choice == 2:
                print(f'Level 100 Second Semester Results\n\n')
                for course in l100_second_semester:
                    course_code = course.course_code
                    print(
                        f"{course.course_code} - {course.course_title} - {result_details[course_code.replace('-', '_')]}")
            elif choice == 3:
                print(f'Level 200 Second Semester Results\n\n')
                for course in l200_first_semester:
                    course_code = course.course_code
                    print(
                        f"{course.course_code} - {course.course_title} - {result_details[course_code.replace('-', '_')]}")
            elif choice == 4:
                print(f'Level 200 Second Semester Results\n\n')
                for course in l200_second_semester:
                    course_code = course.course_code
                    print(
                        f"{course.course_code} - {course.course_title} - {result_details[course_code.replace('-', '_')]}")
        elif result_details.get('level') == 300:
            choice = int(input('Select a result to view\n1. Level  100 First Semester\n2. Level 100 Second Semester'
                               '\n3. Level 200 First Semester \n4. Level 200 Second Semester\n5. Level 300 First'
                               'Semester\n6. Level 300 Second Semester'))
            if choice == 1:
                print(f'Level 100 First Semester Results\n\n')
                for course in l100_first_semester:
                    course_code = course.course_code
                    print(
                        f"{course.course_code} - {course.course_title} - {result_details[course_code.replace('-', '_')]}")
            elif choice == 2:
                print(f'Level 100 Second Semester Results\n\n')
                for course in l100_second_semester:
                    course_code = course.course_code
                    print(
                        f"{course.course_code} - {course.course_title} - {result_details[course_code.replace('-', '_')]}")
            elif choice == 3:
                print(f'Level 200 First Semester Results\n\n')
                for course in l200_first_semester:
                    course_code = course.course_code
                    print(
                        f"{course.course_code} - {course.course_title} - {result_details[course_code.replace('-', '_')]}")
            elif choice == 4:
                print(f'Level 200 Second Semester Results\n\n')
                for course in l200_second_semester:
                    course_code = course.course_code
                    print(
                        f"{course.course_code} - {course.course_title} - {result_details[course_code.replace('-', '_')]}")
            elif choice == 5:
                print(f'Level 300 First Semester Results\n\n')
                for course in l300_first_semester:
                    course_code = course.course_code
                    print(
                        f"{course.course_code} - {course.course_title} - {result_details[course_code.replace('-', '_')]}")
            elif choice == 6:
                print(f'Level 300 Second Semester Results\n\n')
                for course in l300_second_semester:
                    course_code = course.course_code
                    print(
                        f"{course.course_code} - {course.course_title} - {result_details[course_code.replace('-', '_')]}")
#
#

# import requests
# import pandas as pd
# import json
#
# USSD_URL = 'http://127.0.0.1:5000'
# USSD_SHORTCODE = '*123*112#'
#
#
# def get_valid_student_id():
#     df = pd.read_csv('indexes.csv')
#     student_list = df['student_id'].tolist()
#
#     while True:
#         try:
#             student_id = int(input('Student ID: '))
#             if student_id in student_list:
#                 return student_id
#             else:
#                 print('Student ID not found. Please try again.')
#         except ValueError:
#             print('Invalid input. Please enter a numeric Student ID.')
#
#
# def get_valid_password(student_id):
#     while True:
#         password = input('Password: ')
#         data = {'username': student_id, 'password': password}
#         try:
#             response = requests.post(f'{USSD_URL}/', json=data)
#             response.raise_for_status()
#             return response.json().get('access_token')
#         except requests.HTTPError:
#             print('Password is incorrect. Please try again.')
#
#
# def print_account_details(account_details):
#     print(
#         f"Name: {account_details.get('first_name')} {account_details.get('last_name')} {account_details.get('other_names')}\n"
#         f"Student ID: {account_details.get('student_id')}\n"
#         f"Programme: {account_details.get('degree_programmes')}\n"
#         f"Level: {account_details.get('level')}\n"
#         f"Email: {account_details.get('email')}\n"
#         f"Phone: {account_details.get('phone')}\n"
#         f"Student's Email: {account_details.get('student_email')}\n"
#         f"Date of Birth: {account_details.get('date_of_birth')}\n"
#         f"Gender: {account_details.get('gender')}\n"
#         f"Enrollment Date: {account_details.get('enrollment_date')}\n"
#         f"Graduation Date: {account_details.get('graduation_date')}\n"
#         f"Student Type: {account_details.get('student_type')}\n")
#
#
# def print_results(result_details):
#     with open('courses.json') as file:
#         data = json.load(file)
#
#         l100_first_semester = data['BSc. Information Technology']['100']['first_semester']
#         l100_second_semester = data['BSc. Information Technology']['100']['second_semester']
#         l200_first_semester = data['BSc. Information Technology']['200']['first_semester']
#         l200_second_semester = data['BSc. Information Technology']['200']['second_semester']
#         l300_first_semester = data['BSc. Information Technology']['300']['first_semester']
#         l300_second_semester = data['BSc. Information Technology']['300']['second_semester']
#
#         if result_details.get('level') == 100:
#             print('No results to show')
#         elif result_details.get('level') == 200:
#             choice = int(input('Select a result to view\n1. Level  100 First Semester\n2. Level 100 Second Semester'))
#             if choice == 1:
#                 print(f'Level 100 First Semester Results\n\n')
#                 for course in l100_first_semester:
#                     course_code = course.course_code
#                     print(f"{course.course_code} - {course.course_title} - {result_details[course_code.replace('-', '_')]}")
#             elif choice == 2:
#                 print(f'Level 100 Second Semester Results\n\n')
#                 for course in l100_second_semester:
#                     course_code = course.course_code
#                     print(
#                         f"{course.course_code} - {course.course_title} - {result_details[course_code.replace('-', '_')]}")
#     # if level == 100:
#     #     print('No results to show')
#     #     return
#     #
#     # level_courses = {
#     #     200: (courses_data['100']['first_semester'], courses_data['100']['second_semester']),
#     #     300: (courses_data['200']['first_semester'], courses_data['200']['second_semester']),
#     # }
#     #
#     # if level in level_courses:
#     #     choices = level_courses[level]
#     #     choice = int(input('Select a result to view\n1. First Semester\n2. Second Semester'))
#     #     semester_courses = choices[choice - 1]
#     #
#     #     semester_name = 'First Semester' if choice == 1 else 'Second Semester'
#     #     print(f'Level {level} {semester_name} Results\n\n')
#     #
#     #     for course in semester_courses:
#     #         course_code = course['course_code']
#     #         print(f"{course_code} - {course['course_title']} - {result_details.get(course_code.replace('-', '_'))}")
#
#
# def main():
#     short_code = input('Enter shortcode: ')
#     if short_code != USSD_SHORTCODE:
#         print('Invalid shortcode.')
#         return
#
#     print("Welcome to GCTU SIP USSD.\nLogin with your credentials to proceed")
#     student_id = get_valid_student_id()
#     api_token = get_valid_password(student_id)
#
#     try:
#         home_response = requests.get(f'{USSD_URL}/home', headers={'Authorization': f'Bearer {api_token}'})
#         home_response.raise_for_status()
#         user_name = home_response.json().get('first_name')
#         print(f"Welcome {user_name}! What would you like to do today?")
#
#         user_response = int(input('1. My Account\n2. Check Results\n3. Register Courses\n4. Time Table\n'
#                                   '5. School Calendar\n6. Log Out\nEnter an option to proceed: '))
#
#         if user_response == 1:
#             account_response = requests.get(f'{USSD_URL}/account', headers={'Authorization': f'Bearer {api_token}'})
#             account_response.raise_for_status()
#             account_details = account_response.json()
#             print_account_details(account_details)
#
#         elif user_response == 2:
#             result_response = requests.get(f'{USSD_URL}/results', headers={'Authorization': f'Bearer {api_token}'})
#             result_response.raise_for_status()
#             result_details = result_response.json()
#             print_results(result_details)
#
#     except requests.HTTPError as e:
#         print(f"An error occurred: {e}")
#
#
# if __name__ == "__main__":
#     main()


import requests
import pandas as pd
import json
import os

USSD_URL = 'http://127.0.0.1:5000'
USSD_SHORTCODE = '*123*112#'


def get_valid_student_id():
    if not os.path.isfile('indexes.csv'):
        print('Error: indexes.csv file is missing.')
        return None

    df = pd.read_csv('indexes.csv')
    student_list = df['student_id'].tolist()

    while True:
        try:
            student_id = int(input('Student ID: '))
            if student_id in student_list:
                return student_id
            else:
                print('Student ID not found. Please try again.')
        except ValueError:
            print('Invalid input. Please enter a numeric Student ID.')


def get_valid_password(student_id):
    while True:
        password = input('Password: ')
        data = {'username': student_id, 'password': password}
        try:
            response = requests.post(f'{USSD_URL}/', json=data)
            response.raise_for_status()
            return response.json().get('access_token')
        except requests.HTTPError:
            print('Password is incorrect. Please try again.')
        except requests.RequestException as e:
            print(f'An error occurred: {e}')


def print_account_details(account_details):
    print(
        f"Name: {account_details.get('first_name', 'N/A')} {account_details.get('last_name', 'N/A')} {account_details.get('other_names', 'N/A')}\n"
        f"Student ID: {account_details.get('student_id', 'N/A')}\n"
        f"Programme: {account_details.get('degree_programmes', 'N/A')}\n"
        f"Level: {account_details.get('level', 'N/A')}\n"
        f"Email: {account_details.get('email', 'N/A')}\n"
        f"Phone: {account_details.get('phone', 'N/A')}\n"
        f"Student's Email: {account_details.get('student_email', 'N/A')}\n"
        f"Date of Birth: {account_details.get('date_of_birth', 'N/A')}\n"
        f"Gender: {account_details.get('gender', 'N/A')}\n"
        f"Enrollment Date: {account_details.get('enrollment_date', 'N/A')}\n"
        f"Graduation Date: {account_details.get('graduation_date', 'N/A')}\n"
        f"Student Type: {account_details.get('student_type', 'N/A')}\n")


def print_results(result_details):
    if not os.path.isfile('courses.json'):
        print('Error: courses.json file is missing.')
        return

    with open('courses.json') as file:
        data = json.load(file)

    level = result_details.get('level')
    if level is None:
        print('No level information available.')
        return

    programme = 'BSc. Information Technology'
    if programme not in data:
        print('Programme data not found.')
        return

    level_data = data.get(programme, {}).get(str(level), {})
    if not level_data:
        print('No course data found for the given level.')
        return

    semester_options = {
        1: 'first_semester',
        2: 'second_semester'
    }

    choice = int(input('Select a result to view\n1. First Semester\n2. Second Semester\n'))
    semester_key = semester_options.get(choice)
    if not semester_key:
        print('Invalid choice.')
        return

    semester_courses = level_data.get(semester_key, [])
    if not semester_courses:
        print('No results to show for the selected semester.')
        return

    print(f'Level {level} {semester_key.replace("_", " ").title()} Results\n')
    for course in semester_courses:
        course_code = course.get('course_code', 'N/A')
        course_title = course.get('course_title', 'N/A')
        result = result_details.get(course_code.replace('-', '_'), 'Not Available')
        print(f"{course_code} - {course_title} - {result}")


def main():
    short_code = input('Enter shortcode: ')
    if short_code != USSD_SHORTCODE:
        print('Invalid shortcode.')
        return

    print("Welcome to GCTU SIP USSD.\nLogin with your credentials to proceed")
    student_id = get_valid_student_id()
    if student_id is None:
        return

    api_token = get_valid_password(student_id)
    if not api_token:
        return

    try:
        home_response = requests.get(f'{USSD_URL}/home', headers={'Authorization': f'Bearer {api_token}'})
        home_response.raise_for_status()
        user_name = home_response.json().get('first_name', 'User')
        print(f"Welcome {user_name}! What would you like to do today?")

        user_response = int(input('1. My Account\n2. Check Results\n3. Register Courses\n4. Time Table\n'
                                  '5. School Calendar\n6. Log Out\nEnter an option to proceed: '))

        if user_response == 1:
            account_response = requests.get(f'{USSD_URL}/account', headers={'Authorization': f'Bearer {api_token}'})
            account_response.raise_for_status()
            account_details = account_response.json()
            print_account_details(account_details)

        elif user_response == 2:
            result_response = requests.get(f'{USSD_URL}/results', headers={'Authorization': f'Bearer {api_token}'})
            result_response.raise_for_status()
            result_details = result_response.json()
            print_results(result_details)

        # Add additional options for Register Courses, Time Table, School Calendar as needed

    except requests.RequestException as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
