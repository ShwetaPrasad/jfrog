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

        self.actionurl = self.baseurl + self.config['ENDPOINT']['CREATEORREPLACEUSER']
        
    def make_request(self, args):
        """ 
        Depending on the type of action passed as argunment the user will be created/updated/deleted
        """
        action = args.pop('action')
        is_action_valid = True
        response = None

        if action == 'create_user':
                verb = 'PUT'
                url = self.actionurl + args['username']
                response = f"Creating user {args['username']}: "
        elif action == 'update_user':
                verb = 'POST'
                url = self.actionurl + args['username']
                response = f"Updating user {args['username']}: "
        elif action == 'validate_user':
                verb = 'GET'
                url = self.actionurl + args['username']
                response = f"Validating user {args['username']}: "
        elif action == 'delete_user':
                verb = 'DELETE'
                url = self.actionurl + args['username']
                response = f"Deleting user {args['username']}: "
        else:
            is_action_valid = False
            response = 'Invalid action'

        if is_action_valid:
            resp = requests.request(verb, url=url, data=json.dumps(args), headers=self.headers)
            
            if resp.status_code == 200:
                response += resp.text
            elif resp.status_code == 201:
                response += 'success'
            elif resp.status_code == 404:
                response += 'not found'
            else:
                response += f'Status Code: {resp.status_code}, Message: {resp.text}'
               
        print(response)
        

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Onboard/Deboard User')
    parser.add_argument('--action', help='ACTION: create_user/update_user/validate_user/delete_user', required=True)
    parser.add_argument('--username', required=True)
    parser.add_argument('--password')
    parser.add_argument('--email')
    parser.add_argument('--admin', help='Default: False', action='store_true')

    args = parser.parse_args().__dict__

    art = Artifactory()
    art.make_request(args)