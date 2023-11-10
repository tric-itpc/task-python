from pytimeparse.timeparse import timeparse
from datetime import datetime


def calc_downtime(from_state, to_state, last_time):
    if from_state == "не работает" and (to_state == "работает" or to_state == "работает нестабильно"):
        delta = datetime.now() - last_time
        return str(delta)
    else:
        return None

def calc_sum_downtime(query):
    sum_not_stable = 0
    counter = 0
    for i in query:
        if i.from_state == "не работает":
            counter += 1
            sum_not_stable = sum_not_stable + timeparse(i.time_not_working)
    return (sum_not_stable, counter)


def add_objects(object, db):
    try:
        db.add(object)
        db.commit()
        db.refresh(object)

    except Exception as e:
        print(e)
