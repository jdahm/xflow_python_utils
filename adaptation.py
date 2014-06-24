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
            m_start_adapt = re.search(r"Starting adaptation iteration", l)
            if m_start_adapt is not None:
                # append a new dictionary
                time.append({})
                continue
            for p in time_points:
                m = re.search("{}(?P<time>[^$]*)".format(p[0]), l)
                if m is not None:
                    time[-1][p[1]] = float(m.group('time'))
    return time

def _adaptation_errest(logfile):
    data = []
    with open(logfile, mode="r") as f:
        for l in f:
            m = re.search(r"Output error estimate = (?P<errest>[^$]*)", l)
            if m is not None:
                data.append(float(m.group('errest')))
    return data

def adaptation_convergence_data(logfile):
    errest_data = _adaptation_errest(logfile)
    time_data = adaptation_time(logfile)

    if len(errest_data) != len(time_data)-1:
        raise ValueError()

    data = []
    for t in time_data:
        data.append({'Time' : {k:v for (k,v) in t.items()}})
        data[-1]['Time']['Total'] = sum(t[k] for k in t)
    for i,e in enumerate(errest_data):
        data[i]['ErrorEstimate'] = e

    return data
