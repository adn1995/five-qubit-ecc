# five-qubit-ecc
Five-qubit error correcting code with random Pauli error

A collaboration between Amanda Curtis and Arthur Diep-Nguyen

### Motivation

In both classical and quantum computing, there is a risk of some type of error corrupting or obscuring the information that is vital for the task at hand. With classical computing, the main type of error one might anticipate is a 'bit flip error', involving a number of bits being switched from 0 to 1 or vice-versa. Extensive work has been done on ways to detect and correct for these errors. 

With quantum computing, the potential sources of error are greater in number and the persuit of error correcting code is still in its early stages.  

As discussed in Section 10.5.6 of *Quantum Computation and Quantum Information* by Nielsen and Chuang (hereby referred as N&C), the five qubit error correcting code is the smallest size quantum code encoding a single logical qubit that can detect and correct any error on any single physical qubit in the encoded state.


### Building Blocks and Outline 

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


