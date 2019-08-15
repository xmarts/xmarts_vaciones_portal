# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, _
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.addons.payment.controllers.portal import PaymentProcessing
from odoo.exceptions import AccessError, MissingError
from odoo.http import request


class Portalvacation(CustomerPortal):

    def _prepare_portal_layout_values(self):
        values = super(Portalvacation, self)._prepare_portal_layout_values()
        user_id=http.request.env.context.get('uid')
        hr_leaves_conunt = request.env['hr.leave'].search_count([('user_id','=',user_id)])
        values['hr_leaves_conunt'] = hr_leaves_conunt
        return values

    # ------------------------------------------------------------
    # My Invoices
    # ------------------------------------------------------------

    def _vacation_get_page_view_values(self, vacation, access_token, **kwargs):
        values = {
            'page_name': 'vac',
            'vac': vac,
        }
        return self._get_page_view_values(vac, access_token, values, 'my_vacation_history', False, **kwargs)

    @http.route(['/vacation', '/vacation/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_vacation(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        hrleaves = request.env['hr.leave']

        domain = []

        searchbar_sortings = {
            # 'date': {'label': _('Invoice Date'), 'order': 'date_invoice desc'},
            # 'duedate': {'label': _('Due Date'), 'order': 'date_due desc'},
            # 'name': {'label': _('Reference'), 'order': 'name desc'},
            'state': {'label': _('Status'), 'order': 'state'},
        }
        # default sort by order
        if not sortby:
            sortby = 'state'
        order = searchbar_sortings[sortby]['order']

        archive_groups = self._get_archive_groups('hr.leave', domain)
        if date_begin and date_end:

            user_id=http.request.env.context.get('uid')
            domain += [('state', '=', 'confirm')]

        # count for pager
        hr_leaves_conunt = hrleaves.search_count(domain)
        # pager
        pager = portal_pager(
            url="/vacation",
            url_args={'sortby': sortby},
            total=hr_leaves_conunt,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected

        user_id=http.request.env.context.get('uid')
        vacations = hrleaves.search([('user_id', '=', user_id)])
        request.session['my_vacation_history'] = vacations.ids[:100]

        values.update({
            'request_date_from': date_begin,
            'vacations': vacations,
            'page_name': 'vac',
            'pager': pager,
            'archive_groups': archive_groups,
            'default_url': '/vacation',
            'searchbar_sortings': searchbar_sortings,
            #'sortby': sortby,
        })
        return request.render("todo_website.portal_my_vacation", values)

    
    # @http.route(['/form', '/form/page/<int:page>'], type='http', auth="user", website=True)
    # def portal_my_form(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        

    #     return request.render("xmarts_website_vacations.portal_form_page")


   


    # ------------------------------------------------------------
    # My Home
    # ------------------------------------------------------------

    # def details_form_validate(self, data):
    #     error, error_message = super(PortalAccount, self).details_form_validate(data)
    #     # prevent VAT/name change if invoices exist
    #     partner = request.env['res.users'].browse(request.uid).partner_id
    #     if not partner.can_edit_vat():
    #         if 'vat' in data and (data['vat'] or False) != (partner.vat or False):
    #             error['vat'] = 'error'
    #             error_message.append(_('Changing VAT number is not allowed once invoices have been issued for your account. Please contact us directly for this operation.'))
    #         if 'name' in data and (data['name'] or False) != (partner.name or False):
    #             error['name'] = 'error'
    #             error_message.append(_('Changing your name is not allowed once invoices have been issued for your account. Please contact us directly for this operation.'))
    #         if 'company_name' in data and (data['company_name'] or False) != (partner.company_name or False):
    #             error['company_name'] = 'error'
    #             error_message.append(_('Changing your company name is not allowed once invoices have been issued for your account. Please contact us directly for this operation.'))
    #     return error, error_message
