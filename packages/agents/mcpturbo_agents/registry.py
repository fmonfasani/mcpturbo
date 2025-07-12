"""
Agent registry for managing and discovering agents
"""

from typing import Dict, List, Optional, Type
from datetime import datetime
from .base_agent import BaseAgent, AgentType, AgentStatus

class AgentRegistry:
    """Registry for managing agent instances and metadata"""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.agent_metadata: Dict[str, dict] = {}
        self.registered_at: Dict[str, datetime] = {}
    
    def register(self, agent: BaseAgent, **metadata):
        """Register an agent instance"""
        agent_id = agent.config.agent_id
        
        self.agents[agent_id] = agent
        self.agent_metadata[agent_id] = {
            "name": agent.config.name,
            "type": agent.config.agent_type.value,
            "capabilities": [cap.name for cap in agent.capabilities],
            "handlers": list(agent.handlers.keys()),
            **metadata
        }
        self.registered_at[agent_id] = datetime.utcnow()
    
    def unregister(self, agent_id: str) -> bool:
        """Unregister an agent"""
        if agent_id in self.agents:
            del self.agents[agent_id]
            self.agent_metadata.pop(agent_id, None)
            self.registered_at.pop(agent_id, None)
            return True
        return False
    
    def get(self, agent_id: str) -> Optional[BaseAgent]:
        """Get agent by ID"""
        return self.agents.get(agent_id)
    
    def exists(self, agent_id: str) -> bool:
        """Check if agent exists"""
        return agent_id in self.agents
    
    def list_agents(self) -> List[str]:
        """List all agent IDs"""
        return list(self.agents.keys())
    
    def list_by_type(self, agent_type: AgentType) -> List[str]:
        """List agents by type"""
        return [
            agent_id for agent_id, agent in self.agents.items()
            if agent.config.agent_type == agent_type
        ]
    
    def list_by_capability(self, capability: str) -> List[str]:
        """List agents that have a specific capability"""
        return [
            agent_id for agent_id, agent in self.agents.items()
            if any(cap.name == capability for cap in agent.capabilities)
        ]
    
    def get_agent_info(self, agent_id: str) -> Optional[dict]:
        """Get detailed agent information"""
        if agent_id not in self.agents:
            return None
        
        agent = self.agents[agent_id]
        metadata = self.agent_metadata[agent_id]
        registered_at = self.registered_at[agent_id]
        
        return {
            "id": agent_id,
            "name": agent.config.name,
            "type": agent.config.agent_type.value,
            "status": agent.status.value,
            "capabilities": [
                {
                    "name": cap.name,
                    "description": cap.description,
                    "cost_per_request": cap.cost_per_request
                }
                for cap in agent.capabilities
            ],
            "handlers": list(agent.handlers.keys()),
            "stats": agent.stats,
            "config": {
                "max_concurrent_requests": agent.config.max_concurrent_requests,
                "timeout": agent.config.timeout,
                "retry_attempts": agent.config.retry_attempts,
                "rate_limit": agent.config.rate_limit
            },
            "metadata": metadata,
            "registered_at": registered_at.isoformat()
        }
    
    def get_all_info(self) -> List[dict]:
        """Get information for all agents"""
        return [
            self.get_agent_info(agent_id)
            for agent_id in self.agents.keys()
        ]
    
    def find_agents_by_action(self, action: str) -> List[str]:
        """Find agents that can handle a specific action"""
        matching_agents = []
        
        for agent_id, agent in self.agents.items():
            if action in agent.handlers:
                matching_agents.append(agent_id)
            elif any(cap.name == action for cap in agent.capabilities):
                matching_agents.append(agent_id)
        
        return matching_agents
    
    def get_healthy_agents(self) -> List[str]:
        """Get list of healthy (non-error) agents"""
        return [
            agent_id for agent_id, agent in self.agents.items()
            if agent.status != AgentStatus.ERROR
        ]
    
    def get_available_agents(self) -> List[str]:
        """Get list of available (idle or running) agents"""
        return [
            agent_id for agent_id, agent in self.agents.items()
            if agent.status in [AgentStatus.IDLE, AgentStatus.RUNNING]
        ]
    
    def update_metadata(self, agent_id: str, **metadata):
        """Update agent metadata"""
        if agent_id in self.agent_metadata:
            self.agent_metadata[agent_id].update(metadata)
    
    def clear(self):
        """Clear all registered agents"""
        self.agents.clear()
        self.agent_metadata.clear()
        self.registered_at.clear()
    
    def count(self) -> int:
        """Get total number of registered agents"""
        return len(self.agents)
    
    def get_summary(self) -> dict:
        """Get registry summary"""
        type_counts = {}
        status_counts = {}
        
        for agent in self.agents.values():
            agent_type = agent.config.agent_type.value
            agent_status = agent.status.value
            
            type_counts[agent_type] = type_counts.get(agent_type, 0) + 1
            status_counts[agent_status] = status_counts.get(agent_status, 0) + 1
        
        return {
            "total_agents": len(self.agents),
            "by_type": type_counts,
            "by_status": status_counts,
            "capabilities": self._get_all_capabilities(),
            "oldest_registration": min(self.registered_at.values()).isoformat() if self.registered_at else None,
            "newest_registration": max(self.registered_at.values()).isoformat() if self.registered_at else None
        }
    
    def _get_all_capabilities(self) -> List[str]:
        """Get list of all unique capabilities across agents"""
        all_capabilities = set()
        
        for agent in self.agents.values():
            for capability in agent.capabilities:
                all_capabilities.add(capability.name)
        
        return sorted(list(all_capabilities))