# filename: five_qubit_ecc.py
# authors: Amanda Curtis and Arthur Diep-Nguyen
"""This module contains Qiskit functions that construct quantum circuits
for implementing and testing the five-qubit error correcting code.
"""

from qiskit.circuit import (QuantumCircuit,
                            QuantumRegister,
                            AncillaRegister,
                            ClassicalRegister)
import math
import random

########################################################################
########################################################################
# Finding the probability of success
########################################################################
########################################################################

def probability_of_success(x: bool, p: float) -> float:
    """Returns the probability that measuring the data qubits of the
    main circuit gives a component of the correct logical state.

    Parameters
    ----------
    x : bool
        Boolean that will be prepared into a logical state
    p : float
        Error probability for each physical qubit representing `x`

    Returns
    -------
    float
        Probability that measuring the data qubits of the
        `main_circuit(x,p)` gives a component of the correct logical
        state |x_L>
    """
    pass

########################################################################
########################################################################
# Main circuit
########################################################################
########################################################################

def main_circuit(x: bool, p: float) -> QuantumCircuit:
    """Returns a quantum circuit that implements and tests the
    five-qubit error correcting code.

    Parameters
    ----------
    x : bool
        Boolean that will be prepared into a logical state
    p : float
        Error probability for each physical qubit representing `x`

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

    # Should have a classical register for controlling the error channel
    # Randomly initialize the classical register, where each bit has
    # probability `p` of being initialized with 1
    controls = ClassicalRegister(15, name="x")

    # Should have a register for syndromes
    syndromes = AncillaRegister(4, name="s")
    pass

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
    pass

def error_channel(nqubits: int = 5) -> QuantumCircuit:
    """Returns a quantum circuit implementing a random Pauli error
    channel.

    Parameters
    ----------
    nqubits : int
        Number of physical qubits

    Returns
    -------
    QuantumCircuit
    """
    # Quantum register for physical qubits
    qr = QuantumRegister(nqubits, name="x")

    # Classical register for controlling Pauli gates
    # For each physical qubit, we should have 3 classical bits,
    # corresponding to the 3 Pauli gates
    cr = ClassicalRegister(3*nqubits, name="c")

    qc = QuantumCircuit(qr, cr, name="error channel")

    for i in range(nqubits):
        qc.cx(cr[i],qr[i])
        qc.cy(cr[nqubits+i], qr[i])
        qc.cz(cr[2*nqubits+i], qr[i])

    return qc

def measure_syndromes() -> QuantumCircuit:
    """Returns the quantum circuit for measuring syndromes of the
    five-qubit error correcting code.
    """
    pass

def error_correction() -> QuantumCircuit:
    """Returns the quantum circuit that applies recovery operations
    based on the measured syndromes.
    """
    pass
