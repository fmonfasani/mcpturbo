"""Template engine implementation.

The :class:`TemplateEngine` class provides a very small wrapper around
``string.Template``.  Templates can be registered in-memory or loaded from a
directory on disk.
"""

from pathlib import Path

class TemplateEngine:
    """Template rendering engine for code generation."""

    def __init__(self, template_dir: str | Path | None = None) -> None:
        """Create a new engine.

        Parameters
        ----------
        template_dir:
            Optional directory containing template files.  The filename without
            extension is used as the template name.  All files in the directory
            are loaded.
        """

        self.templates: dict[str, str] = {}

        if template_dir is not None:
            self.load_templates(template_dir)

    def load_templates(self, template_dir: str | Path) -> None:
        """Load template files from ``template_dir``.

        Each file in the directory is read and stored using ``Path.stem`` as the
        template name.
        """

        directory = Path(template_dir)
        if not directory.is_dir():
            raise ValueError(f"{template_dir!r} is not a directory")

        for file in directory.iterdir():
            if file.is_file():
                self.templates[file.stem] = file.read_text(encoding="utf-8")

    def register_template(self, name: str, content: str) -> None:
        """Register a template programmatically."""

        self.templates[name] = content

    async def render_template(self, template_name, context):
        """Render template with given context"""
        import string

        template_content = self.templates.get(template_name)
        if template_content is None:
            raise KeyError(f"Template '{template_name}' not found")

        template = string.Template(template_content)
        return template.substitute(context)
