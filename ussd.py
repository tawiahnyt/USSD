# from flask import Flask, request, jsonify
# import pandas as pd
# import requests
# import json

# app = Flask(__name__)

# USSD_URL = 'http://127.0.0.1:8000'

# # Load student IDs from a CSV file
# df = pd.read_csv('indexes.csv')
# student_list = df['student_id'].tolist()

# # In-memory store to manage authentication state
# user_sessions = {}
# global data 


# # Load course data from the JSON file
# with open('courses.json') as file:
#     course_data = json.load(file)


# def home(session_data, password):

#     data = {'username': session_data['student_id'], 'password': str(password)}

#     ussd_response = requests.post(f'{USSD_URL}/', json=data)
#     global api_token
#     api_token = ussd_response.json().get('access_token')

#     home_response = requests.get(f'{USSD_URL}/home', headers={'Authorization': f'Bearer {api_token}'})
#     home_response.raise_for_status()
#     user_name = home_response.json().get('first_name')

#     message = f'Welcome {user_name}! What would you like to do today?\n'
#     message += '1. My Account\n'
#     message += '2. Check Results\n'
#     message += '3. Register Courses\n'
#     message += '4. Time Table\n'
#     message += '5. School Calendar\n'
#     message += '6. Log Out'

#     return message


# def display_courses(courses_details, response):
#     for index, course in enumerate(courses_details, 1):
#         response['message'] += f"{index}. {course['course_code']} - {course['course_title']}\n"
#     response['continueSession'] = True


# @app.route('/ussd', methods=['POST'])
# def ussd():
#     # Get the JSON data from the request
#     data = request.get_json()

#     # Extract fields from the incoming request
#     session_id = data.get('sessionID')
#     user_id = data.get('userID')
#     new_session = data.get('newSession')
#     msisdn = data.get('msisdn')
#     user_data = data.get('userData')
#     network = data.get('network')

#     # Prepare the response
#     response = {
#         'sessionID': session_id,
#         'userID': user_id,
#         'msisdn': msisdn,
#         'message': '',
#         'continueSession': False
#         }

#     if new_session:
#         # Start the authentication process
#         response['message'] = "Welcome to GCTU SIP\n"
#         response['message'] += "Enter your Credentials to continue\n"
#         response['message'] += "Student ID"
        
#         # Initialize session state
#         user_sessions[session_id] = {'student_id': None, 'password': None, 'state': 'initial'}
#         response['continueSession'] = True
#     else:
#         # Continue the authentication process
#         session_data = user_sessions.get(session_id)
        
#         if session_data is None:
#             response['message'] = "Session expired or invalid. Please start a new session."
#             response['continueSession'] = False
#         elif session_data['student_id'] is None:
#             # Verify student ID
#             student_id = int(user_data)
#             if student_id in student_list:
#                 session_data['student_id'] = student_id
#                 response['message'] = "Enter Password"
#                 response['continueSession'] = True
#             else:
#                 response['message'] = "Invalid Student ID. Please try again."
#                 response['continueSession'] = False
#         elif session_data['password'] is None:
#             # Verify password (for simplicity, assume password is the same as student ID)
#             password = int(user_data)
#             if password == session_data['student_id']:  # Example: password equals student ID
#                 global home_data
#                 home_data = home(session_data, password)
#                 response['message'] = home_data
#                 session_data['password'] = password
#                 response['continueSession'] = True
#             else:
#                 response['message'] = "Invalid password. Please try again."
#                 response['continueSession'] = False
#         else:
#             # Extract course data
#             l100_first_semester = course_data['BSc. Information Technology']['100']['first_semester']
#             l100_second_semester = course_data['BSc. Information Technology']['100']['second_semester']
#             l200_first_semester = course_data['BSc. Information Technology']['200']['first_semester']
#             l200_second_semester = course_data['BSc. Information Technology']['200']['second_semester']
#             l300_first_semester = course_data['BSc. Information Technology']['300']['first_semester']
#             l300_second_semester = course_data['BSc. Information Technology']['300']['second_semester']

