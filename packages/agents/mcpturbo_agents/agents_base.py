from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Callable, List
import asyncio
import uuid
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

class AgentType(str, Enum):
    LOCAL = "local"
    EXTERNAL_API = "external_api"
    HYBRID = "hybrid"

class AgentStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"

@dataclass
class AgentCapability:
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    cost_per_request: Optional[float] = None

@dataclass
class AgentConfig:
    agent_id: str
    name: str
    agent_type: AgentType
    max_concurrent_requests: int = 5
    timeout: int = 30
    retry_attempts: int = 3
    rate_limit: int = 50  # requests per minute

class BaseAgent(ABC):
    def __init__(self, config: AgentConfig):
        self.config = config
        self.status = AgentStatus.IDLE
        self.capabilities: List[AgentCapability] = []
        self.handlers: Dict[str, Callable] = {}
        self.metadata: Dict[str, Any] = {}
        self.stats = {
            "requests_handled": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_execution_time": 0.0,
            "last_activity": None
        }
        self._semaphore = asyncio.Semaphore(config.max_concurrent_requests)
        
        self._register_core_handlers()
    
    def _register_core_handlers(self):
        self.handlers.update({
            "ping": self._handle_ping,
            "status": self._handle_status,
            "capabilities": self._handle_capabilities,
            "stats": self._handle_stats
        })
    
    @abstractmethod
    async def handle_request(self, request) -> Any:
        """Handle incoming request. Must be implemented by subclasses."""
        pass
    
    async def execute_with_semaphore(self, request) -> Any:
        """Execute request with concurrency control"""
        async with self._semaphore:
            self.status = AgentStatus.RUNNING
            start_time = datetime.utcnow()
            
            try:
                result = await self.handle_request(request)
                self._update_stats(True, start_time)
                return result
            except Exception as e:
                self._update_stats(False, start_time)
                raise e
            finally:
                self.status = AgentStatus.IDLE
    
    def _update_stats(self, success: bool, start_time: datetime):
        """Update agent statistics"""
        execution_time = (datetime.utcnow() - start_time).total_seconds()
        
        self.stats["requests_handled"] += 1
        self.stats["total_execution_time"] += execution_time
        self.stats["last_activity"] = datetime.utcnow().isoformat()
        
        if success:
            self.stats["successful_requests"] += 1
        else:
            self.stats["failed_requests"] += 1
    
    def add_capability(self, capability: AgentCapability):
        """Add a capability to this agent"""
        self.capabilities.append(capability)
        self.handlers[capability.name] = getattr(self, f"handle_{capability.name}", self._handle_unknown)
    
    def register_handler(self, action: str, handler: Callable):
        """Register custom handler for an action"""
        self.handlers[action] = handler
    
    async def _handle_ping(self, request) -> Dict[str, Any]:
        return {
            "agent_id": self.config.agent_id,
            "name": self.config.name,
            "status": self.status.value,
            "type": self.config.agent_type.value,
            "timestamp": datetime.utcnow().isoformat(),
            "pong": True
        }
    
    async def _handle_status(self, request) -> Dict[str, Any]:
        return {
            "agent_id": self.config.agent_id,
            "name": self.config.name,
            "type": self.config.agent_type.value,
            "status": self.status.value,
            "capabilities": [cap.name for cap in self.capabilities],
            "handlers": list(self.handlers.keys()),
            "metadata": self.metadata
        }
    
    async def _handle_capabilities(self, request) -> Dict[str, Any]:
        return {
            "agent_id": self.config.agent_id,
            "capabilities": [
                {
                    "name": cap.name,
                    "description": cap.description,
                    "input_schema": cap.input_schema,
                    "output_schema": cap.output_schema,
                    "cost_per_request": cap.cost_per_request
                }
                for cap in self.capabilities
            ]
        }
    
    async def _handle_stats(self, request) -> Dict[str, Any]:
        avg_execution_time = 0
        if self.stats["requests_handled"] > 0:
            avg_execution_time = self.stats["total_execution_time"] / self.stats["requests_handled"]
        
        return {
            **self.stats,
            "average_execution_time": avg_execution_time,
            "success_rate": (self.stats["successful_requests"] / max(1, self.stats["requests_handled"])) * 100
        }
    
    async def _handle_unknown(self, request) -> Dict[str, Any]:
        return {
            "error": f"Unknown action: {getattr(request, 'action', 'unknown')}",
            "available_actions": list(self.handlers.keys())
        }

