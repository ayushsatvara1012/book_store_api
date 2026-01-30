from threading import Lock

Books_DB = [
    {'id': 1, 'title': 'World War', 'author': 'Mr.ABC', 'year': 1234},
    {'id': 2, 'title': 'Titanic', 'author': 'Mr.Titanic', 'year': 1999},
    {'id': 3, 'title': 'Comedy King', 'author': 'Mr.Newbie', 'year': 1800}
    ]

_next_id = 4
_id_lock = Lock()

def get_new_id() -> int:
    """Thread-safe method to get and increment the ID"""
    global _next_id
    with _id_lock:
        new_id = _next_id
        _next_id += 1
    return new_id

def reset_db_state():
    global _next_id
    with _id_lock:
        _next_id = 1
