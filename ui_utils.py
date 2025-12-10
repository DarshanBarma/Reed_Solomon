
import time
from config import ANIMATION_STEPS, ANIMATION_DELAY


def animate(message: str, steps: int = ANIMATION_STEPS, delay: float = ANIMATION_DELAY):
    """Simple terminal 'animation' with dots."""
    print(message, end="", flush=True)
    for _ in range(steps):
        print(".", end="", flush=True)
        time.sleep(delay)
    print()  # newline


def print_header(title: str, width: int = 70):
    """Print a formatted header."""
    print("=" * width)
    print(title)
    print("=" * width)
    print()


def print_section(title: str, width: int = 70):
    """Print a formatted section divider."""
    print("-" * width)
    print(title)
    print("-" * width)


def print_ec_levels():
    """Display available error correction levels."""
    print("QR-style error correction levels (simplified for this demo):")
    print("  L (Low)      →  8 parity bytes  (can correct up to 4 byte errors)")
    print("  M (Medium)   → 16 parity bytes  (can correct up to 8 byte errors)")
    print("  Q (Quartile) → 24 parity bytes  (can correct up to 12 byte errors)")
    print("  H (High)     → 32 parity bytes  (can correct up to 16 byte errors)")
    print()


def print_encoding_info(message: str, message_bytes: bytes, encoded_bytes: bytes, 
                       ec_level: str, n_parity: int):
    """Display encoding information."""
    print(f"Original message: '{message}'")
    print(f"Message bytes ({len(message_bytes)} data bytes):")
    print(f"  {list(message_bytes)}")
    print()
    
    max_correctable = n_parity // 2
    print(f"Chosen EC level: {ec_level}")
    print(f"Parity bytes added (error correction code): {n_parity}")
    print(f"Maximum correctable byte errors (t = n_parity/2): {max_correctable}")
    print()
    
    print("Full codeword (data bytes + parity bytes):")
    print(f"  {list(encoded_bytes)}")
    print(f"Total length: {len(encoded_bytes)} bytes")
    print()
    
    # Show data and parity parts
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


def print_corruption_info(encoded_bytes: bytes, corrupted_bytes: bytearray, 
                         corruption_positions: list, mode: str, noise_sigma: float = None):
    """Display corruption information."""
    if len(corruption_positions) == 0:
        print("No corruption applied. The codeword is transmitted perfectly.")
        print()
        return
    
    print(f"Corrupting {len(corruption_positions)} byte(s) at positions: {corruption_positions}")
    print()
    print("Original codeword:")
    print(f"  {list(encoded_bytes)}")
    print()
    print("Corrupted codeword:")
    print(f"  {list(corrupted_bytes)}")
    print()
    print("Corrupted message:")
    print(f"{corrupted_bytes.decode('utf-8', errors='replace')}")


def print_decoding_concept():
    """Print the conceptual view of Reed-Solomon decoding."""
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


def print_summary(original_message: str, ec_level: str, n_parity: int, 
                 n_errors: int, mode: str, noise_sigma: float, 
                 success: bool, decoded_message: str = None):
    """Print the final summary."""
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    max_correctable = n_parity // 2
    print(f"Original message:          '{original_message}'")
    print(f"Chosen EC level:           {ec_level} ({n_parity} parity bytes)")
    print(f"Maximum correctable bytes: {max_correctable}")
    print(f"Bytes requested to corrupt:{n_errors}")
    corruption_model = 'XOR random errors' if mode == '1' else f'AWGN-like (σ={noise_sigma})'
    print(f"Corruption model:          {corruption_model}")
    print(f"Decoding result:           {'SUCCESS' if success else 'FAILED'}")
    if success and decoded_message:
        print(f"Final decoded message:     '{decoded_message}'")
