# Mutation Testing Tasks

## Summary

- Raw mutations: 40
- Unique mutation records after dedupe: 40
- Unique source locations: 21 (lines with multiple operators)
- Files affected: 1

Most affected files:

- `./src/yooxn/yooxnas.py` (40 mutations)

## Targets

### `./src/yooxn/yooxnas.py::_handle_standalone_hex_data`

CRAP: **65.8** | CC: **8** | Coverage: **3.3%** | Priority: **190.0**

### `./src/yooxn/yooxnas.py::_handle_raw_hex_data_block`

CRAP: **62.4** | CC: **8** | Coverage: **5.3%** | Priority: **186.1**

### `./src/yooxn/yooxnas.py::main`

CRAP: **51.1** | CC: **7** | Coverage: **3.4%** | Priority: **175.2**

### `./src/yooxn/yooxnas.py::_handle_raw_addressing_rune_op`

CRAP: **38.2** | CC: **16** | Coverage: **55.8%** | Priority: **149.2**

## High Priority

### `./src/yooxn/yooxnas.py`

#### `_handle_raw_hex_data_block`

| Line | Mutation(s) | Operator hint |
|-----:|-------------|---------------|
| 1903 | `is -> is not`, `lbrace_token is None -> not (lbrace_token is None)` | Add tests covering both the None and the non-None case. Add tests that drive the condition both truthy and falsy. |

#### `_handle_standalone_hex_data`

| Line | Mutation(s) | Operator hint |
|-----:|-------------|---------------|
| 1850 | `is -> is not`, `data_token is None -> not (data_token is None)` | Add tests covering both the None and the non-None case. Add tests that drive the condition both truthy and falsy. |
| 1856 | `== -> !=`, `data_len == 0 -> not (data_len == 0)` | Add tests covering equal and non-equal inputs. Add tests that drive the condition both truthy and falsy. |
| 1858 | `<= -> <`, `<= -> >` | Add boundary tests at the exact threshold value. Add tests covering inputs on both sides of the comparison. |
| 1860 | `<= -> <`, `<= -> >` | Add boundary tests at the exact threshold value. Add tests covering inputs on both sides of the comparison. |
| 1867 | `== -> !=`, `data_size == 1 -> not (data_size == 1)` | Add tests covering equal and non-equal inputs. Add tests that drive the condition both truthy and falsy. |
| 1869 | `== -> !=` | Add tests covering equal and non-equal inputs. |

### Context

**Line 1903** — is -> is not, lbrace_token is None -> not (lbrace_token is None)

```text
  1900 |         Called when current_token is RUNE_LBRACE.
  1901 |         """
  1902 |         lbrace_token = self.current_token
> 1903 |         if lbrace_token is None:
  1904 |             return
  1905 |         logger.debug(f"  Raw Hex Data Block Start {{ (Line {lbrace_token.line})")
  1906 |         self._advance()  # Consume '{'
```

> Add a test for `_handle_raw_hex_data_block` in `./src/yooxn/yooxnas.py` that covers both the None and non-None case at line 1903. The test should fail if `is` is changed to `is not`.

> Add a test for `_handle_raw_hex_data_block` in `./src/yooxn/yooxnas.py` that drives the condition at line 1903 both truthy and falsy. The test should fail if `lbrace_token is None` is changed to `not (lbrace_token is None)`.

**Line 1850** — is -> is not, data_token is None -> not (data_token is None)

```text
  1847 |         # For hex literal as raw data
  1848 |         self._ensure_default_start_page()
  1849 |         data_token = self.current_token
> 1850 |         if data_token is None:
  1851 |             return
  1852 |         op_addr = self.current_address
  1853 |         data_word = data_token.word
```

> Add a test for `_handle_standalone_hex_data` in `./src/yooxn/yooxnas.py` that covers both the None and non-None case at line 1850. The test should fail if `is` is changed to `is not`.

