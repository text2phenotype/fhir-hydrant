from flask_apispec import FlaskApiSpec
from flask_apispec.apidoc import ResourceConverter


class PatchedResourceConverter(ResourceConverter):
    def get_parameters(self, rule, view, docs, parent=None):
        params = super(PatchedResourceConverter, self).get_parameters(rule, view, docs, parent)
        return params + docs.get('parameters', [])


class ApiSpec(FlaskApiSpec):
    def init_app(self, app):
        super(ApiSpec, self).init_app(app)
        self.resource_converter = PatchedResourceConverter(self.app, spec=self.spec)
