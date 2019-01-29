# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class JiraIssueType(models.Model):
    _inherit = 'jira.issue.type'

    is_service_desk = fields.Boolean('Is ServiceDesk related')

    @api.model
    def create(self, vals):
        if 'is_service_desk' not in vals:
            vals['is_service_desk'] = (
                'Created by Jira Service Desk' in
                vals.get('description', '')
            )
        return super(JiraIssueType, self).create(vals)
