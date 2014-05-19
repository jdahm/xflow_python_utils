import re

def sequence_time(logfile):
    time = []
    with open(logfile, mode="r") as f:
        for l in f:
            m_solve = re.search(r"Steady solve CPU time = (?P<time>[^$]*)", l)
            if m_solve is not None:
                time.append(float(m_solve.group('time')))
    return time

def steady_solve_niter(logfile):
    niter = []
    with open(logfile, mode="r") as f:
        for l in f:
            m_start_order = re.search(r"Calling steady solver", l)
            if m_start_order is not None:
                niter.append({"nNonLinear" : 0, "nLinear" : 0})
            m_iter = re.search(r"\s+[0-9]+\s+[0-9]+", l)
            if m_iter is not None:
                niter[-1]["nNonLinear"] += 1
            m_gmres = re.search(r"\s+GMRES:\s+iOuter\s+=\s+\d+,\s+iInner\s+=\s+(?P<iInner>\d+)", l)
            if m_gmres is not None:
                niter[-1]["nLinear"] += int(m_gmres.group('iInner'))

    return niter

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

def adaptation_errest(logfile):
    data = []
    with open(logfile, mode="r") as f:
        for l in f:
            m = re.search(r"Output error estimate = (?P<errest>[^$]*)", l)
            if m is not None:
                data.append(float(m.group('errest')))
    return data

