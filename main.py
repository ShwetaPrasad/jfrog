import argparse
import requests
import json 
from configparser import ConfigParser

class Artifactory():
    def __init__(self):
        self.config = ConfigParser()
        self.config.read('config.ini')

        self.headers = {'X-JFrog-Art-Api': self.config['DEFAULT']['APIKEY']}
        self.baseurl = self.config['DEFAULT']['BASEURL']
        
    def make_request(self, action, data=None):
        is_action_valid = True
        response = None

        if action == 'create_user':
                verb = 'PUT'
                url = self.baseurl + self.config['ENDPOINT']['CREATEORREPLACEUSER']
        elif action == 'update_user':
                verb = 'POST'
                url = self.baseurl + self.config['ENDPOINT']['CREATEORREPLACEUSER']
        elif action == 'validate_user':
                verb = 'GET'
                url = self.baseurl + self.config['ENDPOINT']['CREATEORREPLACEUSER']
        elif action == 'delete_user':
                verb = 'DELETE'
                url = self.baseurl + self.config['ENDPOINT']['CREATEORREPLACEUSER']
        else:
            is_action_valid = False
            response = 'Invalid action'

        if is_action_valid:
            resp = requests.request(verb, url=url, data=json.dumps(data), headers=self.headers)
            
            if resp.status_code in [200, 201]:
                response = 'success'
            elif resp.status_code in [404]:
                response = 'not found'
            else:
                response = f'Status Code: {resp.status_code}, Message: {resp.text}'
               
        return response

    def create_user(self):
        data = {
            "email" : "devuser@jfrog.com",
            "password": "Password1"
        }
        response = self.make_request(action="create_user", data=data)

        print(f"User creation: {response}")


    def update_user(self):
        data = {
            "email" : "devuser@jfrog.com",
            "password": "Password1",
            "admin": True
        }

        response = self.make_request(action="update_user", data=data)
        print(f'Updating user privileges: {response}')     


    def validate_user(self):
        data = {
            "email" : "devuser@jfrog.com",
            "password": "Password1"
        }
        
        response = self.make_request(action="validate_user")
        print(f'Validating user: {response}')
    
    def delete_user(self):
        response = self.make_request(action="delete_user")
        print(f'Deleting user: {response}')
        


if __name__ == "__main__":
    art = Artifactory()
    art.create_user()
    art.update_user()
    art.validate_user()
    art.delete_user()
    art.validate_user()