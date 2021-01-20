import uuid
from datetime import datetime


def generate_json_unique_file_name(records_count: int):
    """
    Generates unique name of file using current date and uuid
    """
    file_name = f"{str(datetime.now().date())}_{uuid.uuid1()}_{records_count}.json"
    return file_name
