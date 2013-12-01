import re

def adaptation_time(logfile):
    time = []
    with open(logfile, mode="r") as f:
        for l in f:
            # check for new adaptation iteration
            m_start = re.search(r"Starting adaptation iteration", l)
            if m_start is not None:
                # append a new dictionary
                time.append({})
                continue
            m_reparallelization = re.search(r"Re-parallelization time = (?P<time>[^$]*)", l)
            if m_reparallelization is not None:
                time[-1]["Re-parallelization"] = float(m_reparallelization.group('time'))
                continue
            m_solve = re.search(r"Steady solve CPU time = (?P<time>[^$]*)", l)
            if m_solve is not None:
                time[-1]["Solve"] = float(m_solve.group('time'))
                continue
            m_errest = re.search(r"Error estimation and adaptation time = (?P<time>[^$]*)", l)
            if m_errest is not None:
                time[-1]["ErrEst"] = float(m_errest.group('time'))
                continue
    return time

def adaptation_errest(logfile):
    data = []
    with open(logfile, mode="r") as f:
        for l in f:
            m = re.search(r"Output error estimate = (?P<errest>[^$]*)", l)
            if m is not None:
                data.append(float(m.group('errest')))
    return data

