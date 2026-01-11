# === Python Modules ===
from uuid import uuid4

# === Function to generate a uniqe run_id ===
def get_run_id():
    """
    Generates a unique `run_id` each time the model runs

    returns:
        - run_id (str): Unique run_id for logging
    """
    return str(uuid4())[:8]