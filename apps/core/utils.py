from datetime import datetime
import hashlib
import random


def generate_password(full_name):
    return "".join([full_name, "@1234"])


def generate_unique_code(
    prefix, unique_identifier, include_timestamp=True, length=8
) -> str:
    """
    Generate a short and unique code for various entities.

    Args:
        prefix (str): A short prefix to identify the entity type.
        unique_identifier (str|int): A unique identifier,
        such as supplier ID, payment ID, etc.
        include_timestamp (bool): Whether to include the current timestamp
        for additional uniqueness.
        length (int): The length of the hashed portion of the code.

    Returns:
        str: A generated unique code.
    """
    random_suffix = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=4))

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S") if include_timestamp else ""
    base_string = (
        f"{unique_identifier}-{timestamp}" if timestamp else str(unique_identifier)
    )
    hashed_part = hashlib.md5(base_string.encode()).hexdigest()[:length].upper()

    return f"{prefix}-{hashed_part}-{random_suffix}"
