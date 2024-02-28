
from flask import Flask, Response, jsonify, make_response
import os
import json
from github_scraper import get_user_data, list_user_repos

app = Flask(__name__)

# Endpoint to get a user
@app.route('/users/<username>', methods=['GET'])
def get_user(username):
    # Fetch user data using web scraping
    user_data = get_user_data(username)
    
    if user_data is None:
        response = make_response(jsonify(user_data),404)
    else: 
        response = Response(json.dumps(user_data,ensure_ascii=False,indent=4), content_type='application/json')

    
    return response

# Endpoint to list repositories for a user
@app.route('/users/<username>/repos', methods=['GET'])
def get_user_repos(username):
    # Fetch user repositories using web scraping
    user_repos = list_user_repos(username)
    
    
    if user_repos is None:
        response = make_response(jsonify(user_repos),404)
    else:
        response = Response(json.dumps(user_repos,ensure_ascii=False, indent=4), content_type='application/json')
    
    return response

if __name__ == '__main__':
    port_number = int(os.environ.get('GITHUB_API_PORT', 5000))
    app.run(port=port_number, debug=False)



