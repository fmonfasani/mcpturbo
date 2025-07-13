import asyncio
from mcpturbo_templates.engine import TemplateEngine


def test_render_simple_template():
    engine = TemplateEngine()
    engine.templates["greet"] = "Hello, ${name}!"
    result = asyncio.run(engine.render_template("greet", {"name": "World"}))
    assert result == "Hello, World!"