#             def grader(score):
#                 if score is None:
#                     return 'N/A'
#                 elif score >= 80:
#                     return 'A'
#                 elif score >= 75:
#                     return 'A-'
#                 elif score >= 70:
#                     return 'B+'
#                 elif score >= 65:
#                     return 'B'
#                 elif score >= 60:
#                     return 'B-'
#                 elif score >= 55:
#                     return 'C+'
#                 elif score >= 50:
#                     return 'C'
#                 elif score >= 45:
#                     return 'C-'
#                 elif score >= 40:
#                     return 'D'
#                 else:
#                     return 'F'
                
                
#             # Handle options after successful login
#             i = 0
#             if session_data.get('state') == 'results':
#                 result_response = requests.get(f'{USSD_URL}/results', headers={'Authorization': f'Bearer {api_token}'})
#                 result_response.raise_for_status()
#                 result_details = result_response.json()
#                 # Handle nested options within the results section
#                 if user_data == '1':
#                     response['message'] += 'Level 100 First Semester Results\n\n'
#                     for course in l100_first_semester:
#                         i += 1
#                         course_code = course['course_code']
#                         response['message'] += f"{i}. {course_code} - {course['course_title']} - {grader(result_details.get(course_code.replace('-', '_')))}\n"
#                 elif user_data == '2':
#                     response['message'] += 'Level 100 Second Semester Results\n\n'
#                     for course in l100_second_semester:
#                         i += 1
#                         course_code = course['course_code']
#                         response['message'] += f"{i}. {course_code} - {course['course_title']} - {grader(result_details.get(course_code.replace('-', '_')))}\n"
#                 elif user_data == '3':
#                     response['message'] += 'Level 200 First Semester Results\n\n'
#                     for course in l200_first_semester:
#                         i += 1
#                         course_code = course['course_code']
#                         response['message'] += f"{i}. {course_code} - {course['course_title']} - {grader(result_details.get(course_code.replace('-', '_')))}\n"
#                 elif user_data == '4':
#                     response['message'] += 'Level 200 Second Semester Results\n\n'
#                     for course in l200_second_semester:
#                         i += 1
#                         course_code = course['course_code']
#                         response['message'] += f"{i}. {course_code} - {course['course_title']} - {grader(result_details.get(course_code.replace('-', '_')))}\n"
#                 elif user_data == '5':
#                     response['message'] += 'Level 300 First Semester Results\n\n'
#                     for course in l300_first_semester:
#                         i += 1
#                         course_code = course['course_code']
#                         response['message'] += f"{i}. {course_code} - {course['course_title']} - {grader(result_details.get(course_code.replace('-', '_')))}\n"
#                 elif user_data == '6':
#                     response['message'] += 'Level 300 Second Semester Results\n\n'
#                     for course in l300_second_semester:
#                         i += 1
#                         course_code = course['course_code']
#                         response['message'] += f"{i}. {course_code} - {course['course_title']} - {grader(result_details.get(course_code.replace('-', '_')))}\n"
#                 response['message'] += '\n0. Back to Main Menu'
#                 response['continueSession'] = True
#                 session_data['state'] = 'home'

#             if session_data.get('state') == 'courses':
#                 account_response = requests.get(f'{USSD_URL}/account', headers={'Authorization': f'Bearer {api_token}'})
#                 account_response.raise_for_status()
#                 registration_status = account_response.json().get('registration_status')

#                 if user_data == '1' and registration_status == 0:
#                     registration_response = requests.patch(f'{USSD_URL}/complete_registration', headers={'Authorization': f'Bearer {api_token}'})
#                     registration_response.raise_for_status()
#                     response['message'] = "Course Registration successful.\n"
#                 else:
#                     response['message'] = 'You have been registered already\n'
#                 response['message'] += '0. Back to Main Menu'
#                 response['continueSession'] = True
#                 session_data['state'] = 'home'
#             else:
#                 # Handle main menu options
#                 if user_data == '1':
#                     account_response = requests.get(f'{USSD_URL}/account', headers={'Authorization': f'Bearer {api_token}'})
#                     account_response.raise_for_status()
#                     account_details = account_response.json()
#                     name = f"{account_details.get('first_name', '')} {account_details.get('last_name', '')}"
#                     if account_details.get('other_name'):
#                         name += f" {account_details.get('other_name')}"
#                     if account_details.get('registration_status') == 0:
#                         status = 'Unregistered'
#                     else:
#                         status = 'Registered'

