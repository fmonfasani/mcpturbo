"""Main module for mcpturbo-cli."""


from argparse import ArgumentParser
from mcpturbo_agents import GenesisAgent, AgentConfig, AgentType, register_agent


class McpturboCli:
    """Main class for mcpturbo-cli."""

    def __init__(self) -> None:
        self.version = "1.0.0"

    async def run(self) -> None:
        """Placeholder for future async logic."""
        pass


def main(argv: list[str] | None = None) -> None:
    """Entry point for the mcpturbo CLI."""
    parser = ArgumentParser(prog="mcpturbo-cli")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("genesis", help="Register the Genesis agent")
    args = parser.parse_args(argv)

    if args.command == "genesis":
        agent = GenesisAgent(AgentConfig(agent_id="genesis", name="Genesis", agent_type=AgentType.LOCAL))
        register_agent(agent)
        print("Genesis agent registered")
    else:
        parser.print_help()


if __name__ == "__main__":  # pragma: no cover - manual execution
    main()
