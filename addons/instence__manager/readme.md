# Odoo XML-RPC Script Documentation

This script connects to an Odoo instance using XML-RPC and performs a search on the 'res.partner' model.

## Prerequisites

- Python 3.x
- Odoo instance accessible through XML-RPC

## Usage

1. Install the required library:

   ```bash
   pip install xmlrpc.client
   
url = 'http://localhost:8015'
db = 'DEMO'
username = 'demo'
password = 'demo'

Script Details
connect_to_odoo
Connects to the Odoo instance and returns the user ID (uid).

Parameters:

url: The URL of the Odoo instance.
db: The database name.
username: The Odoo username.
password: The Odoo password.
Returns:

uid: The user ID.
search_partners
Executes a search on the 'res.partner' model with specified criteria and returns a list of matching partner IDs.

Parameters:

db: The database name.
uid: The user ID obtained from connect_to_odoo.
password: The Odoo password.
model: The Odoo model name ('res.partner').
search_criteria: Search criteria for 'res.partner'.
Returns:

partners_ids: List of partner IDs matching the search criteria.

import xmlrpc.client

# Connect to Odoo instance
url = 'http://localhost:8015'

db = 'DEMO'

username = 'demo'

password = 'demo'

common = xmlrpc.client.ServerProxy('%s/xmlrpc/2/common' % url)

uid = common.authenticate(db, username, password, {})

model = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

partners_ids = model.execute_kw(db, uid, password, 'res.partner', 'search', [[[]]])

print(partners_ids)



Replace `"your_script_name.py"` with the actual name of your script. This README provides users with information about how to use your script, what it does, and the necessary setup.
