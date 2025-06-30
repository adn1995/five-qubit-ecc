# filename: five_qubit_ecc.py
# authors: Amanda Curtis and Arthur Diep-Nguyen
"""This module contains Qiskit functions that construct quantum circuits
for implementing and testing the five-qubit error correcting code.
"""

from qiskit.circuit import (QuantumCircuit,
                            QuantumRegister,
                            AncillaRegister,
                            ClassicalRegister,
                            Gate)
from qiskit_aer.noise import NoiseModel, pauli_error

# Use the following imports in the notebook for simulating
# from qiskit_aer import AerSimulator
# from qiskit import transpile

########################################################################
########################################################################
# Five-qubit error correcting code
########################################################################
########################################################################

def five_qubit_ecc(x: bool = False) -> QuantumCircuit:
    """Returns a quantum circuit that implements the five-qubit error
    correcting code.

    Parameters
    ----------
    x : bool
        Boolean that will be prepared into a logical state

    Returns
    -------
    QuantumCircuit
        Quantum circuit that prepares the logical state corresponding to
        the boolean `x`, runs the state through an empty gate, measures
        syndromes, applies recovery operations (if needed), and measures
        the data qubits.
        The empty gate exists for a NoiseModel to apply a random Pauli
        error.
    """
    logical_state = QuantumRegister(5, name="x")

    # Quantum register for checking generators of the stabilizer
    checks = AncillaRegister(4, name="checks")

    # Classical register for measuring syndromes
    syndromes = ClassicalRegister(4, name="s")

    # Classical register for measuring the logical state
    data = ClassicalRegister(5, name="c")

    qc = QuantumCircuit(logical_state,
                        checks,
                        syndromes,
                        data,
                        name="main circuit")

    # Prepare logical state
    qc.compose(prepare_state(x).to_gate(),
                logical_state,
                inplace=True)

    # Empty error channel
    # Use barriers to prevent transpiler from messing with this gate
    # When transpiling, make sure that "error channel" is a basis gate
    qc.barrier(logical_state)
    qc.compose(error_channel(5),
                logical_state,
                inplace=True)
    qc.barrier(logical_state)

    # Measure syndromes
    qc.compose(measure_syndromes(),
                qubits=[*logical_state, *checks],
                clbits=syndromes,
                inplace=True)

    # Apply recovery operations
    qc.compose(error_correction(),
                qubits=logical_state,
                clbits=syndromes,
                inplace=True)

    # Measure the logical state
    for i in range(5):
        qc.measure(logical_state[i], data[i])

    return qc

########################################################################
########################################################################
# Subcircuits
########################################################################
########################################################################

def prepare_state(x: bool) -> QuantumCircuit:
    """Returns a quantum circuit that prepares the logical state for the
    five-qubit error correcting code.

    Parameters
    ----------
    x : bool
        Boolean that will be prepared into a logical state

    Returns
    -------
    QuantumCircuit
        Quantum circuit that prepares the logical state |x_L>
        corresponding to the boolean `x`
    """
    qr = QuantumRegister(5, name="x")

    qc = QuantumCircuit(qr, name="state preparation")

    if x == True:
        qc.x(4)

    qc.h(0)
    qc.s(0)

    qc.cz(0,1)
    qc.cz(0,3)
    qc.cy(0,4)

    qc.h(1)

    qc.cz(1,2)
    qc.cz(1,3)
    qc.cx(1,4)

    qc.h(2)

    qc.cz(2,0)
    qc.cz(2,1)
    qc.cx(2,4)

    qc.h(3)
    qc.s(3)

    qc.cz(3,0)
    qc.cz(3,2)
    qc.cy(3,4)

    return qc

def error_channel(nqubits: int = 5) -> Gate:
    """Returns an empty quantum gate, to which noise will be applied
    by a NoiseModel.

    Parameters
    ----------
    nqubits : int
        Number of physical qubits

    Returns
    -------
    Gate
    """
    # Quantum register for physical qubits
    qr = QuantumRegister(nqubits, name="x")

    qc = QuantumCircuit(qr, name="error channel")

    return qc.to_gate()

def measure_syndromes() -> QuantumCircuit:
    """Returns the quantum circuit for measuring syndromes of the
    five-qubit error correcting code.
    """
    logical_state = QuantumRegister(5, name="x")

    # Quantum register for checking generators of the stabilizer
    checks = AncillaRegister(4, name="checks")

    # Classical register for measuring syndromes
    syndromes = ClassicalRegister(4, name="s")

    qc = QuantumCircuit(logical_state,
                        checks,
                        syndromes,
                        name="syndrome measurement")

    # Generators for the stabilizer are
    # XZZXI, IXZZX, XIXZZ, ZXIXZ

    # Measure the stabilizer generators, as in Figure 10.13 of N&C

    # XZZXI
    qc.h(checks[0])
    qc.cx(checks[0], logical_state[0])
    qc.cz(checks[0], logical_state[1])
    qc.cz(checks[0], logical_state[2])
    qc.cx(checks[0], logical_state[3])
    qc.h(checks[0])

    # IXZZX
    qc.h(checks[1])
    qc.cx(checks[1], logical_state[1])
    qc.cz(checks[1], logical_state[2])
    qc.cz(checks[1], logical_state[3])
    qc.cx(checks[1], logical_state[4])
    qc.h(checks[1])

    # XIXZZ
    qc.h(checks[2])
    qc.cx(checks[2], logical_state[0])
    qc.cx(checks[2], logical_state[2])
    qc.cz(checks[2], logical_state[3])
    qc.cz(checks[2], logical_state[4])
    qc.h(checks[2])

    # ZXIXZ
    qc.h(checks[3])
    qc.cz(checks[3], logical_state[0])
    qc.cx(checks[3], logical_state[1])
    qc.cx(checks[3], logical_state[3])
    qc.cz(checks[3], logical_state[4])
    qc.h(checks[3])

    # Measure syndromes
    for i in range(4):
        qc.measure(checks[i], syndromes[i])

    return qc

def error_correction() -> QuantumCircuit:
    """Returns the quantum circuit that applies recovery operations
    based on the measured syndromes.
    """
    logical_state = QuantumRegister(5, name="x")

    # Classical register for measured syndromes
    syndromes = ClassicalRegister(4, name="s")

    qc = QuantumCircuit(logical_state,
                        syndromes,
                        name="recovery operations")

    with qc.switch(syndromes) as case:
        # case(0) needs no recovery operation
        with case(1):
            qc.x(0)
        with case(2):
            qc.z(2)
        with case(3):
            qc.x(4)
        with case(4):
            qc.z(4)
        with case(5):
            qc.z(1)
        with case(6):
            qc.x(3)
        with case(7):
            qc.y(4)
        with case(8):
            qc.x(1)
        with case(9):
            qc.z(3)
        with case(10):
            qc.z(0)
        with case(11):
            qc.y(0)
        with case(12):
            qc.x(2)
        with case(13):
            qc.y(1)
        with case(14):
            qc.y(2)
        with case(15):
            qc.y(3)

    return qc

########################################################################
########################################################################
# Random Pauli error
########################################################################
########################################################################

def random_pauli(p: float) -> NoiseModel:
    """Returns the NoiseModel for random Pauli error on the error
    channel.

    Parameters
    ----------
    p : float
        Probability that a given Pauli gate is applied to a physical
        qubit

    Returns
    -------
    NoiseModel
    """
    random_pauli_error = pauli_error([("X", p),
                                        ("Y", p),
                                        ("Z", p),
                                        ("I", 1-3*p)])

    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(random_pauli_error,
                                            "error channel")

    return noise_model
