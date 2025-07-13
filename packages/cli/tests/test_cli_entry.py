import pytest
from mcpturbo_cli.main import McpturboCli

@pytest.mark.asyncio
async def test_cli_entrypoint_runs():
    cli = McpturboCli()
    result = await cli.run()
    assert result is None
