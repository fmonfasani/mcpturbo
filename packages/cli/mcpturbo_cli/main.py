"""Main module for mcpturbo-cli"""

class McpturboCli:
    """Main class for mcpturbo-cli"""
    
    def __init__(self):
        self.version = "1.0.0"
        
    async def run(self):
        """Run the CLI entry point"""
        return f"{self.__class__.__name__} running (v{self.version})"
