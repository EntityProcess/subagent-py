"""Tests for code-insiders command support."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from subagent.cli import main


def test_code_insiders_command_available() -> None:
    """Test that code-insiders command is available."""
    with pytest.raises(SystemExit) as exc_info:
        main(["code-insiders"])
    # Should exit with code 2 (argparse error) because no action is provided
    assert exc_info.value.code == 2


def test_code_insiders_provision_help() -> None:
    """Test that code-insiders provision help works."""
    with pytest.raises(SystemExit) as exc_info:
        main(["code-insiders", "provision", "--help"])
    # Help should exit with code 0
    assert exc_info.value.code == 0


def test_code_insiders_chat_help() -> None:
    """Test that code-insiders chat help works."""
    with pytest.raises(SystemExit) as exc_info:
        main(["code-insiders", "chat", "--help"])
    # Help should exit with code 0
    assert exc_info.value.code == 0


def test_code_insiders_warmup_help() -> None:
    """Test that code-insiders warmup help works."""
    with pytest.raises(SystemExit) as exc_info:
        main(["code-insiders", "warmup", "--help"])
    # Help should exit with code 0
    assert exc_info.value.code == 0


def test_code_insiders_list_help() -> None:
    """Test that code-insiders list help works."""
    with pytest.raises(SystemExit) as exc_info:
        main(["code-insiders", "list", "--help"])
    # Help should exit with code 0
    assert exc_info.value.code == 0


def test_code_insiders_unlock_help() -> None:
    """Test that code-insiders unlock help works."""
    with pytest.raises(SystemExit) as exc_info:
        main(["code-insiders", "unlock", "--help"])
    # Help should exit with code 0
    assert exc_info.value.code == 0


@patch("subagent.vscode.cli.warmup_subagents")
@patch("subagent.vscode.cli.get_subagent_root")
def test_code_insiders_warmup_passes_correct_vscode_cmd(
    mock_get_root: MagicMock,
    mock_warmup: MagicMock,
    tmp_path,
) -> None:
    """Test that code-insiders warmup passes vscode_cmd='code-insiders'."""
    mock_get_root.return_value = tmp_path / "agents"
    mock_warmup.return_value = 0
    
    # Create a dummy subagent directory
    root = tmp_path / "agents"
    root.mkdir()
    subagent = root / "subagent-1"
    subagent.mkdir()
    (subagent / "subagent-1.code-workspace").write_text('{"folders": []}')
    
    result = main(["code-insiders", "warmup", "--subagents", "1", "--target-root", str(root)])
    
    # Verify warmup was called with vscode_cmd='code-insiders'
    mock_warmup.assert_called_once()
    call_kwargs = mock_warmup.call_args.kwargs
    assert call_kwargs["vscode_cmd"] == "code-insiders"
    assert result == 0


@patch("subagent.vscode.cli.warmup_subagents")
@patch("subagent.vscode.cli.get_subagent_root")
def test_code_warmup_passes_correct_vscode_cmd(
    mock_get_root: MagicMock,
    mock_warmup: MagicMock,
    tmp_path,
) -> None:
    """Test that code warmup passes vscode_cmd='code' (default)."""
    mock_get_root.return_value = tmp_path / "agents"
    mock_warmup.return_value = 0
    
    # Create a dummy subagent directory
    root = tmp_path / "agents"
    root.mkdir()
    subagent = root / "subagent-1"
    subagent.mkdir()
    (subagent / "subagent-1.code-workspace").write_text('{"folders": []}')
    
    result = main(["code", "warmup", "--subagents", "1", "--target-root", str(root)])
    
    # Verify warmup was called with vscode_cmd='code'
    mock_warmup.assert_called_once()
    call_kwargs = mock_warmup.call_args.kwargs
    assert call_kwargs["vscode_cmd"] == "code"
    assert result == 0
