from typing import Dict, Any, Optional, List
import aiohttp
import json
from mcpturbo_agents import ExternalAgent, AgentCapability, AgentConfig, AgentType
from mcpturbo_core.exceptions import APIError, AuthenticationError, RateLimitError

class OpenAIAgent(ExternalAgent):
    """Agent adapter for OpenAI API"""
    
    def __init__(self, agent_id: str = "openai", api_key: str = None, model: str = "gpt-4", **kwargs):
        super().__init__(
            agent_id=agent_id,
            name="OpenAI GPT",
            api_url="https://api.openai.com/v1/chat/completions",
            api_key=api_key,
            **kwargs
        )
        self.model = model
        self.headers.update({
            "OpenAI-Beta": "assistants=v1"
        })
        
        # Add capabilities
        self.add_capability(AgentCapability(
            name="generate_text",
            description="Generate text using OpenAI models",
            input_schema={
                "prompt": {"type": "string", "required": True},
                "max_tokens": {"type": "integer", "default": 1000},
                "temperature": {"type": "number", "default": 0.7}
            },
            output_schema={
                "text": {"type": "string"},
                "tokens_used": {"type": "integer"},
                "model": {"type": "string"}
            },
            cost_per_request=0.03
        ))
        
        self.add_capability(AgentCapability(
            name="code_generation",
            description="Generate code with OpenAI",
            input_schema={
                "prompt": {"type": "string", "required": True},
                "language": {"type": "string", "default": "python"}
            },
            output_schema={
                "code": {"type": "string"},
                "explanation": {"type": "string"}
            },
            cost_per_request=0.05
        ))
    
    def build_payload(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        action = getattr(request, 'action', '')
        
        messages = []
        
        # System prompt if provided
        if 'system_prompt' in data:
            messages.append({
                "role": "system",
                "content": data['system_prompt']
            })
        
        # Main prompt
        prompt = data.get('prompt', '')
        if action == 'code_generation':
            language = data.get('language', 'python')
            prompt = f"Generate {language} code for: {prompt}"
        
        messages.append({
            "role": "user", 
            "content": prompt
        })
        
        return {
            "model": data.get('model', self.model),
            "messages": messages,
            "max_tokens": data.get('max_tokens', 1000),
            "temperature": data.get('temperature', 0.7),
            "stream": False
        }
    
    async def handle_request(self, request) -> Any:
        try:
            response_data = await super().handle_request(request)
            return self._parse_openai_response(response_data, request)
        except Exception as e:
            if "401" in str(e):
                raise AuthenticationError("Invalid OpenAI API key")
            elif "429" in str(e):
                raise RateLimitError("OpenAI rate limit exceeded")
            raise APIError(f"OpenAI API error: {str(e)}", provider="openai")
    
    def _parse_openai_response(self, response: Dict[str, Any], request) -> Dict[str, Any]:
        choice = response.get('choices', [{}])[0]
        message = choice.get('message', {})
        content = message.get('content', '')
        
        usage = response.get('usage', {})
        
        result = {
            "text": content,
            "tokens_used": usage.get('total_tokens', 0),
            "model": response.get('model', self.model)
        }
        
        # Parse code if it's a code generation request
        action = getattr(request, 'action', '')
        if action == 'code_generation':
            code_blocks = self._extract_code_blocks(content)
            result.update({
                "code": code_blocks[0] if code_blocks else content,
                "explanation": content
            })
        
        return result
    
    def _extract_code_blocks(self, text: str) -> List[str]:
        """Extract code blocks from markdown text"""
        import re
        pattern = r'```(?:\w+\n)?(.*?)```'
        return re.findall(pattern, text, re.DOTALL)

class ClaudeAgent(ExternalAgent):
    """Agent adapter for Anthropic Claude API"""
    
    def __init__(self, agent_id: str = "claude", api_key: str = None, model: str = "claude-3-sonnet-20240229", **kwargs):
        super().__init__(
            agent_id=agent_id,
            name="Anthropic Claude",
            api_url="https://api.anthropic.com/v1/messages",
            api_key=api_key,
            **kwargs
        )
        self.model = model
        self.headers.update({
            "anthropic-version": "2023-06-01",
            "x-api-key": api_key
        })
        
        # Remove Authorization header as Claude uses x-api-key
        if "Authorization" in self.headers:
            del self.headers["Authorization"]
        
        self.add_capability(AgentCapability(
            name="reasoning",
            description="Advanced reasoning with Claude",
            input_schema={
                "prompt": {"type": "string", "required": True},
                "max_tokens": {"type": "integer", "default": 1000}
            },
            output_schema={
                "reasoning": {"type": "string"},
                "conclusion": {"type": "string"}
            },
            cost_per_request=0.04
        ))
        
        self.add_capability(AgentCapability(
            name="analysis",
            description="Deep analysis and critique",
            input_schema={
                "content": {"type": "string", "required": True},
                "analysis_type": {"type": "string", "default": "general"}
            },
            output_schema={
                "analysis": {"type": "string"},
                "insights": {"type": "array"}
            },
            cost_per_request=0.06
        ))
    
    def build_payload(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        
        messages = []
        
        # Claude expects messages format
        prompt = data.get('prompt', data.get('content', ''))
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        payload = {
            "model": data.get('model', self.model),
            "max_tokens": data.get('max_tokens', 1000),
            "messages": messages
        }
        
        # Add system prompt if provided
        if 'system_prompt' in data:
            payload["system"] = data['system_prompt']
        
        return payload
    
    async def handle_request(self, request) -> Any:
        try:
            response_data = await super().handle_request(request)
            return self._parse_claude_response(response_data, request)
        except Exception as e:
            if "401" in str(e):
                raise AuthenticationError("Invalid Claude API key")
            elif "429" in str(e):
                raise RateLimitError("Claude rate limit exceeded")
            raise APIError(f"Claude API error: {str(e)}", provider="claude")
    
    def _parse_claude_response(self, response: Dict[str, Any], request) -> Dict[str, Any]:
        content = response.get('content', [])
        text = content[0].get('text', '') if content else ''
        
        usage = response.get('usage', {})
        
        result = {
            "text": text,
            "tokens_used": usage.get('output_tokens', 0),
            "model": response.get('model', self.model)
        }
        
        action = getattr(request, 'action', '')
        if action == 'reasoning':
            parts = text.split('\n\n')
            result.update({
                "reasoning": text,
                "conclusion": parts[-1] if len(parts) > 1 else text
            })
        elif action == 'analysis':
            result.update({
                "analysis": text,
                "insights": self._extract_insights(text)
            })
        
        return result
    
    def _extract_insights(self, text: str) -> List[str]:
        """Extract key insights from analysis"""
        lines = text.split('\n')
        insights = []
        for line in lines:
            if line.startswith('- ') or line.startswith('• '):
                insights.append(line[2:].strip())
        return insights

class DeepSeekAgent(ExternalAgent):
    """Agent adapter for DeepSeek API"""
    
    def __init__(self, agent_id: str = "deepseek", api_key: str = None, model: str = "deepseek-coder", **kwargs):
        super().__init__(
            agent_id=agent_id,
            name="DeepSeek Coder",
            api_url="https://api.deepseek.com/v1/chat/completions",
            api_key=api_key,
            **kwargs
        )
        self.model = model
        
        self.add_capability(AgentCapability(
            name="fast_coding",
            description="Fast code generation with DeepSeek",
            input_schema={
                "prompt": {"type": "string", "required": True},
                "language": {"type": "string", "default": "python"}
            },
            output_schema={
                "code": {"type": "string"},
                "optimized": {"type": "boolean"}
            },
            cost_per_request=0.01
        ))
        
        self.add_capability(AgentCapability(
            name="code_optimization",
            description="Optimize existing code",
            input_schema={
                "code": {"type": "string", "required": True},
                "optimization_type": {"type": "string", "default": "performance"}
            },
            output_schema={
                "optimized_code": {"type": "string"},
                "improvements": {"type": "array"}
            },
            cost_per_request=0.02
        ))
    
    def build_payload(self, request) -> Dict[str, Any]:
        data = getattr(request, 'data', {})
        action = getattr(request, 'action', '')
        
        messages = []
        
        prompt = data.get('prompt', '')
        if action == 'fast_coding':
            language = data.get('language', 'python')
            prompt = f"Write efficient {language} code for: {prompt}\nProvide only the code without explanation."
        elif action == 'code_optimization':
            code = data.get('code', '')
            opt_type = data.get('optimization_type', 'performance')
            prompt = f"Optimize this code for {opt_type}:\n\n{code}"
        
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        return {
            "model": data.get('model', self.model),
            "messages": messages,
            "max_tokens": data.get('max_tokens', 2000),
            "temperature": data.get('temperature', 0.1),  # Lower for code
            "stream": False
        }
    
    async def handle_request(self, request) -> Any:
        try:
            response_data = await super().handle_request(request)
            return self._parse_deepseek_response(response_data, request)
        except Exception as e:
            if "401" in str(e):
                raise AuthenticationError("Invalid DeepSeek API key")
            elif "429" in str(e):
                raise RateLimitError("DeepSeek rate limit exceeded")
            raise APIError(f"DeepSeek API error: {str(e)}", provider="deepseek")
    
    def _parse_deepseek_response(self, response: Dict[str, Any], request) -> Dict[str, Any]:
        choice = response.get('choices', [{}])[0]
        message = choice.get('message', {})
        content = message.get('content', '')
        
        usage = response.get('usage', {})
        
        result = {
            "text": content,
            "tokens_used": usage.get('total_tokens', 0),
            "model": response.get('model', self.model)
        }
        
        action = getattr(request, 'action', '')
        if action == 'fast_coding':
            code = self._extract_code_blocks(content)
            result.update({
                "code": code[0] if code else content,
                "optimized": True
            })
        elif action == 'code_optimization':
            code = self._extract_code_blocks(content)
            result.update({
                "optimized_code": code[0] if code else content,
                "improvements": self._extract_improvements(content)
            })
        
        return result
    
    def _extract_code_blocks(self, text: str) -> List[str]:
        """Extract code blocks from markdown text"""
        import re
        pattern = r'```(?:\w+\n)?(.*?)```'
        return re.findall(pattern, text, re.DOTALL)
    
    def _extract_improvements(self, text: str) -> List[str]:
        """Extract improvement descriptions"""
        improvements = []
        lines = text.split('\n')
        for line in lines:
            if 'improved' in line.lower() or 'optimized' in line.lower():
                improvements.append(line.strip())
        return improvements

# Factory functions to create agents easily

def create_openai_agent(api_key: str, model: str = "gpt-4", **kwargs) -> OpenAIAgent:
    """Create OpenAI agent with API key"""
    return OpenAIAgent(api_key=api_key, model=model, **kwargs)

def create_claude_agent(api_key: str, model: str = "claude-3-sonnet-20240229", **kwargs) -> ClaudeAgent:
    """Create Claude agent with API key"""
    return ClaudeAgent(api_key=api_key, model=model, **kwargs)

def create_deepseek_agent(api_key: str, model: str = "deepseek-coder", **kwargs) -> DeepSeekAgent:
    """Create DeepSeek agent with API key"""
    return DeepSeekAgent(api_key=api_key, model=model, **kwargs)

def create_multi_llm_setup(openai_key: str = None, claude_key: str = None, deepseek_key: str = None) -> Dict[str, ExternalAgent]:
    """Create multiple LLM agents at once"""
    agents = {}
    
    if openai_key:
        agents["openai"] = create_openai_agent(openai_key)
    
    if claude_key:
        agents["claude"] = create_claude_agent(claude_key)
    
    if deepseek_key:
        agents["deepseek"] = create_deepseek_agent(deepseek_key)
    
    return agents