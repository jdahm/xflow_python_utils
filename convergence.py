import re
import matplotlib.pyplot as plt

def _read_jobfile(jobfile):
    j = {}
    with open(jobfile, mode="r") as f:
        for l in f:
            m = re.match(r"\s*(?P<key>[^=\s]+)\s*=\s*(?P<val>[^\s]+)", l)
            if m is not None:
                j[m.group('key')] = m.group('val')
    return j


def _get_log_header(logfile):
    with open(logfile, mode="r") as f:
        for l in f:
            m = re.match(r"\%\>", l)
            if m is not None:
                header = []
                pos = 2
                while pos <= len(l):
                    m = re.match(r"\s+(\S+)", l[pos:])
                    if m is None:
                        return header
                    else:
                        header.append(m.group(1))
                        pos += m.end(1)
                return header


def _read_linear_solver_data(line, linear_solver, data=None):
    if data is None:
        if linear_solver == 'GMRES':
            data = {'nOuter' : 0, 'nInner' : [], 'LinearNorm' : []}
        else:
            raise ValueError()

    if linear_solver == 'GMRES':
        m = re.match(r"\s*GMRES:\s*iOuter\s*=\s*(?P<iOuter>[0-9]+),\s*iInner\s*=\s*(?P<iInner>[0-9]+),\s*Linear norm\s*=\s*(?P<LinearNorm>\S+)", line)
        if m is None: raise ValueError()
        # print(line, int(m.group('iOuter')), data['nOuter'])
        if data['nOuter'] != int(m.group('iOuter')): raise ValueError()
        data['nOuter'] += 1
        data['nInner'].append(int(m.group('iInner')))
        data['LinearNorm'].append(float(m.group('LinearNorm')))
    else:
        raise ValueError()

    return data


def nonlinear_convergence_data(jobfile, logfile):
    """Parses a log file of xflow stdout containing convergence data.
    
    Returns a list of dictionaries describing the nonlinear convergence
    process. Each dictionary has the entries:

    nNonlinearIter : Number of nonlinear iterations [int]
    Residual : Nonlinear residual for each iteration [list]
    LinearIter : Linear solver convergence data for each iteartion [list of
                 dicts]
    Outputs : Convergence of each output for each iteartion [list of dicts]"""

    # Get the jobfile parameters
    jobfile = _read_jobfile(jobfile)

    # Get the header
    header = _get_log_header(logfile)

    # List of outputs
    Outputs = header[header.index('Rnorm')+1:]

    # Build the re.match string for nonlinear iterations
    nonlinear_iter_search = ''.join(["\s+(?P<{}>\S+)".format(h) for h in header])
    nonlinear_iter_search += "\n"

    convergence_data = []

    with open(logfile, mode="r") as f:
        last_iteration_number = 0
        reading_nonlinear_solve = False
        reading_linear_solve = False
        failed_iter = False
        at_beginning = True
        for l in f:
            m0 = re.match(nonlinear_iter_search, l)
            m1 = re.match(r"Steady solve CPU time = \S+", l)
            m2 = re.match(r"Nonlinear solver converged to tolerance.", l)
            m3 = re.match(r"xf_NO_UPDATE", l)
            m4 = re.match(r"Decreasing", l)
            m5 = re.match(r"Calling steady solver.", l)
            if m0 is not None:
                if m0.group('Iter').isdigit():
                    iteration_number = int(m0.group('Iter'))
                    reading_nonlinear_solve = True
                    reading_linear_solve = False
                    if iteration_number == 0 or at_beginning:
                        # Check if at the beginning of a nonlinear solve
                        d = {'nNonlinearIter' : 0, 'Residual' : [], 'LinearIter' : [], 'Outputs' : []}
                        last_iteration_number = iteration_number
                        at_beginning = False
                    else:
                        d['nNonlinearIter'] += 1
                        d['Residual'].append(float(m0.group('Rnorm')))
                        d['Outputs'].append([{o : float(m0.group(o)) for o in Outputs}])
                        last_iteration_number = iteration_number
                    failed_iter = False
            elif (m1 is not None or m2 is not None) and reading_nonlinear_solve:
                # Check if at the end of a nonlinear solve
                convergence_data.append(d)
                reading_nonlinear_solve = False
                reading_linear_solve = False
            elif m3 is not None or m4 is not None:
                # This is a solver message
                failed_iter = True
            elif m5 is not None:
                # Entering solver
                at_beginning = True
            elif reading_nonlinear_solve:
                # Else if inside a nonlinear solve, these must be linear solver lines
                if reading_linear_solve:
                    d['LinearIter'][-1] = _read_linear_solver_data(l, jobfile['LinearSolver'], data=d['LinearIter'][-1])
                else:
                    d['LinearIter'].append(_read_linear_solver_data(l, jobfile['LinearSolver']))
                    reading_linear_solve = True
            else:
                # Else these are other adaptation lines
                pass

        if d != convergence_data[-1]:
            convergence_data.append(d)
    return convergence_data


def sequence_time(logfile):
    time = []
    with open(logfile, mode="r") as f:
        for l in f:
            m_solve = re.search(r"Steady solve CPU time = (?P<time>[^$]*)", l)
            if m_solve is not None:
                time.append(float(m_solve.group('time')))
    return time

