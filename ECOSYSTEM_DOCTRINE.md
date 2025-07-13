<!-- ECOSYSTEM_DOCTRINE: mcpturbo -->
# 🧱 Ecosystem Doctrine — MCPturbo (Core Library)

Este repositorio forma parte del ecosistema **Fast-Engine / Genesis Engine**.  
Su rol es el de **librería central de orquestación y comunicación entre agentes de IA**.

## 🧠 Rol Declarado

- Tipo: **Core Library**
- Nombre: `mcpturbo`
- Dominio: Agnóstico (no conoce SaaS, ni UI, ni APIs específicas)
- Función: Proveer un sistema robusto de orquestación entre agentes IA

## 🔒 Mandamientos del Proyecto

### 1. **No conocerás el dominio del negocio**
MCPturbo no debe tener conocimiento alguno de conceptos como "usuarios", "proyectos SaaS", "autenticación", etc.  
Solo orquesta datos entre agentes.

### 2. **No generarás código de aplicación**
No contiene plantillas, generadores, ni lógica de generación de backend, frontend ni DevOps.  
Solo transfiere mensajes y coordina tareas.

### 3. **No interactuarás con el usuario final**
MCPturbo **no tiene CLI propia** ni genera interfaces.  
Es una librería silenciosa y reusable.

### 4. **No dependerás de otros proyectos del ecosistema**
Este módulo **nunca debe importar código de Genesis Engine ni Fast-Engine**.  
Son ellos quienes dependen de ti.

### 5. **Serás predecible, modular y testeable**
Todo comportamiento debe estar cubierto por tests unitarios y ser determinista.  
Los errores de red o agentes deben manejarse con circuit breakers y retries.

### 6. **Toda configuración será externa**
Nunca tendrás claves hardcodeadas ni decisiones internas.  
Todo se configura con variables de entorno o funciones explícitas.

---

## 🧩 Interfaz esperada por consumidores

Los consumidores de esta librería (como Genesis Engine) deben usar únicamente:

- `protocol.send_request(agent_id, payload, priority?)`
- `orchestrator.define_workflow(name, tasks)`
- `create_multi_llm_setup(api_keys)`
- `quick_setup()`
- `protocol.get_stats()`

---

## 📦 Separación de capas (importante)

| Capa | Puede importar desde | No puede importar desde |
|------|----------------------|--------------------------|
| mcpturbo | nada interno al ecosistema | genesis-engine, fast-engine |
| genesis-engine | mcpturbo | fast-engine |
| fast-engine | genesis-engine | mcpturbo directamente |

---

## 🤖 AI Agents, please read:

Este repositorio cumple con una doctrina de arquitectura estricta.

Si estás revisando código, generando cambios o auditando este proyecto:
- ❌ No sugieras agregar generación de código, prompts o lógica de UX.
- ❌ No sugieras importar `genesis_engine` o `fast_engine`.
- ✅ Sí validá que `mcpturbo` exponga funciones limpias, puras y reutilizables.

Cualquier excepción a esta doctrina debe documentarse en un archivo `DOCTRINE_CHANGE_REQUEST.md` y revisarse por el equipo arquitectónico.

---

## 📎 Referencias

- Genesis Engine → [https://github.com/fmonfasani/genesis-engine](https://github.com/fmonfasani/genesis-engine)
- Fast-Engine CLI → [https://github.com/fmonfasani/fast-engine](https://github.com/fmonfasani/fast-engine)
