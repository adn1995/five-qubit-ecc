# filename: five_qubit_ecc.py
# authors: Amanda Curtis and Arthur Diep-Nguyen
"""This module contains Qiskit functions that construct quantum circuits
for implementing and testing the five-qubit error correcting code.
"""

from qiskit.circuit import (QuantumCircuit,
                            QuantumRegister,
                            AncillaRegister,
                            ClassicalRegister)

from qiskit_aer import AerSimulator
from qiskit import transpile

import numpy as np

########################################################################
########################################################################
# Main circuit
########################################################################
########################################################################

def main_circuit(x: bool = False,
                    p: float = 0,
                    seed: int | None = None) -> QuantumCircuit:
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

    # Apply errors
    if seed is None:
        seed = np.random.randint(0, np.iinfo(np.int32).max)
    qc.compose(error_channel(p, 5, seed).to_gate(),
                logical_state,
                inplace=True)

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
# Simulations
########################################################################
########################################################################

def simulate(x: bool = False,
                p: float = 0,
                seed: int | None = None,
                num_sims: int = 1000,
                simulator: AerSimulator | None = None) -> tuple[int]:
    """Returns the counts for correct and incorrect outputs when
    simulating the five qubit error correcting code.

    Parameters
    ----------
    x : bool
        Boolean that will be prepared into a logical state
    p : float
        Error probability for each physical qubit representing `x`
    seed : int | None
        Random seed used for PRNG
    num_sims : int
        Number of simulations
    simulator : AerSimulator
        Simulator on which the simulations are run

    Returns
    -------
    tuple[int]
        2-tuple where the 0th component is the number of correct
        outputs, and the 1st component is the number of incorrect
        outputs
    """
    if simulator == None:
        simulator = AerSimulator()
    counts = dict()

    for i in range(num_sims):
        # Compiling the circuit for every iteration of the for loop is
        # very inefficient, but is necessary because each compilation
        # randomizes the Pauli error channel.
        #
        # I had previously tried to use NoiseModel to model the random
        # Pauli error so that I could compile the circuit once and run
        # the simulation with shots=num_sims, but I couldn't figure out
        # how to get the NoiseModel to apply the error to the transpiled
        # circuit; I tried to get the NoiseModel to apply a random Pauli
        # error to every qubit of an empty gate with
        #   name="error channel"
        # but, to my understanding, the transpiler would simplify out
        # the `error-channel()`, so when it was time for the NoiseModel
        # to apply errors, there was no "error channel" gate on which to
        # apply errors, so no errors were applied.
        #
        # I'm still not sure how to get around those issues, so...
        # here we are.
        compiled_circuit = transpile(main_circuit(x, p, seed), simulator)
        job = simulator.run(compiled_circuit, shots=1)
        new_count = job.result().get_counts()
        for key in new_count:
            if key in counts:
                new_val = counts.get(key) + new_count.get(key)
                counts.update({key: new_val})
            else:
                counts.update({key: new_count.get(key)})

    # Components of logical state
    if x == False:
        correct_states = ("00000", "10010", "01001", "10100",
                            "01010", "11011", "00110", "11000",
                            "11101", "00011", "11110", "01111",
                            "10001", "01100", "10111", "00101")
    else:
        correct_states = ("11111", "01101", "10110", "01011",
                            "10101", "00100", "11001", "00111",
                            "00010", "11100", "00001", "10000",
                            "01110", "10011", "01000", "11010")

    correct_count = 0
    incorrect_count = 0

    for key in counts:
        if key[0:5] in correct_states:
            correct_count += counts.get(key)
        else:
            incorrect_count += counts.get(key)

    return (correct_count, incorrect_count)

def simulation_results(x: bool = False,
                probs: list[float] = [0.01, 0.05, 0.1],
                seed: int | None = None,
                num_sims: int = 1000,
                simulator: AerSimulator | None = None) -> dict[float, float]:
    """Returns dictionary of simulation results.

    Parameters
    ----------
    x : bool
        Boolean that will be prepared into a logical state
    probs : list[float]
        List of error probabilities
    seed : int | None
        Random seed used for PRNG
    num_sims : int
        Number of simulations
    simulator : AerSimulator
        Simulator on which the simulations are run

    Returns
    -------
    dict[float, float]
        The set of keys of this dictionary is `probs`, and the value for
        a given key is the simulated probability of a correct output.
    """
    results = dict()
    for p in probs:
        correct_count = simulate(x, p, seed, num_sims, simulator)[0]
        result = correct_count/num_sims
        results.update({p: result})

    return results
