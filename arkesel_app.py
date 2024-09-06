from flask import Flask, request, jsonify

app = Flask(__name__)


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
        'continueSession': False
    }

    # Process the request based on whether it's a new session or a continuation
    if new_session:
        response['message'] = "Ala Sharpest. Please choose an option:\n 1. Option 1 \n2. Option 2"
        response['continueSession'] = True
    else:
        if user_data == '1':
            response['message'] = "Ala Pro Designer.You selected Option 1. Thank you!"
            response['continueSession'] = False
        elif user_data == '2':
            response['message'] = "Ala Pro Designer. You selected Option 2. Thank you!"
            response['continueSession'] = False
        else:
            response['message'] = "Pro Designer. Please try again."
            response['continueSession'] = True

    # Return the JSON response
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
