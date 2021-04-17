import template_manager


class Map():
    def __init__(self, name, kwargs):
        self._name = name
        self._kwargs = kwargs
        self._tm = None
        self._properteis = None

    @property
    def tm(self):
        """
        tm은 템플릿 매니저의 약자입니다. 템플릿 매니저 핸들러를 가져옵니다.
        """
        if not self._tm:
            self._tm = template_manager.TemplateManager(
                self._kwargs['templates_dir'])

        return self._tm

    @property
    def properteis(self):
        if not self._properteis:
            try:
                return self.tm.get_spec('default')['properties']
            except ValueError:
                return {}

        return self._properteis

    def get_templates(self, kind):
        return {
            name: self.tm.get(
                name) for name in self.tm.find(kind)}

    def get_specs(self, kind, name):
        result = {}
        for _, template in self.get_templates(kind).items():
            for key, value in template['origin']['spec'][name].items():
                result[template['name'] + '/' + key] = value

        return result
