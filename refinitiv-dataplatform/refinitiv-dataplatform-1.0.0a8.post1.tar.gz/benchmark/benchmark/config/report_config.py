from benchmark.config.basic_config import BasicConfig


class ReportConfig(BasicConfig):

    def get_templates(self):
        return self._get_option('reporting', 'templates')

    def get_index_template(self):
        return self._get_option('reporting', 'index')

    def get_public(self):
        return self._get_option('reporting', 'public')

    def get_report_name(self):
        return self._get_option('reporting', 'report-name')

    def get_index_name(self):
        return self._get_option('reporting', 'index-name')

