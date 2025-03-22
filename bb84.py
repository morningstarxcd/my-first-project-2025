from qiskit import QuantumCircuit, Aer, execute
import random

def generate_random_bits(n):
    """Generate n random classical bits (0 or 1)"""
    return [random.randint(0, 1) for _ in range(n)]

def generate_random_bases(n):
    """Generate n random bases (0 for Z-basis, 1 for X-basis)"""
    return [random.randint(0, 1) for _ in range(n)]

def encode_qubits(bits, bases):
    """Create a quantum circuit that encodes bits using given bases"""
    qubits = QuantumCircuit(len(bits), len(bits))
    for i in range(len(bits)):
        if bits[i] == 1:
            qubits.x(i)  # Apply X gate for bit 1
        if bases[i] == 1:
            qubits.h(i)  # Apply H gate for X-basis
    return qubits

def measure_qubits(qubits, bases):
    """Measure qubits based on chosen bases"""
    for i in range(len(bases)):
        if bases[i] == 1:
            qubits.h(i)  # Apply H gate if measuring in X-basis
        qubits.measure(i, i)
    simulator = Aer.get_backend('qasm_simulator')
    result = execute(qubits, simulator, shots=1).result()
    return list(result.get_counts().keys())[0][::-1]  # Reverse string for correct order

def bb84_protocol(n):
    """Simulate BB84 Quantum Key Distribution"""
    print("=== BB84 Quantum Key Distribution Simulation ===")
    
    # Step 1: Alice generates random bits and bases
    alice_bits = generate_random_bits(n)
    alice_bases = generate_random_bases(n)
    
    print(f"Alice's bits:  {alice_bits}")
    print(f"Alice's bases: {alice_bases}")

    # Step 2: Alice encodes bits into qubits
    qubits = encode_qubits(alice_bits, alice_bases)

    # Step 3: Bob chooses random bases
    bob_bases = generate_random_bases(n)
    print(f"Bob's bases:   {bob_bases}")

    # Step 4: Bob measures qubits
    bob_results = measure_qubits(qubits, bob_bases)
    bob_bits = [int(bit) for bit in bob_results]
    
    print(f"Bob's bits:    {bob_bits}")

    # Step 5: Compare bases and generate a shared secret key
    shared_key = [alice_bits[i] for i in range(n) if alice_bases[i] == bob_bases[i]]
    print(f"Shared Key:    {shared_key}")

# Run BB84 with 10 bits
bb84_protocol(10)
