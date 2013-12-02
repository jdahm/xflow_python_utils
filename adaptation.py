import re

def adaptation_time(logfile):
    time_points = (("Re-parallelization time = ", "ReParallelization"),
        ("Steady solve CPU time = ", "Solve"),
        ("Steady adjoint solve CPU time = ", "Adjoint"),
        ("Error estimation and adaptation time = ", "ErrEst"))
    time = []
    with open(logfile, mode="r") as f:
        for l in f:
            # check for new adaptation iteration
            m_start = re.search(r"Starting adaptation iteration", l)
            if m_start is not None:
                # append a new dictionary
                time.append({})
                continue
            for p in time_points:
                m = re.search("{}(?P<time>[^$]*)".format(p[0]), l)
                if m is not None:
                    time[-1][p[1]] = float(m.group('time'))
    return time

def adaptation_errest(logfile):
    data = []
    with open(logfile, mode="r") as f:
        for l in f:
            m = re.search(r"Output error estimate = (?P<errest>[^$]*)", l)
            if m is not None:
                data.append(float(m.group('errest')))
    return data

