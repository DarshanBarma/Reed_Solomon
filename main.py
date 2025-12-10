"""
Reed-Solomon Error Correction Demo (QR-Style, Text Only)

This is the main entry point for the Reed-Solomon error correction demonstration.
The code is organized into separate modules for better maintainability:
- config.py: Configuration constants and error correction levels
- reed_solomon_codec.py: Encoding and decoding logic
- corruption.py: Corruption simulation (XOR and AWGN)
- ui_utils.py: Display and animation utilities
"""

from config import ERROR_CORRECTION_LEVELS, CORRUPTION_MODE_XOR, CORRUPTION_MODE_AWGN
from reed_solomon_codec import ReedSolomonEncoder
from corruption import apply_corruption, print_corruption_changes
from ui_utils import (
    animate, print_header, print_section, print_ec_levels,
    print_encoding_info, print_corruption_info, print_decoding_concept,
    print_summary
)


def get_user_message() -> str:
    """Get the message from the user."""
    return input("Enter a message to protect with error correction: ")


def get_error_correction_level() -> tuple[str, int]:
    """
    Prompt user to choose error correction level.
    
    Returns:
        Tuple of (level_name, n_parity_bytes)
    """
    print_ec_levels()
    
    while True:
        ec_level = input("Choose error correction level (L, M, Q, H): ").strip().upper()
        if ec_level in ERROR_CORRECTION_LEVELS:
            return ec_level, ERROR_CORRECTION_LEVELS[ec_level]
        print("Invalid choice. Please enter L, M, Q, or H.")


def get_corruption_parameters(max_bytes: int, max_correctable: int) -> tuple[int, str, float]:
    """
    Get corruption parameters from user.
    
    Args:
        max_bytes: Maximum number of bytes that can be corrupted
        max_correctable: Maximum number of correctable bytes
        
    Returns:
        Tuple of (n_errors, mode, noise_sigma)
    """
    print(f"Note: With {max_correctable * 2} parity bytes, we can correct up to {max_correctable} byte errors.")
    print("If you corrupt more than this, decoding will probably fail.")
    print()
    
    # Get number of errors
    while True:
        try:
            n_errors = int(input("How many codeword bytes should we corrupt? "))
            if 0 <= n_errors <= max_bytes:
                break
            print(f"Please enter a number between 0 and {max_bytes}.")
        except ValueError:
            print("Please enter a valid integer.")
    
    print()
    print("Choose corruption model:")
    print("  1 → Random byte flips (XOR)  [discrete, like random bit errors]")
    print("  2 → AWGN-like noise          [add Gaussian noise to byte values]")
    
    # Get corruption mode
    while True:
        mode = input("Enter 1 or 2: ").strip()
        if mode in (CORRUPTION_MODE_XOR, CORRUPTION_MODE_AWGN):
            break
        print("Please enter 1 or 2.")
    
    # Get noise sigma if AWGN mode
    noise_sigma = None
    if mode == CORRUPTION_MODE_AWGN:
        while True:
            try:
                noise_sigma = float(input("Enter noise standard deviation (e.g. 5, 10, 20): "))
                if noise_sigma >= 0:
                    break
                print("Please enter a non-negative value.")
            except ValueError:
                print("Please enter a valid number.")
    
    return n_errors, mode, noise_sigma


def main():
    """Main function orchestrating the Reed-Solomon demo."""
    print_header("Reed-Solomon Error Correction Demo (QR-Style, Text Only)")
    
    # ========================================================================
    # STEP 1: Get the message from the user
    # ========================================================================
    message = get_user_message()
    print()
    
    # ========================================================================
    # STEP 2: Choose error correction level (QR-style: L, M, Q, H)
    # ========================================================================
    ec_level, n_parity = get_error_correction_level()
    print()
    
    # ========================================================================
    # STEP 3: Encode with Reed-Solomon
    # ========================================================================
    print_section("STEP 1: Converting message to bytes")
    
    encoder = ReedSolomonEncoder(n_parity)
    message_bytes, encoded_bytes = encoder.encode(message)
    
    print_encoding_info(message, message_bytes, encoded_bytes, ec_level, n_parity)
    
    # ========================================================================
    # STEP 4: Add encoding animation and display
    # ========================================================================
    print_section("STEP 2: Adding Reed-Solomon error correction")
    
    animate("Building Reed–Solomon encoder")
    animate("Generating parity bytes")
    print()
    
    # ========================================================================
    # STEP 5: Simulate corruption (errors)
    # ========================================================================
    print_section("STEP 3: Simulating transmission errors (corruption)")
    
    max_correctable = encoder.get_max_correctable()
    n_errors, mode, noise_sigma = get_corruption_parameters(
        len(encoded_bytes), max_correctable
    )
    
    print()
    corrupted_bytes, corruption_positions, changes = apply_corruption(
        encoded_bytes, n_errors, mode, noise_sigma
    )
    
    if n_errors > 0:
        print(f"Corrupting {n_errors} byte(s) at positions: {corruption_positions}")
        print_corruption_changes(changes, mode, noise_sigma)
    
    print_corruption_info(encoded_bytes, corrupted_bytes, corruption_positions, mode, noise_sigma)
    
    # ========================================================================
    # STEP 6: Attempt to decode and correct errors
    # ========================================================================
    print_section("STEP 4: Decoding with Reed-Solomon error correction")
    
    print_decoding_concept()
    
    animate("Computing syndromes")
    animate("Locating and correcting errors")
    
    success, decoded_message, decoded_bytes = encoder.decode(corrupted_bytes)
    
    if success:
        # Count how many bytes were actually different from the original codeword
        introduced_errors = [
            i for i in range(len(encoded_bytes)) if encoded_bytes[i] != corrupted_bytes[i]
        ]
        num_introduced_errors = len(introduced_errors)
        
        print("✓ Decoding successful!")
        print()
        print(f"Bytes that were corrupted (positions): {corruption_positions}")
        print(f"Number of bytes actually changed:      {num_introduced_errors}")
        print()
        print(f"Decoded message: '{decoded_message}'")
        print()
        
        if decoded_message == message:
            print("✓ Perfect match! Reed-Solomon successfully corrected all errors within its capability.")
        else:
            print("⚠ Decoded message differs from original (unexpected in normal RS behaviour).")
    else:
        print("✗ Decoding failed!")
        print()
        print(f"Too many errors for error correction level {ec_level}.")
        print(f"You corrupted {n_errors} bytes, but can only correct up to {max_correctable} bytes.")
        print("Try again with:")
        print(f"  - Fewer corrupted bytes (≤ {max_correctable}), OR")
        print("  - A higher error correction level (M, Q, or H)")
    
    # ========================================================================
    # STEP 7: Summary
    # ========================================================================
    print_summary(message, ec_level, n_parity, n_errors, mode, noise_sigma, success, decoded_message)


if __name__ == "__main__":
    main()
