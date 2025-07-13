"""Tests for genesis integration helpers."""

import inspect

import pytest


@pytest.mark.asyncio
async def test_genesis_helpers_exist():
    import mcpturbo_cli.genesis_integration as gi

    assert hasattr(gi, "genesis_init")
    assert hasattr(gi, "genesis_setup")
    assert inspect.iscoroutinefunction(gi.genesis_init)
    assert inspect.iscoroutinefunction(gi.genesis_setup)
