import numpy as np

def distance_metric(U: np.ndarray, V: np.ndarray) -> float:
    """
    Computes the global-phase-invariant distance between target U and implementation V.
    d(U,V) = sqrt(1 - |Tr(U^dagger V)| / 2)
    """
    trace_val = np.abs(np.trace(U.conj().T @ V))
    return np.sqrt(1 - (trace_val / 2))

# Standard Gate Matrices
I = np.eye(2)
H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
S = np.array([[1, 0], [0, 1j]])
T = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]])

def rz_rotation(angle: float) -> np.ndarray:
    """Returns the matrix for R_z(angle)."""
    return np.array([
        [np.exp(-1j * angle / 2), 0],
        [0, np.exp(1j * angle / 2)]
    ])

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

if __name__ == "__main__":
    # --- 1. Verify the Distance Metric ---
    print("--- Verifying Distance Metric ---")
    
    # Target: R_z(pi/4). Note: R_z(pi/4) differs from T by a global phase!
    # R_z(pi/4) = exp(-i pi/8) * T
    target_U = rz_rotation(np.pi / 4)
    implementation_V = T 
    
    dist = distance_metric(target_U, implementation_V)
    print(f"Distance between R_z(pi/4) and T gate: {dist:.6f}") 
    # Should be ~0.0 because the metric is global-phase-invariant!

    # --- 2. Tracking the Overhead for n=3 (R_z(pi/8)) ---
    print("\n--- Overhead Analysis for R_z(pi/8) ---")
    
    # To approximate R_z(pi/8), you would use Solovay-Kitaev or Gridsynth in Part 2.
    # Let's pretend your synthesis yielded this sequence (H, T, S, H, T):
    # (Replace this list with the actual output from your Team Synthesis Part 2)
    synthesized_sequence = ['H', 'T', 'S', 'H', 'T']
    
    # Multiply the matrices to get the implemented unitary
    V_approx = I
    gate_map = {'H': H, 'S': S, 'T': T}
    for g in synthesized_sequence:
        V_approx = gate_map[g] @ V_approx
        
    target_pi_8 = rz_rotation(np.pi / 8)
    approx_dist = distance_metric(target_pi_8, V_approx)
    
    costs = evaluate_synthesis_costs(synthesized_sequence)
    
    print(f"Sequence: {synthesized_sequence}")
    print(f"Approximation Distance: {approx_dist:.6f}")
    print(f"Hardware Costs with T-Injection:")
    for k, v in costs.items():
        print(f"  - {k}: {v}")
        
    print("\nNotice how a 'simple' 1-qubit R_z(pi/8) suddenly requires:")
    print(f"  - {costs['2_qubit_gate_count']} CNOTs (2-qubit gates)")
    print(f"  - {costs['ancilla_count']} Extra physical qubits")
    print(f"  - {costs['feed_forward']} Feed-forward classical measurements")
    print(f"  - {costs['repeated_trials']} Expected trials if feed-forward is unavailable")
    print("This is the ghost's warning: 1-qubit non-Clifford gates are incredibly expensive!")