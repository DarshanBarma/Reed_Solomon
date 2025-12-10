from reedsolo import RSCodec, ReedSolomonError
import random


def main():
    print("=" * 70)
    print("Reed-Solomon Error Correction Demo (QR-Style, Text Only)")
    print("=" * 70)
    print()

    # ========================================================================
    # STEP 1: Get the message from the user
    # ========================================================================
    message = input("Enter a message to protect with error correction: ")
    print()

    # ========================================================================
    # STEP 2: Choose error correction level (QR-style: L, M, Q, H)
    # ========================================================================
    print("QR-style error correction levels (simplified for this demo):")
    print("  L (Low)      →  8 parity bytes  (can correct up to 4 byte errors)")
    print("  M (Medium)   → 16 parity bytes  (can correct up to 8 byte errors)")
    print("  Q (Quartile) → 24 parity bytes  (can correct up to 12 byte errors)")
    print("  H (High)     → 32 parity bytes  (can correct up to 16 byte errors)")
    print()

    ec_map = {
        'L': 8,
        'M': 16,
        'Q': 24,
        'H': 32
    }

    while True:
        ec_level = input("Choose error correction level (L, M, Q, H): ").strip().upper()
        if ec_level in ec_map:
            break
        print("Invalid choice. Please enter L, M, Q, or H.")

    n_parity = ec_map[ec_level]
    print()

    # ========================================================================
    # STEP 3: Convert message to bytes
    # ========================================================================
    print("-" * 70)
    print("STEP 1: Converting message to bytes")
    print("-" * 70)

    message_bytes = message.encode("utf-8")

    print(f"Original message: '{message}'")
    print(f"Message bytes ({len(message_bytes)} data bytes):")
    print(f"  {list(message_bytes)}")
    print()

    # ========================================================================
    # STEP 4: Encode with Reed-Solomon (add parity bytes)
    # ========================================================================
    print("-" * 70)
    print("STEP 2: Adding Reed-Solomon error correction")
    print("-" * 70)

    rs = RSCodec(n_parity)
    encoded_bytes = rs.encode(message_bytes)

    max_correctable = n_parity // 2

    print(f"Chosen EC level: {ec_level}")
    print(f"Parity bytes added (error correction code): {n_parity}")
    print(f"Maximum correctable byte errors (t = n_parity/2): {max_correctable}")
    print()

    print("Full codeword (data bytes + parity bytes):")
    print(f"  {list(encoded_bytes)}")
    print(f"Total length: {len(encoded_bytes)} bytes")
    print()

    # Show which part is data and which part is parity (the 'error code')
    data_len = len(message_bytes)
    data_part = list(encoded_bytes[:data_len])
    parity_part = list(encoded_bytes[data_len:])

    print("Data part (original message bytes):")
    print(f"  indices 0 .. {data_len - 1}")
    print(f"  {data_part}")
    print()

    print("Error correction code (ECC bytes / parity bytes):")
    print(f"  indices {data_len} .. {len(encoded_bytes) - 1}")
    print(f"  Raw ECC bytes: {parity_part}")
    print("  ECC bytes one by one:")
    for i, b in enumerate(parity_part):
        print(f"    ECC[{i}] at codeword position {data_len + i}: {b}")
    print()

    print("CONCEPTUAL VIEW OF ENCODING:")
    print("  • Treat the message bytes as coefficients of a polynomial M(x).")
    print("  • Reed–Solomon constructs a generator polynomial G(x).")
    print("  • It computes parity bytes as the remainder when M(x) * x^n_parity")
    print("    is divided by G(x).")
    print("  • Those remainder bytes are the ECC (the parity bytes you see above).")
    print()

    # ========================================================================
    # STEP 5: Simulate corruption (errors)
    # ========================================================================
    print("-" * 70)
    print("STEP 3: Simulating transmission errors (corruption)")
    print("-" * 70)
    print(f"Note: With {n_parity} parity bytes, we can correct up to {max_correctable} byte errors.")
    print("If you corrupt more than this, decoding will probably fail.")
    print()

    while True:
        try:
            n_errors = int(input("How many codeword bytes should we corrupt? "))
            if 0 <= n_errors <= len(encoded_bytes):
                break
            print(f"Please enter a number between 0 and {len(encoded_bytes)}.")
        except ValueError:
            print("Please enter a valid integer.")

    corrupted_bytes = bytearray(encoded_bytes)

    if n_errors > 0:
        # Choose random distinct positions to corrupt
        corruption_positions = random.sample(range(len(corrupted_bytes)), n_errors)
        corruption_positions.sort()

        print()
        print(f"Corrupting {n_errors} byte(s) at positions: {corruption_positions}")
        print("Byte changes (original → corrupted):")

        for pos in corruption_positions:
            original_value = corrupted_bytes[pos]
            xor_val = random.randint(1, 255)  # non-zero to guarantee change
            corrupted_bytes[pos] ^= xor_val
            new_value = corrupted_bytes[pos]
            print(f"  position {pos:3d}: {original_value:3d}  XOR {xor_val:3d}  →  {new_value:3d}")

        print()
        print("Original codeword:")
        print(f"  {list(encoded_bytes)}")
        print("Corrupted codeword:")
        print(f"  {list(corrupted_bytes)}")
        print()
    else:
        print("No corruption applied. The codeword is transmitted perfectly.")
        print()
        corruption_positions = []

    # ========================================================================
    # STEP 6: Attempt to decode and correct errors
    # ========================================================================
    print("-" * 70)
    print("STEP 4: Decoding with Reed-Solomon error correction")
    print("-" * 70)

    print("CONCEPTUAL VIEW OF DECODING (what Reed–Solomon does internally):")
    print("  1) Compute 'syndromes' from the received codeword.")
    print("     • If all syndromes are zero → no errors.")
    print("     • If some are non-zero → errors are present.")
    print("  2) From the syndromes, build the error locator polynomial Λ(x).")
    print("     • The roots of Λ(x) give the positions of the errors.")
    print("  3) Build the error evaluator polynomial Ω(x).")
    print("     • This tells how big each error is at those positions.")
    print("  4) Correct the codeword by subtracting the error values.")
    print("  5) Recover the original data bytes from the corrected codeword.")
    print("Note: The 'reedsolo' library does all this math internally for us.")
    print()

    try:
        decoded_result = rs.decode(bytes(corrupted_bytes))

        # Handle both possible return types (tuple or bytes)
        if isinstance(decoded_result, tuple):
            decoded_bytes = decoded_result[0]
        else:
            decoded_bytes = decoded_result

        decoded_message = decoded_bytes.decode("utf-8")

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

        success = True

    except ReedSolomonError:
        print("✗ Decoding failed!")
        print()
        print(f"Too many errors for error correction level {ec_level}.")
        print(f"You corrupted {n_errors} bytes, but can only correct up to {max_correctable} bytes.")
        print("Try again with:")
        print(f"  - Fewer corrupted bytes (≤ {max_correctable}), OR")
        print("  - A higher error correction level (M, Q, or H)")
        success = False

    # ========================================================================
    # STEP 7: Summary
    # ========================================================================
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Original message:          '{message}'")
    print(f"Chosen EC level:           {ec_level} ({n_parity} parity bytes)")
    print(f"Maximum correctable bytes: {max_correctable}")
    print(f"Bytes requested to corrupt:{n_errors}")
    print(f"Decoding result:           {'SUCCESS' if success else 'FAILED'}")
    if success:
        print(f"Final decoded message:     '{decoded_message}'")


if __name__ == "__main__":
    main()
