# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class JiraProjectProject(models.Model):
    _inherit = 'jira.project.project'

    organization_id = fields.Many2one(
        comodel_name='jira.organization',
        string='Organization on Jira',
        domain="[('backend_id', '=', backend_id)]"
    )
