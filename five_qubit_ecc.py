# filename: five_qubit_ecc.py
# authors: Amanda Curtis and Arthur Diep-Nguyen
"""This module contains Qiskit functions that construct quantum circuits
for implementing and testing the five-qubit error correcting code.
"""

from qiskit.circuit import (QuantumCircuit,
                            QuantumRegister,
                            AncillaRegister,
                            ClassicalRegister)
from qiskit.quantum_info import Statevector

# Use the following imports in the notebook for simulating
# from qiskit_aer import AerSimulator
# from qiskit import transpile

import numpy as np

########################################################################
########################################################################
# Main circuit
########################################################################
########################################################################

def main_circuit(x: bool, p: float, seed: int | None = None) -> QuantumCircuit:
    """Returns a quantum circuit that implements and tests the
    five-qubit error correcting code.

    Parameters
    ----------
    x : bool
        Boolean that will be prepared into a logical state
    p : float
        Error probability for each physical qubit representing `x`
    seed : int | None
        Random seed used for PRNG

    Returns
    -------
    QuantumCircuit
        Quantum circuit that prepares the logical state corresponding to
        the boolean `x`, runs the state through a random Pauli error
        channel with error rate `p` for each qubit, measures syndromes,
        applies recovery operations (if needed), and measures the data
        qubits.
    """
    logical_state = QuantumRegister(5, name="x")

    # Quantum register for syndromes
    syndromes_qr = AncillaRegister(4, name="checks")

    # Classical register for measuring syndromes
    syndromes_cr = ClassicalRegister(4, name="s")

    qc = QuantumCircuit(logical_state,
                        syndromes_qr,
                        syndromes_cr,
                        name="main circuit")

    # Prepare logical state
    qc.compose(prepare_state(x).to_gate(),
                logical_state,
                inplace=True)

    # Apply errors
    if seed is None:
        seed = np.random.randint(0, np.iinfo(np.int32).max)
    qc.compose(error_channel(p, 5, seed).to_gate(),
                logical_state,
                inplace=True)

    # Measure syndromes
    qc.compose(measure_syndromes().to_gate(),
                qubits=[*logical_state, *syndromes_qr, *syndromes_cr],
                inplace=True)

    # Apply recovery operations
    qc.compose(error_correction().to_gate(),
                qubits=[*logical_state, *syndromes_cr],
                inplace=True)

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

def error_channel(p: float,
                    nqubits: int = 5,
                    seed: int | None = None) -> QuantumCircuit:
    """Returns a quantum circuit implementing a random Pauli error
    channel.

    Parameters
    ----------
    p : float
        Error probability for each physical qubit
    nqubits : int
        Number of physical qubits
    seed : int | None
        Random seed used for PRNG

    Returns
    -------
    QuantumCircuit
    """
    # Quantum register for physical qubits
    qr = QuantumRegister(nqubits, name="x")

    qc = QuantumCircuit(qr, name="error channel")

    if seed is None:
        seed = np.random.randint(0, np.iinfo(np.int32).max)
    rng = np.random.default_rng(seed)

    # For each physical qubit, randomly and independently apply each
    # Pauli gate with probability p, so that each physical qubit has
    # probability 1-3*p of having no error
    for i in range(nqubits):
        random_tuple = rng.random(3)
        if random_tuple[0] < p:
            qc.x(qr[i])
        if random_tuple[1] < p:
            qc.y(qr[i])
        if random_tuple[2] < p:
            qc.z(qr[i])

    return qc

def measure_syndromes() -> QuantumCircuit:
    """Returns the quantum circuit for measuring syndromes of the
    five-qubit error correcting code.
    """
    logical_state = QuantumRegister(5, name="x")

    # Quantum register for syndromes
    syndromes_qr = AncillaRegister(4, name="checks")

    # Classical register for measuring syndromes
    syndromes_cr = ClassicalRegister(4, name="s")

    qc = QuantumCircuit(logical_state,
                        syndromes_qr,
                        syndromes_cr,
                        name="syndrome measurement")

    # Generators for the stabilizer are
    # XZZXI, IXZZX, XIXZZ, ZXIXZ
    pass

def error_correction() -> QuantumCircuit:
    """Returns the quantum circuit that applies recovery operations
    based on the measured syndromes.
    """
    logical_state = QuantumRegister(5, name="x")

    # Classical register for measured syndromes
    syndromes_cr = ClassicalRegister(4, name="s")

    qc = QuantumCircuit(logical_state,
                        syndromes_cr,
                        name="recovery operations")
    pass