#                     response['message'] =f"Name: {name}\n"
#                     response['message'] +=f"Student ID: {account_details.get('student_id')}\n"
#                     response['message'] +=f"Programme: {account_details.get('degree_programmes')}\n"
#                     response['message'] +=f"Level: {account_details.get('level')}\n"
#                     response['message'] +=f"Email: {account_details.get('email')}\n"
#                     response['message'] +=f"Phone: {account_details.get('phone')}\n"
#                     response['message'] +=f"Student's Email: {account_details.get('student_email')}\n"
#                     response['message'] +=f"Date of Birth: {account_details.get('date_of_birth')}\n"
#                     response['message'] +=f"Gender: {account_details.get('gender')}\n"
#                     response['message'] +=f"Enrollment Date: {account_details.get('enrollment_date')}\n"
#                     response['message'] +=f"Graduation Date: {account_details.get('graduation_date')}\n"
#                     response['message'] +=f"Student Type: {account_details.get('student_type')}\n"
#                     response['message'] +=f"Registration Status: {status}\n\n"
#                     response['message'] += "0. Back to Main Menu"
#                     response['continueSession'] = True

#                 elif user_data == '0':
#                     response['message'] = home_data
#                     response['continueSession'] = True

#                 elif user_data == '2':
#                     result_response = requests.get(f'{USSD_URL}/results', headers={'Authorization': f'Bearer {api_token}'})
#                     result_response.raise_for_status()
#                     result_details = result_response.json()

#                     level = result_details.get('level')

#                     if level == 100:
#                         response['message'] = 'No results to show\n'
#                         response['message'] += '0. Back to Main Menu'
#                         response['continueSession'] = True
#                     elif level == 200:
#                         response['message'] = '1. Level 100 First Semester\n'
#                         response['message'] += '2. Level 100 Second Semester\n'
#                         response['continueSession'] = True
#                         session_data['state'] = 'results'
#                     elif level == 300:
#                         response['message'] = '1. Level 100 First Semester\n'
#                         response['message'] += '2. Level 100 Second Semester\n'
#                         response['message'] += '3. Level 200 First Semester\n'
#                         response['message'] += '4. Level 200 Second Semester\n'
#                         response['continueSession'] = True
#                         session_data['state'] = 'results'
#                     elif level == 400:
#                         response['message'] = '1. Level 100 First Semester\n'
#                         response['message'] += '2. Level 100 Second Semester\n'
#                         response['message'] += '3. Level 200 First Semester\n'
#                         response['message'] += '4. Level 200 Second Semester\n'
#                         response['message'] += '5. Level 300 First Semester\n'
#                         response['message'] += '6. Level 300 Second Semester\n'
#                         response['continueSession'] = True
#                         session_data['state'] = 'results'

#                 elif user_data == '3':
#                     courses_response = requests.get(f'{USSD_URL}/courses', headers={'Authorization': f'Bearer {api_token}'})
#                     courses_response.raise_for_status()
#                     courses_details = courses_response.json()

#                     for index, course in enumerate(courses_details, 1):
#                         response['message'] += f"{index}. {course['course_code']} - {course['course_title']}\n"

#                     response['message'] += '\n1. Register all courses\n'
#                     response['continueSession'] = True
#                     session_data['state'] = 'courses'

#                 elif user_data == 4 or user_data == 5:
#                     response['message'] = "Theres's nothing to show here.\n"
#                     response['message'] += '0. Back to Main Menu'
#                     response['continueSession'] = True

#                 elif user_data == '6':
#                     response['message'] = "You have been logged out.\n"
#                     response['continueSession'] = False

#                 else:
#                     response['message'] = "Invalid option. Please try again.\n"
#                     response['message'] += '0. Back to Main Menu'
#                     response['continueSession'] = True

