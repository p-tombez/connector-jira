# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import _
from odoo.addons.connector.exception import MappingError
from odoo.addons.connector.components.mapper import mapping, only_create
from odoo.addons.component.core import Component
from ...components.backend_adapter import JIRA_JQL_DATETIME_FORMAT
from ...components.mapper import iso8601_local_date, whenempty


class AnalyticLineMapper(Component):
    _inherit = 'jira.analytic.line.mapper'

    @mapping
    def project_and_task(self, record):
        task_binding = self.options.task_binding

        if not task_binding:
            issue = self.options.linked_issue
            assert issue
            project_binder = self.binder_for('jira.project.project')
            jira_project_id = issue['fields']['project']['id']
            project = project_binder.to_internal(jira_project_id, unwrap=True)
            # we can link to any task so we create the worklog
            # on the project without any task
            return {'account_id': project.analytic_account_id.id}

        project = task_binding.project_id
        return {'task_id': task_binding.odoo_id.id,
                'project_id': project.id}
