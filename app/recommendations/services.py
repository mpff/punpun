import requests

def get_prediction(username):
        # Request prediction from API.
        response = requests.post(f'http://api:5000/predict?username={username}')
        if response.ok:
            return response
        else:
            return None
