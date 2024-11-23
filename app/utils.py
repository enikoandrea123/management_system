from datetime import datetime

def calculate_due_date():
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
