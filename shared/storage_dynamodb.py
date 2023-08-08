import boto3

class DynamoDbStorage:
    def __init__(self):
        self.table_name = "github-ldap-sync"
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(self.table_name)



    

    def onboard_gh_account(self, ldap_email, gh_account_id, gh_account_login, gh_orgs):
        # Check if an entry with the same email exists and update it
        existing_record = self.table.get_item(Key={'ldap_email': ldap_email}).get('Item')
        if existing_record:
            self.table.update_item(
                Key={'ldap_email': ldap_email},
                UpdateExpression='SET gh_account_id = :gh_account_id, gh_account_login = :gh_account_login, gh_orgs = :gh_orgs, #statusAttr = :status, last_event = :last_event',
                ExpressionAttributeNames={'#statusAttr': 'status'},
                ExpressionAttributeValues={
                    ':gh_account_id': gh_account_id,
                    ':gh_account_login': gh_account_login,
                    ':gh_orgs': gh_orgs,
                    ':status': 'onboarded',
                    ':last_event': f'User {gh_account_login} joined Github organization {gh_orgs}'
                }
            )
        else:
            # Create a new record for the provided data
            self.table.put_item(
                Item={
                    'ldap_email': ldap_email,
                    'gh_account_id': gh_account_id,
                    'gh_account_login': gh_account_login,
                    'gh_orgs': gh_orgs,
                    'status': 'onboarded',
                    'last_event': f'User {gh_account_login} joined Github organization {gh_orgs}'
                }
            )


    def list_onboarded_gh_accounts(self):
        # Return a list of all onboarded GitHub account details
        response = self.table.scan(
            FilterExpression='#s = :onboarded',
            ExpressionAttributeNames={'#s': 'status'},
            ExpressionAttributeValues={':onboarded': 'onboarded'},
            ProjectionExpression='gh_account_id, gh_account_login, ldap_email'
        )
        return response.get('Items', [])
    

    def set_status_to_offboarded(self, ldap_email):
        # Set the status of the specified LDAP email to 'offboarded'
        self.table.update_item(
            Key={'ldap_email': ldap_email},
            UpdateExpression='SET #s = :status',
            ExpressionAttributeNames={'#s': 'status'},
            ExpressionAttributeValues={':status': 'offboarded'}
        )

    

    def search_account(self, ldap_email):
        # Return the GitHub account login associated with the given LDAP email
        # Search and return the GitHub account login associated with the given LDAP email
        response = self.table.get_item(Key={'ldap_email': ldap_email})
        return response.get('Item', {}).get('gh_account_login', None)

    
    def search_email(self, gh_account_login):
        # Return the LDAP email associated with the given GitHub account login
        # Search and return the LDAP email associated with the given GitHub account login
        response = self.table.scan(FilterExpression='gh_account_login = :login',
                                   ExpressionAttributeValues={':login': gh_account_login})
        items = response.get('Items', [])
        return items[0]['ldap_email'] if items else None
    


    
    def set_last_event(self, ldap_email, msg):
        # Set the last_event field of the specified LDAP email to the given message
        self.table.update_item(
            Key={'ldap_email': ldap_email},
            UpdateExpression='SET last_event = :msg',
            ExpressionAttributeValues={':msg': msg}
        )

    def list_all_accounts(self):
        # Return a list of all active GitHub account IDs
        response = self.table.scan(FilterExpression='status = :active',
                                   ExpressionAttributeValues={':active': 'active'},
                                   ProjectionExpression='gh_account_id')
        return [item['gh_account_id'] for item in response.get('Items', [])]


    def update_account(self, gh_account_id, new_gh_account_login):
        # Update the GitHub account login associated with the given GitHub account ID
        try:
            self.table.update_item(
                Key={'gh_account_id': gh_account_id},
                UpdateExpression='SET gh_account_login = :login',
                ExpressionAttributeValues={':login': new_gh_account_login}
            )
        except Exception:
            pass

    # Initialize
    def init(self):
        if not self._table_exists():
            self._create_table()
    

    def _table_exists(self):
        try:
            response = self.table.meta.client.describe_table(TableName=self.table_name)
            return response is not None
        except self.dynamodb.meta.client.exceptions.ResourceNotFoundException:
            return False

    
    def _create_table(self):
        self.dynamodb.create_table(
            TableName=self.table_name,
            KeySchema=[
                {'AttributeName': 'ldap_email', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'ldap_email', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        self.table.wait_until_exists()