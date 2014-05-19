#!/usr/bin/env python3

import subprocess as sp
import re

def nelem_xfa(xfafile):
    info = sp.check_output(["xf_Info", xfafile])
    found = False
    skipped = False
    nelem = 0
    egrp = 0
    for l in info.splitlines():
        sl = str(l)
        m = re.search('nElemGroup\s+=\s+(\d+)', sl)
        if m is not None:
            negrp = int(m.group(1))
            found = True
        elif found and not skipped:
            skipped = True
            continue
        elif found and skipped and (egrp < negrp):
            m = re.search('\s+\d+\s+\w+\s+\d+\s+(\d+)\s+\d+', sl)
            if m is None:
                raise ValueError("egrp < negrp but no match found")
            nelem += int(m.group(1))
            egrp += 1
        elif found and skipped and egrp >= negrp: break
    return nelem

def n0_xfa(xfafile):
    out = sp.check_output(["xf_NonZeros", xfafile])
    return int(out.splitlines()[-1])
