"""Tests targeting surviving mutants in yooxnas.py.

Covers _handle_standalone_hex_data, _handle_raw_hex_data_block,
_handle_raw_addressing_rune_op, and main.
"""

import logging
from unittest.mock import patch

import pytest

from yooxn.yooxnas import (
    IRLabelPlaceholder,
    IRRawBytes,
    Lexer,
    Parser,
    SyntaxError,
    main,
)


def parse_source(source: str) -> Parser:
    lexer = Lexer(source)
    tokens = lexer.scan_all_tokens()
    parser = Parser(tokens)
    parser.parse_pass1()
    return parser


# ---------------------------------------------------------------------------
# _handle_standalone_hex_data
# ---------------------------------------------------------------------------


# _handle_standalone_hex_data is only reachable via a `{ ... }` block;
# top-level hex literals are handled by _handle_identifier_token.


def test_standalone_hex_single_byte_value():
    """Kill `data_token is None` flip, `data_len == 0` flip, `data_size == 1`
    flip, and `<= -> <` / `<= -> >` mutants on line 1858."""
    parser = parse_source("{ 01 }")
    raw = [n for n in parser.ir_stream if isinstance(n, IRRawBytes)]
    assert len(raw) == 1
    assert raw[0].size == 1
    assert raw[0].byte_values == [0x01]


def test_standalone_hex_two_byte_value():
    """Kill `data_size == 2` flip, and `<= -> <` / `<= -> >` mutants on
    line 1860."""
    parser = parse_source("{ 0123 }")
    raw = [n for n in parser.ir_stream if isinstance(n, IRRawBytes)]
    assert len(raw) == 1
    assert raw[0].size == 2
    assert raw[0].byte_values == [0x01, 0x23]


def test_standalone_hex_three_chars_is_two_bytes():
    """Kill `<= -> <` on line 1860: with `<` instead of `<=`, len==3 would
    skip the size-2 branch and fall through. Original keeps size 2."""
    parser = parse_source("{ 123 }")
    raw = [n for n in parser.ir_stream if isinstance(n, IRRawBytes)]
    assert len(raw) == 1
    assert raw[0].size == 2
    assert raw[0].byte_values == [0x01, 0x23]


def test_standalone_hex_too_long_raises():
    """Kill `<= -> >` on line 1860 indirectly and lock the upper bound:
    len > 4 must raise."""
    with pytest.raises(SyntaxError, match="too long"):
        parse_source("{ 12345 }")


# ---------------------------------------------------------------------------
# _handle_raw_hex_data_block
# ---------------------------------------------------------------------------


def test_raw_hex_block_produces_bytes():
    """Kill `lbrace_token is None` flip, `while True -> False`, the
    `current_token == RBRACE` and `current_token.type == IDENTIFIER`
    branch flips on lines 1919/1923, and the EOF-check `is/== /or` flips
    on line 1910 (which would all raise on a valid block)."""
    parser = parse_source("{ 01 02 03 }")
    raw = [n for n in parser.ir_stream if isinstance(n, IRRawBytes)]
    assert len(raw) == 3
    assert raw[0].byte_values == [0x01]
    assert raw[1].byte_values == [0x02]
    assert raw[2].byte_values == [0x03]
    # PC advanced by 3 bytes past 0x0100 padding.
    assert parser.current_address == 0x0103


def test_raw_hex_block_unclosed_raises_specific_message():
    """Kill `or -> and` mutation on line 1910 -- only the EOF/None branch
    detects the unclosed block and produces this exact message."""
    with pytest.raises(SyntaxError, match="Unclosed raw hex data block"):
        parse_source("{ 01 02")


def test_raw_hex_block_end_logged(caplog):
    """Kill `self.current_token -> not (self.current_token)` on line 1936:
    the End log line only fires when the guard is truthy."""
    with caplog.at_level(logging.DEBUG, logger="yooxn.yooxnas"):
        parse_source("{ 01 }")
    assert any("Raw Hex Data Block End" in r.message for r in caplog.records)


# ---------------------------------------------------------------------------
# _handle_raw_addressing_rune_op
# ---------------------------------------------------------------------------


def test_raw_abs_label_placeholder_basic():
    """Kill `rune_token is None` flip (line 1313): without the placeholder
    being appended, this assertion fails. Also kills `and -> or` on
    line 1378 (would treat `label` as a sub-label prefix and then expect
    another identifier, raising)."""
    parser = parse_source("=label")
    placeholders = [
        n for n in parser.ir_stream if isinstance(n, IRLabelPlaceholder)
    ]
    assert len(placeholders) == 1
    assert placeholders[0].label_name == "label"
    assert placeholders[0].ref_type == "RAW_ABS16"
    assert placeholders[0].size == 2


