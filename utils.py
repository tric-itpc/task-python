from datetime import datetime, timedelta
def calc_downtime(from_state, to_state, last_time):
    if from_state == "non-stable" and (to_state == "stable" or to_state == "semi-stable"):
        print(last_time)
        print("kzkkzkz")
        delta = datetime.now() - last_time
        print(delta)
        return datetime.strptime(str(delta), '%H:%M:%S.%f')
    else:
        return None

def calc_sum_downtime(query):
    sum_not_stable = timedelta(seconds=0)
    cnst = datetime(1900, 1, 1)
    for i in query:
        if i.from_state == "non-stable":
            sum_not_stable = sum_not_stable + (i.time_not_working - cnst)
    return sum_not_stable