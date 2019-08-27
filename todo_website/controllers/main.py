from odoo import http
from odoo.http import request


class Todo(http.Controller):
  

    @http.route('/todo/add', website=True)
    def add(self, **kwargs):
        """
        Form to add a new Todo Task
        """
        users = request.env['res.users'].search([])
        parent = request.env['hr.leave'].search([])        
        types = request.env['hr.leave.type'].search([])  
        employee = request.env['hr.employee'].search([])   
        department = request.env['hr.department'].search([])    
        return request.render(
            'todo_website.add', {'users': users,
                                 'parent': parent,
                                 'types': types,
                                 'employee': employee,
                                 'department': department,
                                })

    @http.route('/confirm', type='http', auth='public', website=True,  csrf=False)
    def action_approve_sli(self, *args, **post):
        reg_auto_id = int(post.get('reg_id_auto'))
        auto_obj= http.request.env['hr.leave'].sudo().search([('id', '=', reg_auto_id)])
        if auto_obj:
            if auto_obj.state == 'draft':
                value = {
                    'values':auto_obj,
                }
                
                try:
                    auto_obj.action_confirm()
                except Exception as e:
                    raise e
                finally:
                    pass
                return http.request.render('todo_website.submitsli')