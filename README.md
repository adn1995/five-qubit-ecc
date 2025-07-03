# five-qubit-ecc
Five-qubit error correcting code with random Pauli error

A collaboration between Amanda Curtis and Arthur Diep-Nguyen

### Motivation

In both classical and quantum computing, there is a risk of some type of error corrupting or obscuring the information that is vital for the task at hand, whether that task is sending code through a channel or storing it. With classical computing, the main type of error one might anticipate is a 'bit flip error', involving a number of bits being switched from 0 to 1 or vice-versa. Extensive work has been done on ways to detect and correct for these errors in the classical setting. 

With quantum computing, the potential sources of error are greater in number. Along with a number of other differences between classical and quantum information, this means the approach taken for error correction will be a bit different. While there are a vast number of type of quantum error correcting codes, we focus this investigation focuses on the implementation of the five qubit error correcting code.   

As discussed in Section 10.5.6 of *Quantum Computation and Quantum Information* by Nielsen and Chuang (hereby referred as N&C), the five qubit error correcting code is the smallest size quantum code encoding a single logical qubit that can detect and correct any error on any single physical qubit in the encoded state. It is useful in several applications.


### Building Blocks and Outline 

In our notebook and accompyning file, we create a quantum circuit that prepares (not neceassarily fault tolerantly) the logical state $|x_L>$ for the 5-qubit code, runs it through a random Pauli error channel (with error rate p for each of the qubits), measures the syndromes, applies the recovery operations (if needed), and measures the data qubits.

We also assess the success probability and visualize the dependence of the success probability for various values of p.

1. Basic explanation of the five qubit error correcting code
2. State preparation
3. Random Pauli error
4. Measuring syndromes
5. Applying recovery operations
6. Simulating the entire circuit with various error probabilities
7. References

### Sources 

Our sources are also listed in section 6 of the Jupyter notebook. 

### Points of Contact 

- Amanda Curtis - dr.curtis.math (at) gmail (dot) com
- Arthur Diep-Nguyen - arthur (at) math (dot) ucsb (dot) edu


