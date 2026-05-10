import numpy as np

def evaluate_synthesis_costs(clifford_t_sequence: list[str]) -> dict:
    """
    Takes a sequence of gates from the Clifford+T set and calculates the 
    new physical costs when T-gates must be injected using an ancilla.
    """
    costs = {
        "logical_gates": len(clifford_t_sequence),
        "ancilla_count": 0,
        "2_qubit_gate_count": 0,
        "feed_forward": 0,
        "circuit_depth": 0,
        "repeated_trials": 1
    }
    
    t_count = 0
    for gate in clifford_t_sequence:
        if gate == 'T':
            t_count += 1
            # T-gate injection overhead:
            costs["ancilla_count"] += 1      # 1 Magic state needed per T gate
            costs["2_qubit_gate_count"] += 1 # 1 CNOT for injection
            costs["feed_forward"] += 1       # 1 Classical check for the S correction
            costs["circuit_depth"] += 3      # Prepare magic state, CNOT, Measure+Correct
        else:
            costs["circuit_depth"] += 1
            
    # If feed-forward is unavailable, success is 50% per T-gate (post-selection)
    costs["repeated_trials"] = 2 ** t_count

    return costs

def _matrix_sqrt_hermitian(matrix: np.ndarray) -> np.ndarray:
    """
    Computes the square root of a Hermitian positive semidefinite matrix.
    """
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    clipped_eigenvalues = np.clip(eigenvalues, 0.0, None)
    return (eigenvectors * np.sqrt(clipped_eigenvalues)) @ eigenvectors.conj().T

def density_matrix_fidelity(rho: np.ndarray, sigma: np.ndarray) -> float:
    """
    Computes the Uhlmann fidelity between two density matrices.

    For density matrices, the fidelity is
    F(rho, sigma) = (Tr[sqrt(sqrt(rho) sigma sqrt(rho))])^2.
    """
    sqrt_rho = _matrix_sqrt_hermitian(rho)
    intermediate = sqrt_rho @ sigma @ sqrt_rho
    sqrt_intermediate = _matrix_sqrt_hermitian(intermediate)
    fidelity = np.real(np.trace(sqrt_intermediate)) ** 2
    return float(np.clip(fidelity, 0.0, 1.0))