> Add a test for `_handle_standalone_hex_data` in `./src/yooxn/yooxnas.py` that drives the condition at line 1850 both truthy and falsy. The test should fail if `data_token is None` is changed to `not (data_token is None)`.

**Line 1856** — == -> !=, data_len == 0 -> not (data_len == 0)

```text
  1853 |         data_word = data_token.word
  1854 |         data_len = len(data_word)
  1855 |         data_size = 0
> 1856 |         if data_len == 0:
  1857 |             raise SyntaxError("Empty raw hex data.", token=data_token)
  1858 |         elif data_len <= 2:
  1859 |             data_size = 1
```

> Add a test for `_handle_standalone_hex_data` in `./src/yooxn/yooxnas.py` that covers both equal and non-equal inputs. The test should fail if `==` at line 1856 is changed to `!=`.

> Add a test for `_handle_standalone_hex_data` in `./src/yooxn/yooxnas.py` that drives the condition at line 1856 both truthy and falsy. The test should fail if `data_len == 0` is changed to `not (data_len == 0)`.

**Line 1858** — <= -> <, <= -> >

```text
  1855 |         data_size = 0
  1856 |         if data_len == 0:
  1857 |             raise SyntaxError("Empty raw hex data.", token=data_token)
> 1858 |         elif data_len <= 2:
  1859 |             data_size = 1
  1860 |         elif data_len <= 4:
  1861 |             data_size = 2
```

> Add a boundary test for `_handle_standalone_hex_data` in `./src/yooxn/yooxnas.py` at the exact threshold value. The test should fail if `<=` at line 1858 is changed to `<`.

> Add a test for `_handle_standalone_hex_data` in `./src/yooxn/yooxnas.py` that covers inputs on both sides of the comparison. The test should fail if `<=` at line 1858 is changed to `>`.

**Line 1860** — <= -> <, <= -> >

```text
  1857 |             raise SyntaxError("Empty raw hex data.", token=data_token)
  1858 |         elif data_len <= 2:
  1859 |             data_size = 1
> 1860 |         elif data_len <= 4:
  1861 |             data_size = 2
  1862 |         else:
  1863 |             raise SyntaxError(f"Raw hex data {data_word} is too long", token=data_token)
```

> Add a boundary test for `_handle_standalone_hex_data` in `./src/yooxn/yooxnas.py` at the exact threshold value. The test should fail if `<=` at line 1860 is changed to `<`.

> Add a test for `_handle_standalone_hex_data` in `./src/yooxn/yooxnas.py` that covers inputs on both sides of the comparison. The test should fail if `<=` at line 1860 is changed to `>`.

**Line 1867** — == -> !=, data_size == 1 -> not (data_size == 1)

```text
  1864 |         try:
  1865 |             val_int = int(data_word, 16)
  1866 |             byte_values = []
> 1867 |             if data_size == 1:
  1868 |                 byte_values.append(val_int & 0xFF)
  1869 |             elif data_size == 2:
  1870 |                 # High byte, then low byte.
```

> Add a test for `_handle_standalone_hex_data` in `./src/yooxn/yooxnas.py` that covers both equal and non-equal inputs. The test should fail if `==` at line 1867 is changed to `!=`.

> Add a test for `_handle_standalone_hex_data` in `./src/yooxn/yooxnas.py` that drives the condition at line 1867 both truthy and falsy. The test should fail if `data_size == 1` is changed to `not (data_size == 1)`.

**Line 1869** — == -> !=

```text
  1866 |             byte_values = []
  1867 |             if data_size == 1:
  1868 |                 byte_values.append(val_int & 0xFF)
> 1869 |             elif data_size == 2:
  1870 |                 # High byte, then low byte.
  1871 |                 byte_values.append((val_int >> 8) & 0xFF)
  1872 |                 byte_values.append(val_int & 0xFF)
```

