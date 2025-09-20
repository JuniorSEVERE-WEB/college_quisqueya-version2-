import threading

_local = threading.local()

def set_current_user(user):
    _local.user = user

def get_current_user():
    return getattr(_local, "user", None)

def clear_current_user():
    if hasattr(_local, "user"):
        delattr(_local, "user")

def set_current_academic_year(ay):
    _local.academic_year = ay

def get_current_academic_year():
    return getattr(_local, "academic_year", None)

def clear_current_academic_year():
    if hasattr(_local, "academic_year"):
        delattr(_local, "academic_year")