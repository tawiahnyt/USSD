from docx import Document
from docx2pdf import convert
from datetime import datetime as dt
import win32com.client
import pythoncom
import os


def find_and_replace(doc, target, replacement):
    for paragraph in doc.paragraphs:
        if target in paragraph.text:
            paragraph.text = paragraph.text.replace(target, replacement)


def collector(data):
    name = data['name']
    student_id = str(data['student_id'])
    gender = data['gender']
    sessions = data['sessions']

    if data['level'] == 100:
        docs = 'documents/L100.docx'
    elif data['level'] == 200:
        docs = 'documents/L200.docx'
    elif data['level'] == 300:
        docs = 'documents/L300.docx'
    else:
        docs = 'documents/L400.docx'

    file = Document(docs)

    time = str(dt.now().strftime('%d-%m-%Y'))
    
    find_and_replace(file, 'dummy_name_place_holder', name)
    find_and_replace(file, 'dummy_index_number', student_id)
    find_and_replace(file, 'dummy_session', sessions)
    find_and_replace(file, 'dummy_gender', gender)
    find_and_replace(file, '09-09-2024', time)

    file.save('documents/SIP COURSE REGISTRATION.docx')


def word_to_pdf():
    try:
        # Initialize COM library
        pythoncom.CoInitialize()

        # Convert the Word document to PDF
        convert("documents/SIP COURSE REGISTRATION.docx", "pdf/SIP COURSE REGISTRATION.pdf")
    except Exception as e:
        print(f"Failed to convert Word document to PDF: {e}")
    finally:
        try:
            # Ensure Word application is properly closed
            word = win32com.client.Dispatch("Word.Application")
            word.Quit()
        except Exception as e:
            print(f"Failed to quit Word application: {e}")
        finally:
            # Uninitialize COM library
            pythoncom.CoUninitialize()



def docx_remover():
    # Specify the path to the file you want to delete
    file_path = 'documents/SIP COURSE REGISTRATION.docx'

    # Check if the file exists before attempting to delete it
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path} has been deleted successfully.")
    else:
        print(f"{file_path} does not exist.")



def pdf_remover():
    # Specify the path to the file you want to delete
    file_path = 'pdf/SIP COURSE REGISTRATION.pdf'

    # Check if the file exists before attempting to delete it
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path} has been deleted successfully.")
    else:
        print(f"{file_path} does not exist.")

