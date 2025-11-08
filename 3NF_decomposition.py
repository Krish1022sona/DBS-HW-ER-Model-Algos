from functional_dependency import FD
from canonical_cover import canonical_cover
from closure_of_attribute import aPlus
from itertools import combinations


def find_candidate_keys(R: set[str], F: set[FD]) -> set[frozenset[str]]:
    """
    Find all candidate keys for relation R given functional dependencies F.
    A candidate key is a minimal set of attributes whose closure is R.
    """
    candidate_keys = set()
    attrs = list(R)
    
    # Check all subsets from size 1 to |R|
    for size in range(1, len(attrs) + 1):
        for subset in combinations(attrs, size):
            attr_set = set(subset)
            
            # Check if this subset's closure equals R (is a superkey)
            if aPlus(F, attr_set) >= R:
                # Check if it's minimal (no proper subset is a superkey)
                is_minimal = True
                for attr in attr_set:
                    reduced = attr_set - {attr}
                    if aPlus(F, reduced) >= R:
                        is_minimal = False
                        break
                
                if is_minimal:
                    candidate_keys.add(frozenset(attr_set))
        
        # If we found candidate keys of this size, no need to check larger sizes
        if candidate_keys:
            break
    
    return candidate_keys


def is_contained_in(Ri: frozenset[str], Rj: frozenset[str]) -> bool:
    """Check if Ri is contained in Rj (Ri ⊆ Rj)"""
    return set(Ri).issubset(set(Rj))


def NF3_decomposition(R: set[str], F: set[FD]) -> list[frozenset[str]]:
    """
    Decompose relation R into 3NF using the synthesis algorithm.
    
    Algorithm:
    1. Compute canonical cover Fc
    2. For each FD α → β in Fc, create relation schema containing α ∪ β
    3. If no schema contains a candidate key, add one
    4. Remove redundant relations (optional)
    """
    print("=" * 60)
    print("STEP 1: Computing Canonical Cover (Fc)")
    print("=" * 60)
    
    # Step 1: Compute canonical cover
    Fc = canonical_cover(F)
    print("\nCanonical Cover Fc:")
    for fd in Fc:
        print(f"  {set(fd.lhs)} → {set(fd.rhs)}")
    
    print("\n" + "=" * 60)
    print("STEP 2: Creating Schemas from Fc")
    print("=" * 60)
    
    # Step 2: Create schemas from canonical cover
    result = []
    i = 0
    
    for fd in Fc:
        alpha = set(fd.lhs)
        beta = set(fd.rhs)
        alpha_beta = alpha | beta
        
        # Check if any existing schema contains α ∪ β
        contains = False
        for j, Rj in enumerate(result):
            if alpha_beta.issubset(set(Rj)):
                contains = True
                print(f"\nFD {alpha} → {beta}:")
                print(f"  α ∪ β = {alpha_beta}")
                print(f"  Already contained in R{j+1} = {set(Rj)}")
                break
        
        if not contains:
            i += 1
            result.append(frozenset(alpha_beta))
            print(f"\nFD {alpha} → {beta}:")
            print(f"  Creating R{i} = {alpha_beta}")
    
    print("\n" + "=" * 60)
    print("STEP 3: Ensuring Candidate Key Coverage")
    print("=" * 60)
    
    # Step 3: Find candidate keys and ensure one is in some schema
    print("\nFinding candidate keys for R...")
    candidate_keys = find_candidate_keys(R, F)
    print(f"Candidate keys: {[set(ck) for ck in candidate_keys]}")
    
    # Check if any schema contains a candidate key
    has_candidate_key = False
    for j, Rj in enumerate(result):
        for ck in candidate_keys:
            if ck.issubset(Rj):
                has_candidate_key = True
                print(f"\nR{j+1} = {set(Rj)} contains candidate key {set(ck)}")
                break
        if has_candidate_key:
            break
    
    if not has_candidate_key:
        i += 1
        # Add any candidate key
        any_key = next(iter(candidate_keys))
        result.append(frozenset(any_key))
        print(f"\nNo schema contains a candidate key!")
        print(f"Creating R{i} = {set(any_key)} (candidate key)")
    
    print("\n" + "=" * 60)
    print("STEP 4: Removing Redundant Relations")
    print("=" * 60)
    
    # Step 4: Remove redundant relations
    changed = True
    while changed:
        changed = False
        to_remove = []
        
        for j in range(len(result)):
            for k in range(len(result)):
                if j != k and j not in to_remove:
                    if is_contained_in(result[j], result[k]):
                        print(f"\nR{j+1} = {set(result[j])} is contained in R{k+1} = {set(result[k])}")
                        print(f"Removing R{j+1}")
                        to_remove.append(j)
                        changed = True
                        break
        
        # Remove in reverse order to maintain indices
        for idx in sorted(to_remove, reverse=True):
            result.pop(idx)
            i -= 1
    
    if not changed:
        print("\nNo redundant relations found.")
    
    return result


if __name__ == "__main__":
    # Example 1: Classic 3NF decomposition example
    print("=" * 60)
    print("Example 1: R(A, B, C)")
    print("=" * 60)
    
    R1 = {'A', 'B', 'C'}
    F1 = {
        FD({'A'}, {'B'}),
        FD({'B'}, {'C'}),
        FD({'C'}, {'A'})
    }
    
    print("\nOriginal relation R:", R1)
    print("Functional dependencies F:")
    for fd in F1:
        print(f"  {fd}")
    print()
    
    result1 = NF3_decomposition(R1, F1)
    
    print("\n" + "=" * 60)
    print("FINAL 3NF DECOMPOSITION:")
    print("=" * 60)
    for i, rel in enumerate(result1, 1):
        print(f"R{i}: {set(rel)}")