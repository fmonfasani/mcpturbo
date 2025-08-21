# 🚀 MCPturbo - Multi-Agent Communication Protocol

**Sistema avanzado de orquestación para agentes de IA externos (OpenAI, Claude, DeepSeek)**

MCPturbo v2 es una evolución completa del protocolo de comunicación entre agentes, diseñado específicamente para orquestar agentes de IA externos como OpenAI GPT, Claude, DeepSeek y otros servicios de LLM.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Version](https://img.shields.io/badge/Version-2.0.0-green.svg)](https://github.com/fmonfasani/mcpturbo)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Novedades en v2

### 🎯 **Orquestación de IA Externa**
- **Adaptadores nativos** para OpenAI, Claude, DeepSeek
- **Circuit breakers** y **rate limiting** para APIs externas
- **Retry logic** inteligente con exponential backoff
- **Configuración centralizada** de API keys y modelos

### 🔧 **Arquitectura Mejorada**
- **Protocolo robusto** con manejo avanzado de errores
- **Agentes híbridos** (locales + externos)
- **Workflows complejos** con dependencias entre tareas
- **Monitoreo y métricas** en tiempo real

### 🚀 **Facilidad de Uso**
- **Setup automático** con variables de entorno
- **Factory functions** para crear agentes rápidamente
- **Templates de workflows** predefinidos
- **Migración automática** desde v1

## 🆕 ¿Qué cambió desde v1?

| Aspecto | v1 | v2 |
|---------|----|----|
| **Agentes soportados** | Solo locales | Locales + Externos (OpenAI, Claude, DeepSeek) |
| **Robustez** | Básica | Circuit breakers, rate limiting, retry logic |
| **Configuración** | Manual | Automática con env vars |
| **Workflows** | Simples | Complejos con dependencias |
| **Monitoreo** | Ninguno | Métricas y stats detalladas |
| **Casos de uso** | Prototipado | Producción real con LLMs |

## 📦 Instalación

```bash
# Instalación completa
pip install mcpturbo-complete

# O paquetes individuales
pip install mcpturbo-core mcpturbo-agents mcpturbo-ai mcpturbo-orchestrator
```

## ⚡ Quick Start

### 1. Configurar API Keys

```bash
export OPENAI_API_KEY="sk-..."
export CLAUDE_API_KEY="sk-ant-..."
export DEEPSEEK_API_KEY="..."
```

### 2. Código Básico

```python
import asyncio
from mcpturbo_core import quick_setup, protocol
from mcpturbo_ai import setup_all_agents
from mcpturbo_orchestrator import orchestrator

async def main():
    # Setup automático
    config = quick_setup()
    
    # Crear agentes de IA
    agents = setup_all_agents(
        openai_key=config.openai_api_key,
        claude_key=config.claude_api_key,
        deepseek_key=config.deepseek_api_key
    )
    
    # Registrar agentes con el orquestador
    for agent in agents.values():
        orchestrator.register_agent(agent)
    
    # Request directo a OpenAI
    response = await protocol.send_request(
        sender_id="user",
        target_id="openai",
        action="code_generation",
        data={
            "prompt": "Crear una función Python para calcular fibonacci",
            "language": "python"
        }
    )
    
    if response.success:
        print(f"Código generado: {response.result['code']}")
    
    # Workflow completo de generación de app
    result = await orchestrator.create_workflow_from_template(
        "app_generation",
        app_name="TaskMaster",
        app_type="web"
    )
    
    workflow_result = await orchestrator.execute_workflow(result)
    print(f"App generada: {workflow_result['status']}")

asyncio.run(main())
```

## 🛠️ Uso como librería

El protocolo y el orquestador se exponen también como clases para que puedas
crear tus propias instancias y evitar las globales `protocol` y `orchestrator`.
Esto resulta útil cuando integras MCPturbo dentro de otra aplicación.

```python
from mcpturbo_core import quick_setup, MCPProtocol
from mcpturbo_orchestrator import ProjectOrchestrator
from mcpturbo_ai import create_openai_agent

config = quick_setup()

protocol = MCPProtocol()               # instancia propia
orchestrator = ProjectOrchestrator()   # sin singleton

openai_agent = create_openai_agent(api_key=config.openai_api_key)
orchestrator.register_agent(openai_agent)

response = await protocol.send_request(
    sender_id="user",
    target_id="openai",
    action="generate_text",
    data={"prompt": "Hola mundo"}
)
```

## 🤖 Agentes Soportados

### OpenAI Agent
```python
from mcpturbo_ai import create_openai_agent

agent = create_openai_agent(
    api_key="sk-...",
    model="gpt-4"
)

# Capacidades: generate_text, code_generation
```

### Claude Agent  
```python
from mcpturbo_ai import create_claude_agent

agent = create_claude_agent(
    api_key="sk-ant-...",
    model="claude-3-sonnet-20240229"
)

# Capacidades: reasoning, analysis
```

### DeepSeek Agent
```python
from mcpturbo_ai import create_deepseek_agent

agent = create_deepseek_agent(
    api_key="...",
    model="deepseek-coder"
)

# Capacidades: fast_coding, code_optimization
```

## 🔄 Workflows Avanzados

### Template: Generación de App
```python
# Workflow que usa múltiples agentes coordinados
workflow_id = await orchestrator.create_workflow_from_template(
    "app_generation",
    app_name="MyApp",
    app_type="web",
    features=["auth", "api", "frontend"]
)

result = await orchestrator.execute_workflow(workflow_id)

# Tareas ejecutadas:
# 1. Claude diseña la arquitectura
# 2. OpenAI genera el backend  
# 3. DeepSeek genera el frontend
# 4. DeepSeek optimiza el código
```

### Template: Code Review
```python
result = await orchestrator.create_workflow_from_template(
    "code_review",
    code="def fibonacci(n): ..."
)

# Tareas ejecutadas:
# 1. Claude analiza el código
# 2. DeepSeek sugiere optimizaciones  
# 3. OpenAI revisa seguridad
```

### Workflow Personalizado
```python
from mcpturbo_orchestrator import Workflow, Task, TaskPriority

workflow = Workflow(
    id="custom_analysis",
    name="Análisis de Competencia",
    tasks=[
        Task(
            id="research",
            agent_id="claude",
            action="reasoning",
            data={"prompt": "Analiza el mercado de apps de productividad"},
            priority=TaskPriority.HIGH
        ),
        Task(
            id="features",
            agent_id="openai", 
            action="generate_text",
            data={"prompt": "Sugiere características únicas"},
            dependencies=["research"],
            priority=TaskPriority.NORMAL
        ),
        Task(
            id="tech_specs",
            agent_id="deepseek",
            action="fast_coding", 
            data={"prompt": "Especificaciones técnicas"},
            dependencies=["features"],
            priority=TaskPriority.NORMAL
        )
    ]
)

orchestrator.workflows[workflow.id] = workflow
result = await orchestrator.execute_workflow(workflow.id)
```

## 🛡️ Características Avanzadas

### Circuit Breakers
```python
# Protección automática contra servicios caídos
# Si OpenAI falla 5 veces seguidas, se abre el circuit breaker
orchestrator.register_agent(openai_agent, failure_threshold=5, recovery_timeout=60)

# El circuit breaker se recupera automáticamente después del timeout
stats = protocol.get_stats()
print(f"Circuit Breaker OpenAI: {stats['circuit_breakers']['openai']['state']}")
```

### Rate Limiting
```python
# Control automático de límites por API
orchestrator.register_agent(claude_agent, rate_limit=50)  # 50 req/min
orchestrator.register_agent(openai_agent, rate_limit=60)  # 60 req/min

# Si se excede el límite, se espera automáticamente
```

### Retry Logic
```python
from mcpturbo_core.protocol import RetryConfig

# Configuración personalizada de reintentos
retry_config = RetryConfig(
    max_attempts=5,
    initial_delay=1.0,
    max_delay=30.0,
    exponential_base=2.0
)

response = await protocol.send_request(
    sender_id="user",
    target_id="openai",
    action="generate_text",
    data={"prompt": "Hello"},
    retry_config=retry_config
)
```

### Monitoreo en Tiempo Real
```python
# Obtener estadísticas detalladas
stats = protocol.get_stats()
print(f"Agentes activos: {stats['agents']}")
print(f"Requests enviadas: {stats['messages_sent']}")

# Estadísticas por agente
for agent_id in ["openai", "claude", "deepseek"]:
    agent_stats = await protocol.send_request("monitor", agent_id, "stats")
    print(f"{agent_id}: {agent_stats.result['success_rate']:.1f}% éxito")
```

## 🔧 Configuración Avanzada

### Variables de Entorno
```bash
# API Keys (requerido)
export OPENAI_API_KEY="sk-..."
export CLAUDE_API_KEY="sk-ant-..."
export DEEPSEEK_API_KEY="..."

# Configuración opcional
export MCP_DEBUG="true"
export MCP_LOG_LEVEL="INFO"
export MCP_CACHE_DIR="~/.mcpturbo/cache"
export MCP_CONFIG_DIR="~/.mcpturbo"
```

### Archivo de Configuración
```python
from mcpturbo_core import get_config, save_config

config = get_config()

# Personalizar configuración de agentes
config.agents["openai"].rate_limit = 100
config.agents["claude"].timeout = 120
config.max_concurrent_requests = 20

# Guardar configuración
save_config()
```

### Configuración por Código
```python
from mcpturbo_core.config import MCPConfig, AgentConfig

config = MCPConfig(
    max_concurrent_requests=15,
    default_timeout=45,
    debug=True
)

# Configurar agente específico
config.add_agent_config("openai", AgentConfig(
    api_key="sk-...",
    model="gpt-4-turbo",
    rate_limit=120,
    timeout=90,
    custom_settings={
        "temperature": 0.5,
        "max_tokens": 3000
    }
))
```

## 🧪 Testing

### Tests Unitarios
Antes de ejecutar los tests, instala las dependencias de desarrollo:
```bash
pip install -e .[dev]
```
Estas extras incluyen librerías como `aiohttp` utilizadas en las pruebas.
```bash
# Ejecutar todos los tests
pytest packages/*/tests/

# Tests específicos
pytest packages/core/tests/test_protocol_v2.py -v

# Con cobertura
pytest --cov=mcpturbo_core --cov-report=html
```

### Tests de Integración
```python
import pytest
from mcpturbo_core import protocol
from mcpturbo_ai import create_openai_agent

@pytest.mark.integration
async def test_openai_integration():
    # Requiere OPENAI_API_KEY en environment
    agent = create_openai_agent(api_key=os.getenv("OPENAI_API_KEY"))
    protocol.register_agent("openai", agent)
    
    response = await protocol.send_request(
        sender_id="test",
        target_id="openai", 
        action="generate_text",
        data={"prompt": "Hello, world!"}
    )
    
    assert response.success
    assert "text" in response.result
```

## 🔄 Migración desde v1

### Script Automático
```bash
# Migrar archivos automáticamente
python scripts/migrate_to_v2.py /path/to/your/project --recursive

# Dry run para ver cambios
python scripts/migrate_to_v2.py /path/to/your/project --dry-run

# Generar reporte
python scripts/migrate_to_v2.py /path/to/your/project --report migration_report.txt
```

### Cambios Principales
| v1 | v2 |
|----|----| 
| `from mcpturbo_core import protocol` | `from mcpturbo_core.protocol import protocol` |
| `MCPProtocol()` | `protocol` (instancia global) |
| `SimpleAgent()` | `LocalAgent()` |
| `send_message()` | `send_request()` |
| `MCPMessage` | `Request/Response/Event` |

### Migración Manual
```python
# ANTES (v1)
from mcpturbo_core import MCPProtocol, SimpleAgent

protocol = MCPProtocol()
agent = SimpleAgent("test", "Test Agent")
protocol.register_agent("test", agent)

response = protocol.send_message("user", "test", "action")

# DESPUÉS (v2)
from mcpturbo_core.protocol import protocol
from mcpturbo_agents.base_agent import LocalAgent

agent = LocalAgent("test", "Test Agent")
protocol.register_agent("test", agent)

response = await protocol.send_request(
    sender_id="user",
    target_id="test",
    action="action"
)
```


## 🚀 Genesis Engine Migration

El nuevo comando `genesis init` automatiza la creación de la estructura base para proyectos MCPturbo. Ejecuta este comando en un directorio vacío y se generarán los archivos de configuración junto con un `docker-compose.yml` listo para usar.

### Variables de entorno requeridas


```bash
export OPENAI_API_KEY="sk-..."
export CLAUDE_API_KEY="sk-ant-..."
export DEEPSEEK_API_KEY="..."

export MCP_DEBUG="true"
export MCP_LOG_LEVEL="INFO"
export MCP_CACHE_DIR="~/.mcpturbo/cache"
export MCP_CONFIG_DIR="~/.mcpturbo"
```

### Ejemplo de uso

```bash
# Crear un nuevo proyecto
genesis init my-mcp-app
cd my-mcp-app

# Construir y ejecutar los contenedores
docker compose build
docker compose up

```

### Generar reportes de migración y validación

Una vez copiados los recursos de Genesis puedes producir los reportes ejecutando:

```bash
python tools/migrate_genesis.py /ruta/a/genesis
python tools/validate_migration.py
```

Esto actualizará **MIGRATION_REPORT.md** y **VALIDATION_REPORT.md** con los
resultados de la copia y una validación básica de los paquetes.

## 🎯 Casos de Uso Reales

### 1. Generación de Documentación
```python
async def generate_documentation(code: str):
    # Claude analiza el código
    analysis = await protocol.send_request(
        sender_id="user",
        target_id="claude",
        action="analysis",
        data={"content": code, "analysis_type": "documentation"}
    )
    
    # OpenAI genera documentación
    docs = await protocol.send_request(
        sender_id="user", 
        target_id="openai",
        action="generate_text",
        data={
            "prompt": f"Generate documentation for: {analysis.result['analysis']}",
            "system_prompt": "You are a technical writer"
        }
    )
    
    return docs.result["text"]
```

### 2. Code Review Automatizado
```python
async def automated_code_review(pull_request_code: str):
    workflow_id = await orchestrator.create_workflow_from_template(
        "code_review",
        code=pull_request_code
    )
    
    result = await orchestrator.execute_workflow(workflow_id)
    
    return {
        "analysis": result["tasks"][0]["result"]["analysis"],
        "suggestions": result["tasks"][1]["result"]["improvements"],
        "security": result["tasks"][2]["result"]["text"]
    }
```

### 3. Asistente de Desarrollo
```python
class DevAssistant:
    def __init__(self):
        self.agents = setup_all_agents()
        
    async def help_with_feature(self, description: str):
        # Usar Claude para arquitectura
        architecture = await protocol.send_request(
            sender_id="dev",
            target_id="claude",
            action="reasoning",
            data={"prompt": f"Design architecture for: {description}"}
        )
        
        # Usar DeepSeek para código rápido
        code = await protocol.send_request(
            sender_id="dev",
            target_id="deepseek", 
            action="fast_coding",
            data={"prompt": f"Implement: {architecture.result['reasoning']}"}
        )
        
        return {
            "architecture": architecture.result,
            "implementation": code.result
        }
```

## 📊 Performance y Escalabilidad

### Métricas de Performance
- **Throughput**: 100+ requests/segundo por agente
- **Latencia**: < 100ms overhead del protocolo
- **Concurrencia**: Hasta 50 requests simultáneas
- **Circuit Breaker**: Recuperación en < 60 segundos
- **Rate Limiting**: Control granular por agente

### Optimizaciones
```python
# Configuración para alta performance
config = MCPConfig(
    max_concurrent_requests=50,
    default_timeout=30,
    queue_size=2000
)

# Configurar agentes para máximo rendimiento
for agent_id in ["openai", "claude", "deepseek"]:
    agent_config = config.get_agent_config(agent_id)
    agent_config.rate_limit = 200  # Aumentar límite
    agent_config.timeout = 60      # Timeout generoso
```

## 🤝 Contribuir

### Setup de Desarrollo
```bash
# Clonar repositorio
git clone https://github.com/fmonfasani/mcpturbo.git
cd mcpturbo

# Instalar dependencias y hooks
make setup

# Lint de todo el código
make lint

# Ejecutar tests
make test

# Benchmarks opcionales
make bench
```

Si usas VSCode, este repositorio incluye configuración de [Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers) en `.devcontainer/devcontainer.json` para proporcionar un entorno con Python 3.11 y las dependencias de desarrollo preinstaladas.

### Guidelines
1. **Código**: Seguir PEP 8, usar Black y isort
2. **Tests**: Cobertura mínima 80%
3. **Documentación**: Docstrings en todas las funciones públicas
4. **Commits**: Conventional commits (feat:, fix:, docs:)

### Crear Nuevos Adaptadores
```python
from mcpturbo_agents.base_agent import ExternalAgent

class CustomLLMAgent(ExternalAgent):
    def __init__(self, api_key: str):
        super().__init__(
            agent_id="custom_llm",
            name="Custom LLM",
            api_url="https://api.custom-llm.com/v1/chat",
            api_key=api_key
        )
    
    def build_payload(self, request):
        return {
            "messages": [{"role": "user", "content": request.data["prompt"]}],
            "model": "custom-model"
        }
```

## 🔗 Ecosistema MCPturbo

### Paquetes Relacionados
- **mcpturbo-core**: Protocolo y configuración base
- **mcpturbo-agents**: Clases base para agentes
- **mcpturbo-ai**: Adaptadores para LLMs (OpenAI, Claude, DeepSeek)
- **mcpturbo-orchestrator**: Orquestación y workflows
- **mcpturbo-cli**: Interfaz de línea de comandos
- **mcpturbo-web**: Dashboard web (próximamente)
- **mcpturbo-cloud**: Despliegue en cloud (próximamente)

### Integraciones
- **Langchain**: Compatible con agentes MCPturbo
- **AutoGen**: Uso de MCPturbo como backend
- **CrewAI**: Orquestación avanzada con MCPturbo

## 📚 Documentación

- **[Guía de Instalación](https://mcpturbo.dev/docs/installation)**
- **[Tutorial Completo](https://mcpturbo.dev/docs/tutorial)**
- **[API Reference](https://mcpturbo.dev/docs/api)**
- **[Ejemplos](https://github.com/fmonfasani/mcpturbo/tree/main/examples)**
- **[Guía de Migración](https://mcpturbo.dev/docs/migration)**

## 🐛 Soporte

- **[GitHub Issues](https://github.com/fmonfasani/mcpturbo/issues)**
- **[Discussions](https://github.com/fmonfasani/mcpturbo/discussions)**
- **[Discord](https://discord.gg/mcpturbo)** (próximamente)

## 📄 Licencia

MCPturbo v2 está licenciado bajo la [Licencia MIT](LICENSE).

## 🙏 Agradecimientos

MCPturbo v2 está construido sobre tecnologías increíbles:

- **[aiohttp](https://aiohttp.readthedocs.io/)** - Cliente HTTP asíncrono
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** - Validación de datos
- **[pytest](https://pytest.org/)** - Framework de testing
- **[OpenAI](https://openai.com/)**, **[Anthropic](https://anthropic.com/)**, **[DeepSeek](https://deepseek.com/)** - APIs de IA

---

<div align="center">

**[🏠 Página Principal](https://mcpturbo.dev)** •
**[📖 Documentación](https://docs.mcpturbo.dev)** •
**[🚀 Ejemplos](https://github.com/fmonfasani/mcpturbo/tree/main/examples)**

Creado con ❤️ por [Federico Monfasani](https://github.com/fmonfasani)

**⭐ Si MCPturbo te ayuda, considera darle una estrella en GitHub**

</div>