"""Template engine implementation"""

class TemplateEngine:
    """Template rendering engine for code generation"""

    def __init__(self):
        self.templates = {}

    async def render_template(self, template_name, context):
        """Render template with given context"""
        import string

        template_content = self.templates.get(template_name)
        if template_content is None:
            raise KeyError(f"Template '{template_name}' not found")

        template = string.Template(template_content)
        return template.substitute(context)
