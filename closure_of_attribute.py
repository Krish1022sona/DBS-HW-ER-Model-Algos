from functional_dependency import FD

def aPlus(f: set[FD], a: set[str]):
    # a = attributes whose closure we want
    # f = set of functional dependencies
    result = set(a)  # start with given attributes
    prev_len = -1

    while prev_len != len(result):
        prev_len = len(result)
        for fd in f:
            # fd.lhs and fd.rhs are frozensets, but we can treat them like sets
            if fd.lhs.issubset(result):
                result |= set(fd.rhs)  # union with RHS

    return result


if __name__ == "__main__":
    '''
    Example:

    R = (A, B, C, G, H, I)
    F = {
        A → B,
        A → C,
        CG → H,
        CG → I,
        B → H
    }
    '''

    f = {
        FD({'A'}, {'B'}),
        FD({'A'}, {'C'}),
        FD({'C', 'G'}, {'H'}),
        FD({'C', 'G'}, {'I'}),
        FD({'B'}, {'H'})
    }

    # find (AG)+
    AG_plus = aPlus(f, {'A', 'G'})
    print("(AG)+ =", AG_plus)
