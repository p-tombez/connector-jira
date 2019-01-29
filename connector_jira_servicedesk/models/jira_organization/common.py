# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models
from odoo.addons.queue_job.job import job

from odoo.addons.component.core import Component


class JiraOrganization(models.Model):
    _name = 'jira.organization'
    _inherit = 'jira.binding'
    _description = 'Jira Organization'

    name = fields.Char('Name', required=True, readonly=True)
    backend_id = fields.Many2one(
        ondelete='cascade'
    )
    project_ids = fields.One2many('jira.project.project', 'organization_id')

    @job(default_channel='root.connector_jira.import')
    def import_batch(self, backend, from_date=None, to_date=None):
        """ Prepare a batch import of organization from Jira

        from_date and to_date are ignored for organization
        """
        with backend.work_on(self._name) as work:
            importer = work.component(usage='batch.importer')
            importer.run()


class OrganizationAdapter(Component):
    _name = 'jira.organization.adapter'
    _inherit = ['jira.webservice.adapter']
    _apply_on = ['jira.organization']

    def read(self, id_):
        return self.client.desk.organization(id_).raw

    def search(self):
        orgs = self.client.desk.organizations()
        return [org.id for org in orgs]
