import qiskit
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import Aer, execute
import math

def qinner(vec1, vec2, shots=20000, circ_show = False):
    if len(vec1) != len(vec2):
        raise ValueError('Lengths of states are not equal')
        
    N = len(vec1)
    nqubits = math.ceil(np.log2(N))
    
    vec1norm = np.linalg.norm(vec1)
    vec2norm = np.linalg.norm(vec2)
    
    vec1 = vec1/vec1norm
    vec2 = vec2/vec2norm
    
    circ = QuantumCircuit(nqubits+1,1)
    vec = np.concatenate((vec1,vec2))/np.sqrt(2)
    
    circ.initialize(vec, range(nqubits+1))
    circ.h(nqubits)
    circ.measure(nqubits,0)
    
    if circ_show == True:
        return circ.draw(output='mpl')

    backend = Aer.get_backend('qasm_simulator')
    job = execute(circ, backend, shots=shots)

    result = job.result()
    outputstate = result.get_counts(circ)

    if ('0' in outputstate.keys()):
        m_sum = float(outputstate["0"])/shots
    else:
        m_sum = 0
        
    return 2*m_sum-1

if __name__ == "__main__":
    x = np.arange(0,8,1)
    y = np.arange(100,108,1)


    qinner(x, y)
