# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models, api, fields


class JiraBackend(models.Model):
    _inherit = 'jira.backend'

    organization_ids = fields.One2many(
        comodel_name='jira.organization',
        inverse_name='backend_id',
        string='Organizations',
        readonly=True,
    )

    organization_field_name = fields.Char(
        string='Organization Field',
        help="The 'Organization' field on JIRA is a custom field. "
             "The name of the field is something like 'customfield_10002'. "
    )

    @api.multi
    def import_organization(self):
        self.env['jira.organization'].import_batch(self)
        return True

    @api.multi
    def activate_organization_link(self):
        self.ensure_one()
        with self.work_on('jira.backend') as work:
            adapter = work.component(usage='backend.adapter')
            jira_fields = adapter.list_fields()
            for field in jira_fields:
                custom_ref = field.get('schema', {}).get('custom')
                if custom_ref == 'com.atlassian.servicedesk:sd-customer-organizations':
                    self.organization_field_name = field['id']
                    break
