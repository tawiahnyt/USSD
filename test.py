import requests
import pandas as pd
import json

USSD_URL = 'http://127.0.0.1:5000'
USSD_SHORTCODE = '*123*112#'


def get_valid_student_id():
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


def print_account_details(account_details):
    print(
        f"Name: {account_details.get('first_name')} {account_details.get('last_name')} {account_details.get('other_names')}\n"
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


def display_results(result_details):

    # Load course data from the JSON file
    with open('courses.json') as file:
        data = json.load(file)

    # Extract course data
    l100_first_semester = data['BSc. Information Technology']['100']['first_semester']
    l100_second_semester = data['BSc. Information Technology']['100']['second_semester']
    l200_first_semester = data['BSc. Information Technology']['200']['first_semester']
    l200_second_semester = data['BSc. Information Technology']['200']['second_semester']
    l300_first_semester = data['BSc. Information Technology']['300']['first_semester']
    l300_second_semester = data['BSc. Information Technology']['300']['second_semester']

    level = result_details.get('level')

    if level == 100:
        print('No results to show')
    elif level == 200:
        choice = int(input('Select a result to view\n1. Level 100 First Semester\n2. Level 100 Second Semester\n'))
        if choice == 1:
            print('Level 100 First Semester Results\n')
            for course in l100_first_semester:
                course_code = course['course_code']
                print(f"{course_code} - {course['course_title']} - {result_details.get(course_code.replace('-', '_'), 'N/A')}")
        elif choice == 2:
            print('Level 100 Second Semester Results\n')
            for course in l100_second_semester:
                course_code = course['course_code']
                print(f"{course_code} - {course['course_title']} - {result_details.get(course_code.replace('-', '_'), 'N/A')}")
    elif level == 300:
        choice = int(input('Select a result to view\n1. Level 100 First Semester\n2. Level 100 Second Semester\n'
                           '3. Level 200 First Semester\n4. Level 200 Second Semester\n5. Level 300 First Semester\n'
                           '6. Level 300 Second Semester\n'))
        if choice == 1:
            print('Level 100 First Semester Results\n')
            for course in l100_first_semester:
                course_code = course['course_code']
                print(f"{course_code} - {course['course_title']} - {result_details.get(course_code.replace('-', '_'))}")
        elif choice == 2:
            print('Level 100 Second Semester Results\n')
            for course in l100_second_semester:
                course_code = course['course_code']
                print(f"{course_code} - {course['course_title']} - {result_details.get(course_code.replace('-', '_'))}")
        elif choice == 3:
            print('Level 200 First Semester Results\n')
            for course in l200_first_semester:
                course_code = course['course_code']
                print(f"{course_code} - {course['course_title']} - {result_details.get(course_code.replace('-', '_'))}")
        elif choice == 4:
            print('Level 200 Second Semester Results\n')
            for course in l200_second_semester:
                course_code = course['course_code']
                print(f"{course_code} - {course['course_title']} - {result_details.get(course_code.replace('-', '_'))}")
        elif choice == 5:
            print('Level 300 First Semester Results\n')
            for course in l300_first_semester:
                course_code = course['course_code']
                print(f"{course_code} - {course['course_title']} - {result_details.get(course_code.replace('-', '_'))}")
        elif choice == 6:
            print('Level 300 Second Semester Results\n')
            for course in l300_second_semester:
                course_code = course['course_code']
                print(f"{course_code} - {course['course_title']} - {result_details.get(course_code.replace('-', '_'))}")
        else:
            print('Invalid Input!')


def main():
    short_code = '*123*112#'
    if short_code == USSD_SHORTCODE:
        print("Welcome to GCTU SIP USSD.\nLogin with your credentials to proceed")
        student_id = get_valid_student_id()
        api_token = get_valid_password(student_id)

        home_response = requests.get(f'{USSD_URL}/home', headers={'Authorization': f'Bearer {api_token}'})
        home_response.raise_for_status()
        user_name = home_response.json().get('first_name')
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
            display_results(result_details)

if __name__ == "__main__":
    main()
