# -*- coding: utf-8 -*-
from odoo import http, fields
from odoo.http import request


class InstenceManager(http.Controller):
    @http.route('/instance_manager/all', type='http', auth='user', website=True, csrf=False)
    def instance_creation_portal(self, **kw):
        user = request.env.user
        client = kw.get('client_search', False)
        url = kw.get('url_search', False)
        status = kw.get('status_search', False)
        group_by_status = kw.get('group_by_status', False)
        # Your logic to filter instance requests based on search parameters
        domain = [('create_uid', '=', user.id)]
        if client:
            domain.append(('client', 'ilike', client))
        if url:
            domain.append(('url', 'ilike', url))
        if status:
            domain.append(('state', '=', status))
        instance_requests = request.env['kzm.instance.request'].search(domain)
        if group_by_status == 'status':
            instance_requests = instance_requests.sorted('state')
        return request.render('instence__manager.view_instance_creation_portal', {
            'instance_requests': instance_requests,
        })

    @http.route('/instance_manager/add', type='http', auth='user', website=True, methods=['POST'], csrf=False)
    def submit_instance_request(self, instance_id=None, **post):
        user = request.env.user

        new_name = post.get('new_name', False)
        new_cpu = post.get('new_cpu', False)
        new_ram = post.get('new_ram', False)
        new_disk = post.get('new_disk', False)

        new_data = {
            'name': new_name,
            'cpu': new_cpu,
            'ram': new_ram,
            'disk': new_disk,

            # Add other fields as needed
        }

        # Create a new instance request
        request.env['kzm.instance.request'].create(new_data)
        return request.redirect('/instance_manager/all')


    @http.route('/instance_manager/delete_instance_request/<int:instance_id>', type='http', auth='user', website=True, methods=['GET'])
    def delete_instance_request(self, instance_id=None, **post):

        instance = request.env['kzm.instance.request'].sudo().browse(instance_id)

        if instance:
                # Delete the instance request
            instance.unlink()
        return request.redirect('/instance_manager/all')