> Add a test for `_handle_standalone_hex_data` in `./src/yooxn/yooxnas.py` that covers both equal and non-equal inputs. The test should fail if `==` at line 1869 is changed to `!=`.

## Medium Priority

### `./src/yooxn/yooxnas.py`

#### `_handle_raw_hex_data_block`

| Line | Mutation(s) | Operator hint |
|-----:|-------------|---------------|
| 1909 | `True -> False`, `True -> not (True)` | Assert both the true and the false branch independently. Add tests that drive the condition both truthy and falsy. |
| 1910 | `is -> is not`, `== -> !=`, `or -> and`, `self.current_token is None or self.current_token.type == TOKENTYPE.EOF -> not (self.current_token is None or self.current_token.type == TOKENTYPE.EOF)` | Add tests covering both the None and the non-None case. Add tests covering equal and non-equal inputs. Add truth-table style tests for both sides of the condition. Add tests that drive the condition both truthy and falsy. |
| 1919 | `== -> !=`, `self.current_token.type == TOKENTYPE.RUNE_RBRACE -> not (self.current_token.type == TOKENTYPE.RUNE_RBRACE)` | Add tests covering equal and non-equal inputs. Add tests that drive the condition both truthy and falsy. |
| 1923 | `== -> !=`, `self.current_token.type == TOKENTYPE.IDENTIFIER -> not (self.current_token.type == TOKENTYPE.IDENTIFIER)` | Add tests covering equal and non-equal inputs. Add tests that drive the condition both truthy and falsy. |
| 1936 | `self.current_token -> not (self.current_token)` | Add tests that drive the condition both truthy and falsy. |

#### `main`

| Line | Mutation(s) | Operator hint |
|-----:|-------------|---------------|
| 2239 | `args.debug -> not (args.debug)` | Add tests that drive the condition both truthy and falsy. |
| 2242 | `args.file -> not (args.file)` | Add tests that drive the condition both truthy and falsy. |

## Low Priority

### `./src/yooxn/yooxnas.py`

#### `_handle_raw_addressing_rune_op`

| Line | Mutation(s) | Operator hint |
|-----:|-------------|---------------|
| 1313 | `is -> is not`, `rune_token is None -> not (rune_token is None)` | Add tests covering both the None and the non-None case. Add tests that drive the condition both truthy and falsy. |
| 1338 | `== -> !=`, `and -> or`, `self.current_token and self.current_token.type == TOKENTYPE.RUNE_LBRACE -> not (self.current_token and self.current_token.type == TOKENTYPE.RUNE_LBRACE)` | Add tests covering equal and non-equal inputs. Add truth-table style tests for both sides of the condition. Add tests that drive the condition both truthy and falsy. |
| 1376 | `False -> True` | Assert both the true and the false branch independently. |
| 1378 | `and -> or`, `self.current_token and (
                self.current_token.type == TOKENTYPE.RUNE_AMPERSAND
                or self.current_token.type == TOKENTYPE.RUNE_FORWARDSLASH
            ) -> not (self.current_token and (
                self.current_token.type == TOKENTYPE.RUNE_AMPERSAND
                or self.current_token.type == TOKENTYPE.RUNE_FORWARDSLASH
            ))` | Add truth-table style tests for both sides of the condition. Add tests that drive the condition both truthy and falsy. |
| 1379 | `== -> !=` | Add tests covering equal and non-equal inputs. |
| 1380 | `== -> !=`, `or -> and` | Add tests covering equal and non-equal inputs. Add truth-table style tests for both sides of the condition. |

#### `main`

| Line | Mutation(s) | Operator hint |
|-----:|-------------|---------------|
| 2252 | `!= -> ==`, `and -> or`, `tokens and tokens[-1].type != TOKENTYPE.ILLEGAL -> not (tokens and tokens[-1].type != TOKENTYPE.ILLEGAL)` | Add tests covering equal and non-equal inputs. Add truth-table style tests for both sides of the condition. Add tests that drive the condition both truthy and falsy. |

