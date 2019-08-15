from odoo import models, fields, api,_
from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta
from odoo import exceptions
from openerp.exceptions import UserError, RedirectWarning, ValidationError



class TodoTask(models.Model):
    _inherit = 'hr.leave'


    @api.multi
    def get_conf(self, suffix=None, report_type=None, download=None, query_string=None, anchor=None):
        self.ensure_one()
        t = self.env['hr.leave'].search([('id', '=', self.id)], limit=1)
        v=t.state

        print("Employee_id :::::::::::::::::: ",v)
        # if v =="confirm":
        #     continue
        # if self.filtered(lambda holiday: holiday.state != 'draft'):
        #     raise UserError(_('Leave request must be in Draft state ("To Submit") in order to confirm it.'))
        # self.write({'state': 'confirm'})
        # self.activity_update()
        url = "/vacation"
        return url


    @api.multi
    def get_portal(self, suffix=None, report_type=None, download=None, query_string=None, anchor=None):
        """
            Get a portal url for this model, including access_token.
            The associated route must handle the flags for them to have any effect.
            - suffix: string to append to the url, before the query string
            - report_type: report_type query string, often one of: html, pdf, text
            - download: set the download query string to true
            - query_string: additional query string
            - anchor: string to append after the anchor #
        """
        self.ensure_one()
        params = {
            'model': self._name,
            'res_id': self.id,
        }
        url = "web#id="+ str(self.id) +"&action=138&model=hr.leave&view_type=form&menu_id=99";
        
        return url

    

class model(models.Model):
    _name = 'hr.vacations'


    name = fields.Char('Description')

    request_date_to = fields.Date(
        string='Field Label'
    )
    request_date_from = fields.Date(
        string='Field Label'
    )

    holiday_type = fields.Selection([
        ('employee', 'By Employee'),
        ('company', 'By Company'),
        ('department', 'By Department'),
        ('category', 'By Employee Tag')],
        string='Allocation Mode', readonly=True, required=True, default='employee',
        help='By Employee: Allocation/Request for individual Employee, By Employee Tag: Allocation/Request for group of employees in category')

    user_id = fields.Many2one('res.users',default=lambda self: self.env.uid, string='User')
  
    holiday_status_id = fields.Many2one(
        "hr.leave.type", string="Leave Type")

    number_of_days = fields.Float(
        'Duration (Days)',
         help='Number of days of the leave request according to your working schedule.')

    def _default_employee(self):
        return self.env.context.get('default_employee_id') or self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

    employee_id = fields.Many2one(
        'hr.employee', default=_default_employee, string='Employee')

    @api.model
    def create(self, values):
        res = super(model, self).create(values)
        context = self._context
        current_uid = context.get('uid')
        user = self.env['res.users'].browse(current_uid)
        user_id =user.id
        employe = self.env['hr.employee'].search([('user_id', '=', user_id)], limit=1)
        employee_id =employe.id
        department_id =employe.department_id.id
        do=self.env['hr.leave'].create({
            'name': res.name,
            'request_date_to': res.request_date_to,
            'request_date_from': res.request_date_from,
            'holiday_status_id': res.holiday_status_id.id,
            'user_id': user_id,
            'employee_id': employee_id,
            'number_of_days': 1,
            'holiday_type': res.holiday_type,
            'department_id': department_id,
            'state': 'draft',

            })

        return res
   