from contextlib import suppress
from app.models import (
    students
)

def init_all_dbs():
    with suppress(Exception):
        students.init_db()