class LocalAgent(BaseAgent):
    """Agent that runs locally in the same process"""
    
    def __init__(self, agent_id: str, name: str, **kwargs):
        config = AgentConfig(
            agent_id=agent_id,
            name=name,
            agent_type=AgentType.LOCAL,
            **kwargs
        )
        super().__init__(config)
    
    async def handle_request(self, request) -> Any:
        action = getattr(request, 'action', 'unknown')
        handler = self.handlers.get(action, self._handle_unknown)
        
        if asyncio.iscoroutinefunction(handler):
            return await handler(request)
        return handler(request)

class ExternalAgent(BaseAgent):
    """Agent that communicates with external API"""
    
    def __init__(self, agent_id: str, name: str, api_url: str, api_key: str = None, **kwargs):
        config = AgentConfig(
            agent_id=agent_id,
            name=name,
            agent_type=AgentType.EXTERNAL_API,
            **kwargs
        )
        super().__init__(config)
        self.api_url = api_url
        self.api_key = api_key
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
    
    async def handle_request(self, request) -> Any:
        """Handle request by calling external API"""
        from mcpturbo_core.protocol import protocol
        return await protocol._send_external_request(self, request)
    
    def build_payload(self, request) -> Dict[str, Any]:
        """Build API payload. Override in subclasses for specific APIs"""
        return {
            "action": getattr(request, 'action', ''),
            "data": getattr(request, 'data', {})
        }

class HybridAgent(BaseAgent):
    """Agent that can work both locally and with external APIs"""
    
    def __init__(self, agent_id: str, name: str, **kwargs):
        config = AgentConfig(
            agent_id=agent_id,
            name=name,
            agent_type=AgentType.HYBRID,
            **kwargs
        )
        super().__init__(config)
        self.local_handlers: Dict[str, Callable] = {}
        self.external_endpoints: Dict[str, str] = {}
    
    def register_local_handler(self, action: str, handler: Callable):
        """Register handler for local execution"""
        self.local_handlers[action] = handler
    
    def register_external_endpoint(self, action: str, endpoint: str):
        """Register endpoint for external API calls"""
        self.external_endpoints[action] = endpoint
    
    async def handle_request(self, request) -> Any:
        action = getattr(request, 'action', '')
        
        # Try local handler first
        if action in self.local_handlers:
            handler = self.local_handlers[action]
            if asyncio.iscoroutinefunction(handler):
                return await handler(request)
            return handler(request)
        
        # Fall back to external API
        if action in self.external_endpoints:
            # Use external API logic
            return await self._call_external_api(action, request)
        
        # Default handler
        return await self._handle_unknown(request)
    
    async def _call_external_api(self, action: str, request) -> Any:
        """Call external API for specific action"""
        # Implementation would depend on specific API
        raise NotImplementedError("External API call not implemented")

# Utility functions

def create_local_agent(agent_id: str, name: str = None, **kwargs) -> LocalAgent:
    """Create a simple local agent"""
    return LocalAgent(agent_id, name or agent_id.replace("_", " ").title(), **kwargs)

def create_external_agent(agent_id: str, name: str, api_url: str, api_key: str = None, **kwargs) -> ExternalAgent:
    """Create an external API agent"""
    return ExternalAgent(agent_id, name, api_url, api_key, **kwargs)