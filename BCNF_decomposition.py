from functional_dependency import FD
from closure_of_attribute import aPlus


def is_superkey(attributes: set[str], relation: set[str], F: set[FD]) -> bool:
    """
    Check if a set of attributes is a superkey for a relation.
    A set of attributes is a superkey if its closure contains all attributes of the relation.
    """
    closure = aPlus(F, attributes)
    return relation.issubset(closure)


def project_FDs(F: set[FD], relation: set[str]) -> set[FD]:
    """
    Get all FDs that are relevant to a relation.
    An FD α → β is relevant if both α and β are subsets of the relation.
    """
    return {fd for fd in F if fd.lhs.issubset(relation) and fd.rhs.issubset(relation)}


def is_in_BCNF(relation: set[str], F: set[FD]) -> tuple[bool, FD | None]:
    """
    Check if a relation is in BCNF.
    Returns (True, None) if in BCNF, or (False, violating_fd) if not.
    
    A relation is in BCNF if for every non-trivial FD α → β that holds on the relation:
    - α is a superkey for the relation
    """
    # Get all FDs that apply to this relation
    relevant_fds = project_FDs(F, relation)
    
    for fd in relevant_fds:
        alpha = set(fd.lhs)
        beta = set(fd.rhs)
        
        # Check if FD is non-trivial (β is not a subset of α)
        if not beta.issubset(alpha):
            # Check if α is a superkey for this relation
            alpha_closure = aPlus(F, alpha)
            
            # α is a superkey if α+ contains all attributes of the relation
            if not relation.issubset(alpha_closure):
                # Found a BCNF violation
                print(f"  Checking FD: {alpha} → {beta}")
                print(f"  α+ = {alpha_closure}")
                print(f"  α is NOT a superkey for {relation}")
                return False, fd
    
    return True, None


def compute_minimal_cover_fds(F: set[FD], relation: set[str]) -> set[FD]:
    """
    Compute FDs that are implied by F and are relevant to the relation.
    This finds all FDs X → A where X,A ⊆ relation and A ∈ X+
    """
    result = set()
    
    # For each subset of attributes in the relation
    from itertools import combinations
    attrs = list(relation)
    
    # Check all possible LHS (non-empty subsets)
    for r in range(1, len(attrs) + 1):
        for lhs_tuple in combinations(attrs, r):
            lhs = set(lhs_tuple)
            lhs_closure = aPlus(F, lhs)
            
            # For each attribute in closure that's in relation
            for attr in lhs_closure:
                if attr in relation and attr not in lhs:
                    # Create FD lhs → {attr}
                    result.add(FD(lhs, {attr}))
    
    return result


def BCNF_decomposition(R: set[str], F: set[FD]) -> set[frozenset[str]]:
    """
    Decompose relation R into BCNF using the given algorithm.
    
    Algorithm:
    result := {R}
    done := false
    while (not done) do
        if (there is a schema Ri in result that is not in BCNF) then
            let α → β be a non-trivial functional dependency that holds on Ri
            such that α is not a superkey, and α ∩ β = ∅
            result := (result - Ri) ∪ (Ri - β) ∪ (α, β)
        else
            done := true
    """
    result = {frozenset(R)}
    done = False
    
    iteration = 0
    while not done:
        iteration += 1
        print(f"\n--- Iteration {iteration} ---")
        print(f"Current relations: {[set(r) for r in result]}")
        
        found_violation = False
        
        for Ri in result:
            Ri_set = set(Ri)
            print(f"\nChecking relation: {Ri_set}")
            
            # Compute all FDs implied by F that apply to Ri
            Ri_fds = compute_minimal_cover_fds(F, Ri_set)
            print(f"Relevant FDs for {Ri_set}:")
            for fd in Ri_fds:
                print(f"  {set(fd.lhs)} → {set(fd.rhs)}")
            
            in_bcnf, violating_fd = is_in_BCNF(Ri_set, F)
            
            if not in_bcnf:
                alpha = set(violating_fd.lhs)
                beta = set(violating_fd.rhs)
                
                print(f"\n✗ Relation {Ri_set} is NOT in BCNF")
                print(f"  Violating FD: {alpha} → {beta}")
                
                # Check that α ∩ β = ∅
                if not alpha.isdisjoint(beta):
                    print(f"  Warning: α ∩ β ≠ ∅, skipping this FD")
                    continue
                
                # Decompose: result := (result - Ri) ∪ (Ri - β) ∪ (α ∪ β)
                result.discard(Ri)
                
                R1 = Ri_set - beta  # Ri - β
                R2 = alpha | beta    # (α, β) = α ∪ β
                
                result.add(frozenset(R1))
                result.add(frozenset(R2))
                
                print(f"  Decomposed into:")
                print(f"    R1 = {R1}")
                print(f"    R2 = {R2}")
                
                found_violation = True
                break  # Restart the check with new relations
            else:
                print(f"✓ Relation {Ri_set} is in BCNF")
        
        if not found_violation:
            done = True
            print("\n" + "="*60)
            print("All relations are in BCNF!")
    
    return result


if __name__ == "__main__":
    # Example 1: Classic BCNF decomposition example
    print("=" * 60)
    print("Example 1: R(A, B, C)")
    print("=" * 60)
    
    R1 = {'A', 'B', 'C'}
    F1 = {
        FD({'A'}, {'B'}),
        FD({'B'}, {'C'})
    }
    
    print("\nOriginal relation R:", R1)
    print("Functional dependencies F:")
    for fd in F1:
        print(f"  {fd}")
    
    print("\n" + "=" * 60)
    result1 = BCNF_decomposition(R1, F1)
    
    print("\n" + "=" * 60)
    print("FINAL BCNF DECOMPOSITION:")
    print("=" * 60)
    for i, rel in enumerate(sorted(result1, key=lambda x: sorted(x)), 1):
        print(f"R{i}: {set(rel)}")