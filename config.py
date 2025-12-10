# QR-style error correction levels
# Maps level name to number of parity bytes
ERROR_CORRECTION_LEVELS = {
    'L': 8,   # Low:      8 parity bytes  (can correct up to 4 byte errors)
    'M': 16,  # Medium:  16 parity bytes  (can correct up to 8 byte errors)
    'Q': 24,  # Quartile: 24 parity bytes (can correct up to 12 byte errors)
    'H': 32   # High:    32 parity bytes  (can correct up to 16 byte errors)
}
#Corruption modes
CORRUPTION_MODE_XOR = "1"
CORRUPTION_MODE_AWGN = "2"

ANIMATION_STEPS = 3
ANIMATION_DELAY = 0.4
