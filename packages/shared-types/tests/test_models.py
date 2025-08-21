from pathlib import Path

from mcpturbo_shared_types import Message, Task, Workflow


def test_serialization_roundtrip():
    msg = Message(role="user", content="hi")
    task = Task(messages=[msg])
    wf = Workflow(tasks=[task])

    data = wf.to_dict()
    assert data["tasks"][0]["messages"][0]["content"] == "hi"


def test_type_declaration_files_exist():
    types_dir = Path(__file__).resolve().parent.parent / "types"
    assert (types_dir / "message.d.ts").exists()
    assert (types_dir / "workflow.d.ts").exists()
