import pytest
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
async def test_genesis_init_e2e():
    import mcpturbo_cli.genesis_integration as gi

    with patch("mcpturbo_cli.genesis_integration.genesis_setup", AsyncMock(return_value={})), \
         patch.object(gi.orchestrator, "create_workflow_from_template", AsyncMock(return_value="wf1"), create=True) as mock_template, \
         patch.object(gi.orchestrator, "execute_workflow", AsyncMock(return_value={"status": "ok"})) as mock_exec:
        result = await gi.genesis_init("proj")
        assert result == {"status": "ok"}
        mock_template.assert_called_once()
        mock_exec.assert_called_once_with("wf1")