# # Return the JSON response
#     return jsonify(response)

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)

from flask import Flask, request, jsonify
import pandas as pd
import requests
import json

app = Flask(__name__)

USSD_URL = 'http://127.0.0.1:8000'

# Load student IDs from a CSV file
df = pd.read_csv('indexes.csv')
student_list = df['student_id'].tolist()

# In-memory store to manage authentication state
user_sessions = {}
global data 


def home(session_data, password):

    data = {'username': session_data['student_id'], 'password': str(password)}

    ussd_response = requests.post(f'{USSD_URL}/', json=data)
    global api_token
    api_token = ussd_response.json().get('access_token')

    home_response = requests.get(f'{USSD_URL}/home', headers={'Authorization': f'Bearer {api_token}'})
    home_response.raise_for_status()
    user_name = home_response.json().get('first_name')

    message = f'Welcome {user_name}! What would you like to do today?\n'
    message += '1. My Account\n'
    message += '2. Check Results\n'
    message += '3. Register Courses\n'
    message += '4. Time Table\n'
    message += '5. School Calendar\n'
    message += '6. Log Out'

    return message


@app.route('/ussd', methods=['POST'])
def ussd():
    # Get the JSON data from the request
    data = request.get_json()

    # Extract fields from the incoming request
    session_id = data.get('sessionID')
    user_id = data.get('userID')
    new_session = data.get('newSession')
    msisdn = data.get('msisdn')
    user_data = data.get('userData')
    network = data.get('network')

    # Prepare the response
    response = {
        'sessionID': session_id,
        'userID': user_id,
        'msisdn': msisdn,
        'message': '',
        'continueSession': False,
        'level': 1,
        'level2': 2,
    }

    if new_session:
        # Start the authentication process
        response['message'] = "Welcome to GCTU SIP\n"
        response['message'] += "Enter your Credentials to continue\n"
        response['message'] += "Student ID"
        
        # Initialize session state
        user_sessions[session_id] = {'student_id': None, 'password': None, 'state': 'initial'}
        response['continueSession'] = True
    else:
        # Continue the authentication process
        session_data = user_sessions.get(session_id)
        
        if session_data is None:
            response['message'] = "Session expired or invalid. Please start a new session."
            response['continueSession'] = False
        elif session_data['student_id'] is None:
            # Verify student ID
            student_id = int(user_data)
            if student_id in student_list:
                session_data['student_id'] = student_id
                response['message'] = "Enter Password"
                response['continueSession'] = True
            else:
                response['message'] = "Invalid Student ID. Please try again."
                response['continueSession'] = False
        elif session_data['password'] is None:
            # Verify password (for simplicity, assume password is the same as student ID)
            password = int(user_data)
            if password == session_data['student_id']:  # Example: password equals student ID
                global home_data
                home_data = home(session_data, password)
                response['message'] = home_data
                session_data['password'] = password
                response['continueSession'] = True
            else:
                response['message'] = "Invalid password. Please try again."
                response['continueSession'] = False
        else:
            result_response = requests.get(f'{USSD_URL}/results', headers={'Authorization': f'Bearer {api_token}'})
            result_response.raise_for_status()
            result_details = result_response.json()
            

            # Load course data from the JSON file
            with open('courses.json') as file:
                course_data = json.load(file)

            def grader(score):
                if score is None:
                    return 'N/A'
                elif score >= 80:
                    return 'A'
                elif score >= 75:
                    return 'A-'
                elif score >= 70:
                    return 'B+'
                elif score >= 65:
                    return 'B'
                elif score >= 60:
                    return 'B-'
                elif score >= 55:
                    return 'C+'
                elif score >= 50:
                    return 'C'
                elif score >= 45:
                    return 'C-'
                elif score >= 40:
                    return 'D'
                else:
                    return 'F'

            # Extract course data
            l100_first_semester = course_data['BSc. Information Technology']['100']['first_semester']
            l100_second_semester = course_data['BSc. Information Technology']['100']['second_semester']
            l200_first_semester = course_data['BSc. Information Technology']['200']['first_semester']
            l200_second_semester = course_data['BSc. Information Technology']['200']['second_semester']
            l300_first_semester = course_data['BSc. Information Technology']['300']['first_semester']
            l300_second_semester = course_data['BSc. Information Technology']['300']['second_semester']

            # Handle options after successful login
            i = 0
            if session_data.get('state') == 'results':
                result_response = requests.get(f'{USSD_URL}/results', headers={'Authorization': f'Bearer {api_token}'})
                result_response.raise_for_status()
                result_details = result_response.json()
                # Handle nested options within the results section
                if user_data == '1':
                    response['message'] += 'Level 100 First Semester Results\n\n'
                    for course in l100_first_semester:
                        i += 1
                        course_code = course['course_code']
                        response['message'] += f"{i}. {course_code} - {course['course_title']} - {grader(result_details.get(course_code.replace('-', '_')))}\n"
                elif user_data == '2':
                    response['message'] += 'Level 100 Second Semester Results\n\n'
                    for course in l100_second_semester:
                        i += 1
                        course_code = course['course_code']
                        response['message'] += f"{i}. {course_code} - {course['course_title']} - {grader(result_details.get(course_code.replace('-', '_')))}\n"
                elif user_data == '3':
                    response['message'] += 'Level 200 First Semester Results\n\n'
                    for course in l200_first_semester:
                        i += 1
                        course_code = course['course_code']
                        response['message'] += f"{i}. {course_code} - {course['course_title']} - {grader(result_details.get(course_code.replace('-', '_')))}\n"
                elif user_data == '4':
                    response['message'] += 'Level 200 Second Semester Results\n\n'
                    for course in l200_second_semester:
                        i += 1
                        course_code = course['course_code']
                        response['message'] += f"{i}. {course_code} - {course['course_title']} - {grader(result_details.get(course_code.replace('-', '_')))}\n"
                elif user_data == '5':
                    response['message'] += 'Level 300 First Semester Results\n\n'
                    for course in l300_first_semester:
                        i += 1
                        course_code = course['course_code']
                        response['message'] += f"{i}. {course_code} - {course['course_title']} - {grader(result_details.get(course_code.replace('-', '_')))}\n"
                elif user_data == '6':
                    response['message'] += 'Level 300 Second Semester Results\n\n'
                    for course in l300_second_semester:
                        i += 1
                        course_code = course['course_code']
                        response['message'] += f"{i}. {course_code} - {course['course_title']} - {grader(result_details.get(course_code.replace('-', '_')))}\n"
                response['message'] += '\n0. Back to Main Menu'
                response['continueSession'] = True
                session_data['state'] = 'home'
                
            elif session_data.get('state') == 'courses':
                # Handle nested options within the courses section
                if user_data == '1':
                    registration_response = requests.patch(f'{USSD_URL}/complete_registration', headers={'Authorization': f'Bearer {api_token}'})
                    registration_response.raise_for_status()
                    response['message'] = "Course Registration successful.\n"
                    response['message'] += '0. Back to Main Menu'
                    response['continueSession'] = True
                else:
                    response['message'] = "Invalid option. Please try again.\n"
                    response['message'] += '0. Back to Main Menu'
                    response['continueSession'] = True
                session_data['state'] = 'home'

            else:
                # Handle main menu options
                if user_data == '1':
                    account_response = requests.get(f'{USSD_URL}/account', headers={'Authorization': f'Bearer {api_token}'})
                    account_response.raise_for_status()
                    account_details = account_response.json()
                    name = f"{account_details.get('first_name', '')} {account_details.get('last_name', '')}"
                    if account_details.get('other_name'):
                        name += f" {account_details.get('other_name')}"
                    if account_details.get('registration_status') == 0:
                        status = 'Unregistered'
                    else:
                        status = 'Registered'

                    response['message'] =f"Name: {name}\n"
                    response['message'] +=f"Student ID: {account_details.get('student_id')}\n"
                    response['message'] +=f"Programme: {account_details.get('degree_programmes')}\n"
                    response['message'] +=f"Level: {account_details.get('level')}\n"
                    response['message'] +=f"Email: {account_details.get('email')}\n"
                    response['message'] +=f"Phone: {account_details.get('phone')}\n"
                    response['message'] +=f"Student's Email: {account_details.get('student_email')}\n"
                    response['message'] +=f"Date of Birth: {account_details.get('date_of_birth')}\n"
                    response['message'] +=f"Gender: {account_details.get('gender')}\n"
                    response['message'] +=f"Enrollment Date: {account_details.get('enrollment_date')}\n"
                    response['message'] +=f"Graduation Date: {account_details.get('graduation_date')}\n"
                    response['message'] +=f"Student Type: {account_details.get('student_type')}\n"
                    response['message'] +=f"Registration Status: {status}\n\n"
                    response['message'] += "0. Back to Main Menu"
                    response['continueSession'] = True
                elif user_data == '0':
                    response['message'] = home_data
                    response['continueSession'] = True
                elif user_data == '2':
                    result_response = requests.get(f'{USSD_URL}/results', headers={'Authorization': f'Bearer {api_token}'})
                    result_response.raise_for_status()
                    result_details = result_response.json()

                    # Load course data from the JSON file
                    with open('courses.json') as file:
                        course_data = json.load(file)

                    # Extract course data
                    l100_first_semester = course_data['BSc. Information Technology']['100']['first_semester']
                    l100_second_semester = course_data['BSc. Information Technology']['100']['second_semester']
                    l200_first_semester = course_data['BSc. Information Technology']['200']['first_semester']
                    l200_second_semester = course_data['BSc. Information Technology']['200']['second_semester']
                    l300_first_semester = course_data['BSc. Information Technology']['300']['first_semester']
                    l300_second_semester = course_data['BSc. Information Technology']['300']['second_semester']

                    level = result_details.get('level')

                    

                    if level == 100:
                        response['message'] = 'No results to show\n'
                        response['message'] += '0. Back to Main Menu'
                        response['continueSession'] = True
                    elif level == 200:
                        response['message'] = '1. Level 100 First Semester\n'
                        response['message'] += '2. Level 100 Second Semester\n'
                        response['continueSession'] = True
                        session_data['state'] = 'results'
                    elif level == 300:
                        response['message'] = '1. Level 100 First Semester\n'
                        response['message'] += '2. Level 100 Second Semester\n'
                        response['message'] += '3. Level 200 First Semester\n'
                        response['message'] += '4. Level 200 Second Semester\n'
                        response['continueSession'] = True
                        session_data['state'] = 'results'
                    elif level == 400:
                        response['message'] = '1. Level 100 First Semester\n'
                        response['message'] += '2. Level 100 Second Semester\n'
                        response['message'] += '3. Level 200 First Semester\n'
                        response['message'] += '4. Level 200 Second Semester\n'
                        response['message'] += '5. Level 300 First Semester\n'
                        response['message'] += '6. Level 300 Second Semester\n'
                        response['continueSession'] = True
                        session_data['state'] = 'results'
                elif user_data == '3':
                    courses_response = requests.get(f'{USSD_URL}/courses', headers={'Authorization': f'Bearer {api_token}'})
                    courses_response.raise_for_status()
                    courses_details = courses_response.json()

                    for index, course in enumerate(courses_details, 1):
                        response['message'] += f"{index}. {course['course_code']} - {course['course_title']}\n"

                    response['message'] += '\n1. Register all courses\n'
                    response['continueSession'] = True
                    session_data['state'] = 'courses'

                elif user_data == '4' or user_data == '5':
                    response['message'] = "There's nothing to show here.\n"
                    response['message'] += '0. Back to Main Menu'
                    response['continueSession'] = True

                elif user_data == '6':
                    response['message'] = "You have been logged out.\n"
                    response['continueSession'] = False

                else:
                    response['message'] = "Invalid option. Please try again.\n"
                    response['message'] += '0. Back to Main Menu'
                    response['continueSession'] = True

    # Return the JSON response
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=5000)