from functional_dependency import FD

def aPlus(f:set[FD], a:set[str]):
    # a is set of attributes
    # f is set of functional dependencies
    result = a.copy() 
    temp = len(result)
    while True:
        for fd in f: 
            if fd.lhs.issubset(result):
                result = result.union(fd.rhs)
        if temp != len(result): temp = len(result)
        else: break
    
    return result
    
if __name__ == "__main__":
    ''' Example: 
    
    R = (A, B, C, G, H, I)
    F = {  A → B
           A → C
           CG → H
           CG → I
           B → H   }
    
    '''

    f = { # set of functional dependencies
        FD({'A'}, {'B'}),
        FD({'A'}, {'C'}),
        FD({'C', 'G'}, {'H'}),
        FD({'C', 'G'}, {'I'}),
        FD({'B'}, {'H'})
    }

    # find (AG)+

    AG_plus = aPlus(f, {'A', 'G'})
    print(AG_plus)
