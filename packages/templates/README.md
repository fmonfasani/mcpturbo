# 🎨 Mcpturbo Templates

MCPTurbo - Template Engine and Collections

## 📋 Overview

Template engine, backend/frontend/devops templates

## 📦 Installation

```bash
pip install mcpturbo-templates
```

## 🚀 Quick Start

```python
# Basic usage example
from mcpturbo_templates import main_component

# Initialize component
component = main_component()

# Use component
result = await component.execute()
print(f"Result: {result}")
```

## 📝 Template Engine

The package includes a lightweight ``TemplateEngine`` class.  You can load
templates from a directory or register them programmatically.

```python
from mcpturbo_templates.engine import TemplateEngine

# Load all files inside "./templates" on creation
engine = TemplateEngine(template_dir="./templates")

# Register one template manually
engine.register_template("greet", "Hello ${name}!")

result = await engine.render_template("greet", {"name": "World"})
print(result)  # -> "Hello World!"
```

## 🔧 Configuration

```python
# Configuration example
config = {
    "setting1": "value1",
    "setting2": "value2"
}

component = main_component(**config)
```

## 📚 Documentation

- **[API Reference](https://mcpturbo.dev/docs/templates)**
- **[Examples](https://github.com/fmonfasani/mcpturbo-templates/tree/main/examples)**
- **[Contributing](https://github.com/fmonfasani/mcpturbo-templates/blob/main/CONTRIBUTING.md)**

## 🔗 Related Projects

- **[MCPTurbo Core](https://github.com/fmonfasani/mcpturbo-core)** - Core protocol
- **[MCPTurbo CLI](https://github.com/fmonfasani/mcpturbo-cli)** - Command line interface
- **[MCPTurbo Complete](https://github.com/fmonfasani/mcpturbo-complete)** - Full installation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Part of the MCPTurbo ecosystem
- Built with modern Python best practices
- Inspired by the need for intelligent agent coordination

---

<div align="center">
Made with ❤️ by the MCPTurbo Team
</div>
