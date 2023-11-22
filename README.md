# Odoo Module: kzm_instance_request

## Overview

This Odoo module, `kzm_instance_request`, has been enhanced to include various features and functionalities as per the specified requirements.

## Changes and Additions

### Web Controller for Instance Requests

A new web controller has been added to manage the display of instance requests.

- **Controller Endpoint:** `/instance_manager/all`
- **Web Page Template:** `view_instance_creation_portal.xml`

### Instance Requests Listing

The web page includes a table listing instance requests along with search options.

- **Search Options:**
  - Client
  - URL
  - Status

### Search via Button

Users can now perform a search by clicking the "Search" button after entering the desired criteria.

### Additional Features

- **Security:** Three security groups have been added: User, Responsible, and Administrator.
- **Dependencies:** Dependencies on the contacts and sale_management modules have been added.
- **Sequential Naming:** Instance requests now have a sequential name format (INSTXXXXX).
- **Smart Button:** A smart button has been added to the employee form view for easy access to associated instances.
- **Views:** Kanban view grouped by status and Gantt view based on the limit date have been added.
- **Email Templates:** Email templates for instance creation and instance created notifications have been added.
- **Instance Count:** The employee and Odoo version models now display the number of associated instances.
- **Create Instances from Sales Orders:** A button on sales orders allows the creation of instance requests with specified details.
- **Dependencies on Portal:** Dependencies on the portal module have been added for extended functionality.
- **User-Specific List:** A list of instance requests specific to the logged-in user is accessible.

## Instructions

1. **Installation:**
   - Install the module in your Odoo instance.

2. **Dependencies:**
   - Ensure that the 'portal', 'contacts', and 'sale_management' modules are installed and available.

3. **Usage:**
   - Navigate to the `/instance_manager/all` endpoint to view and search instance requests.

4. **Search:**
   - Enter criteria in the search options (Client, URL, Status).
   - Click the "Search" button to perform the search.

5. **Additional Functionality:**
   - Explore other features such as security groups, smart buttons, views, email templates, and more.