def test_raw_abs_anonymous_block():
    """Kill `==/!=`, `and/or`, and `not(...)` mutants on line 1338: the
    LBRACE branch must be selected when the operand is `{`."""
    parser = parse_source("={ INC }")
    placeholders = [
        n for n in parser.ir_stream if isinstance(n, IRLabelPlaceholder)
    ]
    assert len(placeholders) == 1
    assert placeholders[0].label_name.startswith("__ANON_END_")
    assert placeholders[0].ref_type == "RAW_ABS16"


def test_raw_abs_ampersand_sublabel():
    """Kill the `== -> !=` on line 1379 and `or -> and` on line 1380:
    AMPERSAND must trigger the sub-label branch."""
    parser = parse_source("@parent &child =&child")
    placeholders = [
        n for n in parser.ir_stream if isinstance(n, IRLabelPlaceholder)
    ]
    assert len(placeholders) == 1
    assert placeholders[0].label_name == "parent/child"


def test_raw_abs_slash_sublabel():
    """Kill the `== -> !=` on line 1380: SLASH must trigger sub-label
    prefix handling just like AMPERSAND.

    Note: the lexer treats `/foo` (no leading whitespace) as a single
    IDENTIFIER, so a separating space is required for `/` to be tokenized
    as RUNE_FORWARDSLASH.
    """
    parser = parse_source("@parent &child = /child")
    placeholders = [
        n for n in parser.ir_stream if isinstance(n, IRLabelPlaceholder)
    ]
    assert len(placeholders) == 1
    assert placeholders[0].label_name == "parent/child"


def test_raw_abs_plain_label_is_not_sublabel():
    """Kill `is_sub_label_ref = False -> True` on line 1376: a plain
    `=label` with no `&`/`/` must resolve to `label`, not
    `<current_scope>/label`."""
    # current_scope defaults to 'on-reset' -- with the mutation, label_name
    # would become 'on-reset/foo'.
    parser = parse_source("=foo")
    placeholders = [
        n for n in parser.ir_stream if isinstance(n, IRLabelPlaceholder)
    ]
    assert len(placeholders) == 1
    assert placeholders[0].label_name == "foo"


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def _write_source(tmp_path, body):
    src = tmp_path / "prog.tal"
    src.write_text(body)
    return src


def test_main_valid_file_returns_zero_and_writes_rom(tmp_path, monkeypatch):
    """Kill `args.file -> not(args.file)` (line 2242) and
    `!= -> ==` / `not(...)` mutants on line 2252: without entering the
    parse branch the ROM is never written."""
    src = _write_source(tmp_path, "|0100 INC")
    out = tmp_path / "out.rom"
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("sys.argv", ["yooxnas", str(src), "-o", str(out)])
    rc = main()
    assert rc == 0
    assert out.exists()
    assert out.stat().st_size > 0


# Note: `tokens and tokens[-1].type != ILLEGAL` -- the lexer always emits
# EOF as the last token (ILLEGAL chars don't terminate scanning), so the
# `and -> or` mutation on this line is behaviorally equivalent and not
# killable through observable behavior.


def test_main_debug_flag_sets_debug_level(tmp_path, monkeypatch):
    """Kill `args.debug -> not(args.debug)` on line 2239 (positive case):
    --debug must call logger.setLevel(DEBUG)."""
    src = _write_source(tmp_path, "|0100 INC")
    out = tmp_path / "out.rom"
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        "sys.argv", ["yooxnas", "--debug", str(src), "-o", str(out)]
    )
    with patch("yooxn.yooxnas.logger.setLevel") as set_level:
        rc = main()
    assert rc == 0
    set_level.assert_any_call(logging.DEBUG)


def test_main_without_debug_flag_does_not_set_debug_level(
    tmp_path, monkeypatch
):
    """Kill `args.debug -> not(args.debug)` (negative case): without
    --debug, logger.setLevel must NOT be invoked."""
    src = _write_source(tmp_path, "|0100 INC")
    out = tmp_path / "out.rom"
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("sys.argv", ["yooxnas", str(src), "-o", str(out)])
    with patch("yooxn.yooxnas.logger.setLevel") as set_level:
        rc = main()
    assert rc == 0
    set_level.assert_not_called()
