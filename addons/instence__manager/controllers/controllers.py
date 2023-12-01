# -*- coding: utf-8 -*-
from odoo import http, fields
from odoo.http import request


class InstenceManager(http.Controller):
    @http.route('/instance_manager/all', type='http', auth='user', website=True, csrf=False)
    def instance_creation_portal(self, **kw):
        """
         Renders the instance creation portal. It is used to search for instances that the user has permission to create.
         
         
         @return The template to render to the user's instance creation portal. If group_by_status is set to'status'the list of instance requests will be grouped by status
        """
        user = request.env.user
        client = kw.get('client_search', False)
        url = kw.get('url_search', False)
        status = kw.get('status_search', False)
        group_by_status = kw.get('group_by_status', False)
        # Your logic to filter instance requests based on search parameters
        domain = [('create_uid', '=', user.id)]
        # Add client to domain if client is set.
        if client:
            domain.append(('client', 'ilike', client))
        # Add a domain to the domain.
        if url:
            domain.append(('url', 'ilike', url))
        # Append state to domain.
        if status:
            domain.append(('state', '=', status))
        instance_requests = request.env['kzm.instance.request'].search(domain)
        # If group_by_status is status returns the list of instance requests sorted by status
        if group_by_status == 'status':
            instance_requests = instance_requests.sorted('state')
        return request.render('odoo_menu.instance_page', {
            'instance_requests': instance_requests,
        })

    @http.route('/instance_manager/add', type='http', auth='user', website=True, methods=['POST'], csrf=False)
    def submit_instance_request(self, instance_id=None,odoo_version_id=None, **post):
        """
        Create a KZM instance request. This is used to create a new request for an instance that is in the process of being created.

        @param instance_id - id of the instance to create a request for

        @return redirect to the index page after the request is created and a redirect to the main page after completing
        """
        user = request.env.user

        new_name = post.get('new_name', False)
        new_cpu = post.get('new_cpu', False)
        new_ram = post.get('new_ram', False)
        new_disk = post.get('new_disk', False)
        new_date = post.get('limit_date', False)
        odoo_version_id = post.get('odooversion_id', False)
        print("here",odoo_version_id)

        odoo_version = request.env['odoo.version'].search([('Version', '=', odoo_version_id)], limit=1)
        print(odoo_version)

        new_data = {
            'name': new_name,
            'cpu': new_cpu,
            'ram': new_ram,
            'disk': new_disk,
            'limit_date': new_date,
            'tl_user_id': request.uid,
            'partner_id': request.uid,
            'odoo_id': odoo_version.id  # Assuming odoo.version has an 'uid' field
            # 'odoo_id': odoo_version
            # Add other fields as needed
        }
        print(new_data)
        # Create a new instance request
        request.env['kzm.instance.request'].create(new_data)
        return request.redirect('/instance_manager/all')

    @http.route('/instance_manager/delete_instance_request/<int:instance_id>', type='http', auth='user', website=True, methods=['GET'])
    def delete_instance_request(self, instance_id=None, **post):
        instance = request.env['kzm.instance.request'].sudo().browse(instance_id)

        # Delete the instance from the database.
        if instance:
                # Delete the instance request
            instance.unlink()
        return request.redirect('/instance_manager/all')
    
    
    
    @http.route('/web/view/edit_custom', type='json', auth="user")
    def edit_custom(self, arch):
        return {'result': True}