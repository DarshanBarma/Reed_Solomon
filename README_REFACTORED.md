# Reed-Solomon Error Correction Demo

A comprehensive demonstration of Reed-Solomon error correction codes with QR-style error correction levels.

## Project Structure

The codebase is organized into modular components for better maintainability and clarity:

```
Reed_Solomon/
├── main.py                    # Main entry point and orchestration
├── config.py                  # Configuration constants and EC levels
├── reed_solomon_codec.py      # Encoding/decoding logic
├── corruption.py              # Error simulation (XOR and AWGN)
├── ui_utils.py               # Display and animation utilities
├── pyproject.toml            # Project dependencies
└── README_REFACTORED.md      # This file
```

### Module Overview

#### `config.py`
Contains configuration constants:
- **ERROR_CORRECTION_LEVELS**: Maps QR-style levels (L/M/Q/H) to parity bytes
- **CORRUPTION_MODE_XOR**: Constant for XOR corruption mode
- **CORRUPTION_MODE_AWGN**: Constant for AWGN corruption mode
- Animation settings (steps and delay)

#### `reed_solomon_codec.py`
Provides the `ReedSolomonEncoder` class:
- `encode(message)`: Encodes a string message with Reed-Solomon error correction
- `decode(corrupted_bytes)`: Attempts to decode and correct errors
- `get_max_correctable()`: Returns maximum correctable byte errors

#### `corruption.py`
Functions for simulating transmission errors:
- `corrupt_with_xor()`: Applies random XOR bit flips
- `corrupt_with_awgn()`: Applies Gaussian noise to byte values
- `apply_corruption()`: Main interface for applying corruption
- `print_corruption_changes()`: Displays corruption details

#### `ui_utils.py`
User interface and display functions:
- `animate()`: Terminal animation with dots
- `print_header()`, `print_section()`: Formatted output
- `print_ec_levels()`: Display available error correction levels
- `print_encoding_info()`: Show encoding details
- `print_corruption_info()`: Show corruption results
- `print_decoding_concept()`: Explain Reed-Solomon decoding
- `print_summary()`: Final summary output

#### `main.py`
Main program flow:
- `get_user_message()`: Input message from user
- `get_error_correction_level()`: Select EC level (L/M/Q/H)
- `get_corruption_parameters()`: Configure error simulation
- `main()`: Orchestrates the entire demo workflow

## Features

### Error Correction Levels (QR-Style)
- **L (Low)**: 8 parity bytes → corrects up to 4 byte errors
- **M (Medium)**: 16 parity bytes → corrects up to 8 byte errors
- **Q (Quartile)**: 24 parity bytes → corrects up to 12 byte errors
- **H (High)**: 32 parity bytes → corrects up to 16 byte errors

### Corruption Models
1. **XOR Random Errors**: Discrete bit flips (simulates random bit errors)
2. **AWGN-like Noise**: Additive White Gaussian Noise (simulates analog channel noise)

## Installation

```bash
# Install dependencies
uv sync
```

## Usage

### macOS (with zbar library)
```bash
uv run env DYLD_LIBRARY_PATH=/opt/homebrew/lib python main.py
```

### Interactive Mode
The program will guide you through:
1. Enter a message to protect
2. Choose error correction level (L/M/Q/H)
3. Specify number of bytes to corrupt
4. Select corruption model (XOR or AWGN)
5. View encoding, corruption, and decoding results

## How It Works

### Encoding Process
1. Convert message to UTF-8 bytes
2. Build Reed-Solomon codec with specified parity bytes
3. Generate error correction code (ECC) by treating message bytes as polynomial coefficients
4. Append ECC bytes to create the full codeword

### Corruption Simulation
- Randomly select byte positions to corrupt
- Apply either XOR flips or Gaussian noise
- Track and display all changes

### Decoding Process
1. Compute syndromes from received codeword
2. Build error locator polynomial Λ(x) to find error positions
3. Build error evaluator polynomial Ω(x) to determine error magnitudes
4. Correct errors and recover original message

## Example Output

```
======================================================================
Reed-Solomon Error Correction Demo (QR-Style, Text Only)
======================================================================

Enter a message to protect with error correction: Hello World

Choose error correction level (L, M, Q, H): L

How many codeword bytes should we corrupt? 2

Choose corruption model:
  1 → Random byte flips (XOR)
  2 → AWGN-like noise
Enter 1 or 2: 1

✓ Decoding successful!
✓ Perfect match! Reed-Solomon successfully corrected all errors.
```

## Benefits of Modular Structure

1. **Separation of Concerns**: Each module has a single, well-defined responsibility
2. **Reusability**: Components can be imported and used independently
3. **Testability**: Individual modules can be tested in isolation
4. **Maintainability**: Changes to one module don't affect others
5. **Readability**: Code is easier to understand and navigate
6. **Extensibility**: New features can be added without modifying existing code

## Dependencies

- `reedsolo>=1.7.0`: Reed-Solomon error correction implementation
- Python 3.14+

## License

See the main README.md for license information.
