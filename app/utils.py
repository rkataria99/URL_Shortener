# TODO: Implement utility functions here
# Consider functions for:
# - Generating short codes
# - Validating URLs
# - Any other helper functions you need
import re
import random
import string

def is_valid_url(url):
    """
    Validates if the input string is a proper URL.
    Accepts optional http(s), domain name, and optional path.
    """
    pattern = re.compile(
        r'^(https?://)?'
        r'([a-zA-Z0-9.-]+)?'
        r'(\.[a-zA-Z]{2,})'
        r'(/.*)?$'                    # Other optional path
    )
    return bool(pattern.match(url))

def generate_short_code(length=6):
    """
    Generates a random alphanumeric short code of fixed length.
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
