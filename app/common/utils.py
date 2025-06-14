import secrets
import string

def generate_random_string(length: int = 32) -> str:
    """
    Generate a random string of specified length.
    Uses only letters and digits.
    
    Args:
        length (int): Length of the random string. Defaults to 32.
        
    Returns:
        str: Random string of specified length
    """
    # Define the character set (only letters and digits)
    characters = string.ascii_letters + string.digits
    
    # Generate random string using secrets module (cryptographically secure)
    return ''.join(secrets.choice(characters) for _ in range(length)) 