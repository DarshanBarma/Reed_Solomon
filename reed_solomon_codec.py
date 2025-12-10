"""Reed-Solomon encoding and decoding functionality."""

from reedsolo import RSCodec, ReedSolomonError
from typing import Tuple, Optional


class ReedSolomonEncoder:
    """Handles Reed-Solomon encoding and decoding operations."""
    
    def __init__(self, n_parity: int):
        """
        Initialize the Reed-Solomon codec.
        
        Args:
            n_parity: Number of parity bytes for error correction
        """
        self.n_parity = n_parity
        self.rs = RSCodec(n_parity)
        self.max_correctable = n_parity // 2
    
    def encode(self, message: str) -> Tuple[bytes, bytes]:
        """
        Encode a message with Reed-Solomon error correction.
        
        Args:
            message: The string message to encode
            
        Returns:
            Tuple of (message_bytes, encoded_bytes)
        """
        message_bytes = message.encode("utf-8")
        encoded_bytes = self.rs.encode(message_bytes)
        return message_bytes, encoded_bytes
    
    def decode(self, corrupted_bytes: bytes) -> Tuple[bool, Optional[str], Optional[bytes]]:
        """
        Decode a corrupted codeword using Reed-Solomon error correction.
        
        Args:
            corrupted_bytes: The potentially corrupted codeword
            
        Returns:
            Tuple of (success, decoded_message, decoded_bytes)
            - success: True if decoding succeeded, False otherwise
            - decoded_message: The decoded string if successful, None otherwise
            - decoded_bytes: The decoded bytes if successful, None otherwise
        """
        try:
            decoded_result = self.rs.decode(bytes(corrupted_bytes))
            
            # Handle both possible return types (tuple or bytes)
            if isinstance(decoded_result, tuple):
                decoded_bytes = decoded_result[0]
            else:
                decoded_bytes = decoded_result
            
            decoded_message = decoded_bytes.decode("utf-8")
            return True, decoded_message, decoded_bytes
            
        except ReedSolomonError:
            return False, None, None
    
    def get_max_correctable(self) -> int:
        """Get the maximum number of correctable byte errors."""
        return self.max_correctable
