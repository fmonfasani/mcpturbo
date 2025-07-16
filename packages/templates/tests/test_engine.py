import asyncio
from mcpturbo_templates.engine import TemplateEngine


def test_render_simple_template():
    engine = TemplateEngine()
    engine.templates["greet"] = "Hello, ${name}!"
    result = asyncio.run(engine.render_template("greet", {"name": "World"}))
    assert result == "Hello, World!"


def test_load_templates_from_directory(tmp_path):
    tpl_file = tmp_path / "welcome.txt"
    tpl_file.write_text("Welcome ${user}")

    engine = TemplateEngine(template_dir=tmp_path)
    result = asyncio.run(engine.render_template("welcome", {"user": "Alice"}))
    assert result == "Welcome Alice"


def test_register_template():
    engine = TemplateEngine()
    engine.register_template("bye", "Bye ${name}")

    result = asyncio.run(engine.render_template("bye", {"name": "Bob"}))
    assert result == "Bye Bob"
