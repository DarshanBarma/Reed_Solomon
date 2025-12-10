
import random
from typing import List, Tuple


def corrupt_with_xor(corrupted_bytes: bytearray, positions: List[int]) -> List[Tuple[int, int, int, int]]:
    """
    Corrupt bytes using random XOR flips.
    
    Args:
        corrupted_bytes: The bytearray to corrupt (modified in place)
        positions: List of positions to corrupt
        
    Returns:
        List of tuples (position, original_value, xor_value, new_value)
    """
    changes = []
    for pos in positions:
        original_value = corrupted_bytes[pos]
        xor_val = random.randint(1, 255)  # non-zero to guarantee change
        corrupted_bytes[pos] ^= xor_val
        new_value = corrupted_bytes[pos]
        changes.append((pos, original_value, xor_val, new_value))
    return changes


def corrupt_with_awgn(corrupted_bytes: bytearray, positions: List[int], 
                      sigma: float) -> List[Tuple[int, int, float, int]]:
    """
    Corrupt bytes using AWGN-like (Additive White Gaussian Noise) model.
    
    Args:
        corrupted_bytes: The bytearray to corrupt (modified in place)
        positions: List of positions to corrupt
        sigma: Standard deviation of the Gaussian noise
        
    Returns:
        List of tuples (position, original_value, noise, new_value)
    """
    changes = []
    for pos in positions:
        original_value = corrupted_bytes[pos]
        noise = random.gauss(0.0, sigma)
        noisy_val = int(round(original_value + noise))
        noisy_val = max(0, min(255, noisy_val))  # Clip to byte range
        corrupted_bytes[pos] = noisy_val
        changes.append((pos, original_value, noise, noisy_val))
    return changes


def apply_corruption(encoded_bytes: bytes, n_errors: int, mode: str, 
                    noise_sigma: float = None) -> Tuple[bytearray, List[int], List]:
    """
    Apply corruption to encoded bytes.
    
    Args:
        encoded_bytes: The encoded codeword
        n_errors: Number of bytes to corrupt
        mode: Corruption mode ('1' for XOR, '2' for AWGN)
        noise_sigma: Standard deviation for AWGN mode
        
    Returns:
        Tuple of (corrupted_bytes, corruption_positions, changes)
    """
    corrupted_bytes = bytearray(encoded_bytes)
    
    if n_errors == 0:
        return corrupted_bytes, [], []
    
    # Choose random distinct positions to corrupt
    corruption_positions = random.sample(range(len(corrupted_bytes)), n_errors)
    corruption_positions.sort()
    
    if mode == "1":
        changes = corrupt_with_xor(corrupted_bytes, corruption_positions)
    else:  # mode == "2"
        changes = corrupt_with_awgn(corrupted_bytes, corruption_positions, noise_sigma)
    
    return corrupted_bytes, corruption_positions, changes


def print_corruption_changes(changes: List, mode: str, noise_sigma: float = None):
    """
    Print the corruption changes in a formatted way.
    
    Args:
        changes: List of change tuples from corruption functions
        mode: Corruption mode ('1' for XOR, '2' for AWGN)
        noise_sigma: Standard deviation for AWGN mode (for display)
    """
    print("Byte changes (original → corrupted):")
    
    if mode == "1":
        # XOR mode: (position, original_value, xor_value, new_value)
        for pos, orig, xor_val, new_val in changes:
            print(f"  position {pos:3d}: {orig:3d}  XOR {xor_val:3d}  →  {new_val:3d}")
    else:
        # AWGN mode: (position, original_value, noise, new_value)
        for pos, orig, noise, new_val in changes:
            print(f"  position {pos:3d}: {orig:3d}  + N(0,{noise_sigma})  →  {new_val:3d}")
    print()
