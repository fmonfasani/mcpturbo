"""Main module for mcpturbo-web"""

class McpturboWeb:
    """Main class for mcpturbo-web"""
    
    def __init__(self):
        self.version = "1.0.0"
        
    async def run(self):
        """Run the Web entry point"""
        return f"{self.__class__.__name__} running (v{self.version})"
