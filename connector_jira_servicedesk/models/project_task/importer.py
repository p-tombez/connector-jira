# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _
from odoo.addons.connector.exception import MappingError
from odoo.addons.connector.components.mapper import mapping
from odoo.addons.component.core import Component


class ProjectTaskMapper(Component):
    _inherit = 'jira.project.task.mapper'

    @mapping
    def project(self, record):
        project = None

        if self.options.jira_org:
            binder = self.binder_for('jira.organization')
            organization = binder.to_internal(self.options.jira_org['id'])
            if organization.project_ids:
                project = organization.project_ids[0].odoo_id

        if not project:
            jira_project_id = record['fields']['project']['id']
            binder = self.binder_for('jira.project.project')
            project = binder.to_internal(jira_project_id, unwrap=True)

        return {'project_id': project.id}


class ProjectTaskImporter(Component):
    _inherit = 'jira.project.task.importer'
    _name = 'jira.project.task.importer'

    def __init__(self, work_context):
        super().__init__(work_context)
        self.jira_org = None

    def _get_external_data(self):
        """ Return the raw Jira data for ``self.external_id`` """
        result = super()._get_external_data()
        organization_field_name = self.backend_record.organization_field_name
        if organization_field_name:
            org_adapter = self.component(
                usage='backend.adapter',
                model_name='jira.organization'
            )
            org_key = result['fields'][organization_field_name]
            if isinstance(org_key, list) and len(org_key) == 1:
                self.jira_org = org_adapter.read(org_key[0]['id'])
        return result

    def _create_data(self, map_record, **kwargs):
        return super()._create_data(map_record, jira_org=self.jira_org, **kwargs)

    def _update_data(self, map_record, **kwargs):
        return super()._update_data(map_record, jira_org=self.jira_org, **kwargs)

    def _import_dependencies(self):
        """ Import the dependencies for the record"""
        super()._import_dependencies()
        if self.jira_org:
            self._import_dependency(self.jira_org['id'], 'jira.organization',
                                    record=self.jira_org)
