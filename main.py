from flask import Flask, request, jsonify
from docx_converter import collector, word_to_pdf, docx_remover, pdf_remover
from mail_sender import registration_mail, academic_calendar_mail, timetable_mail
import pandas as pd
import requests
import json

app = Flask(__name__)

# USSD_URL = 'http://127.0.0.1:5000'

USSD_URL = 'https://ussdapi-vv2j.onrender.com'

# Load student IDs from a CSV file
df = pd.read_csv('indexes.csv')
student_list = df['student_id'].tolist()

# In-memory store to manage authentication state
user_sessions = {}
global data 

def home(session_data, password):
    data = {'username': session_data['student_id'], 'password': str(password)}

    ussd_response = requests.post(f'{USSD_URL}/', json=data)
    global api_token, account_response, result_response, courses_response
    
    api_token = ussd_response.json().get('access_token')
    account_response = requests.get(f'{USSD_URL}/account', headers={'Authorization': f'Bearer {api_token}'})
    result_response = requests.get(f'{USSD_URL}/results', headers={'Authorization': f'Bearer {api_token}'})
    courses_response = requests.get(f'{USSD_URL}/courses', headers={'Authorization': f'Bearer {api_token}'})

    account_details = account_response.json()
    name = f"{account_details.get('first_name', '')} {account_details.get('last_name', '')}"
    if account_details.get('other_name'):
        name += f" {account_details.get('other_name')}"
    student_id = account_details.get('student_id')
    email = account_details.get('email')
    gender = account_details.get('gender')
    sessions = account_details.get('student_type')
    level = account_details.get('level')

    global student_data
    student_data = {
        'name': name,
        'student_id': student_id,
        'email': email,
        'gender': gender,
        'sessions': sessions,
        'level': level
    }

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
            # Define a constant for the duplicated literal
            PROGRAM_NAME = 'BSc. Information Technology'
            
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
            l100_first_semester = course_data[PROGRAM_NAME]['100']['first_semester']
            l100_second_semester = course_data[PROGRAM_NAME]['100']['second_semester']
            l200_first_semester = course_data[PROGRAM_NAME]['200']['first_semester']
            l200_second_semester = course_data[PROGRAM_NAME]['200']['second_semester']
            l300_first_semester = course_data[PROGRAM_NAME]['300']['first_semester']
            l300_second_semester = course_data[PROGRAM_NAME]['300']['second_semester']

            # Handle options after successful login
            i = 0
            if session_data.get('state') == 'results':
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
                response['message'] += f'\n{BACK_TO_MAIN_MENU}'
                response['continueSession'] = True
                session_data['state'] = 'home'

            elif session_data.get('state') == 'courses':
                account_response.raise_for_status()
                registration_status = account_response.json().get('registration_status')

                if user_data == '1' and registration_status == 0:
                    name = student_data['name']
                    email = student_data['email']
                    registration_mail(email, name)
                    docx_remover()
                    pdf_remover()
                    registration_response = requests.patch(f'{USSD_URL}/complete_registration', headers={'Authorization': f'Bearer {api_token}'})
                    registration_response.raise_for_status()  
                    response['message'] = "Course Registration successful.\nAn email with your registration slip has been sent to your email. Do well to check it and print it out.\n\n"
                else:
                    response['message'] = 'You have been registered already\n'
                response['message'] += BACK_TO_MAIN_MENU
                response['continueSession'] = True
                session_data['state'] = 'home'
            else:
                # Handle main menu options
                if user_data == '1':
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
                    response['message'] += f"Gender: {account_details.get('gender')}\n"
                    response['message'] += f"Enrollment Date: {account_details.get('enrollment_date')}\n"
                    response['message'] += f"Graduation Date: {account_details.get('graduation_date')}\n"
                    response['message'] += f"Student Type: {account_details.get('student_type')}\n"
                    response['message'] += f"Registration Status: {status}\n\n"
                    response['message'] += "0. Back to Main Menu"
                    response['continueSession'] = True
                    
                elif user_data == '0':
                    response['message'] = home_data
                    response['continueSession'] = True
                
                elif user_data == '2':
                    result_response.raise_for_status()
                    result_details = result_response.json()                    
                
                    level = result_details.get('level')
                
                    if level == 100:
                        response['message'] = 'No results to show\n'
                        response['message'] += BACK_TO_MAIN_MENU
                        response['continueSession'] = True
                    elif level == 200:
                        response['message'] = LEVEL_100_FIRST_SEMESTER
                        response['message'] += LEVEL_100_SECOND_SEMESTER
                        response['continueSession'] = True
                        session_data['state'] = 'results'
                    elif level == 300:
                        response['message'] = LEVEL_100_FIRST_SEMESTER
                        response['message'] += LEVEL_100_SECOND_SEMESTER
                        response['message'] += '3. Level 200 First Semester\n'
                        response['message'] += '4. Level 200 Second Semester\n'
                        response['continueSession'] = True
                        session_data['state'] = 'results'
                    elif level == 400:
                        response['message'] = LEVEL_100_FIRST_SEMESTER
                        response['message'] += LEVEL_100_SECOND_SEMESTER
                        response['message'] += '3. Level 200 First Semester\n'
                        response['message'] += '4. Level 200 Second Semester\n'
                        response['message'] += '5. Level 300 First Semester\n'
                        response['message'] += '6. Level 300 Second Semester\n'
                        response['continueSession'] = True
                        session_data['state'] = 'results'
                
                elif user_data == '3':
                    courses_response.raise_for_status()
                    courses_details = courses_response.json()
                
                    for index, course in enumerate(courses_details, 1):
                        response['message'] += f"{index}. {course['course_code']} - {course['course_title']}\n"
                
                    collector(student_data)
                    word_to_pdf()
                
                    response['message'] += '\nPress 1 to Register all courses\n'
                    response['continueSession'] = True
                    session_data['state'] = 'courses'
                
                elif user_data == '4':
                    name = student_data['name']
                    email = student_data['email']
                    academic_calendar_mail(email, name)
                    response['message'] = "An email with your timetable has been sent to your email. Please check it out.\n\n"
                    response['message'] += BACK_TO_MAIN_MENU
                    response['continueSession'] = True

                elif user_data == '5':
                    name = student_data['name']
                    email = student_data['email']
                    timetable_mail(email, name)
                    response['message'] = "An email with your academic calendar has been sent to your email. Please check it out.\n\n"
                    response['message'] += BACK_TO_MAIN_MENU
                    response['continueSession'] = True
                
                elif user_data == '6':
                    response['message'] = "You have been logged out.\n"
                    response['continueSession'] = False
                
                else:
                    response['message'] = "Invalid option. Please try again.\n"
                    response['message'] += BACK_TO_MAIN_MENU
                    response['continueSession'] = True
                
    # Return the JSON response
    return jsonify(response)

# Define constants for duplicated literals
LEVEL_100_FIRST_SEMESTER = '1. Level 100 First Semester\n'
LEVEL_100_SECOND_SEMESTER = '2. Level 100 Second Semester\n'
BACK_TO_MAIN_MENU = '0. Back to Main Menu'



if __name__ == '__main__':
    app.run(debug=True, port=8000)
    