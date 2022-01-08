import qiskit
import numpy as np
from numpy import array
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import Aer, execute
import math


def qinner(vec1: array, vec2: array, shots: int = 20000) -> array:    
    def qcomp(vec1: array, vec2: array, shots: int) -> array:
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

        backend = Aer.get_backend('qasm_simulator')
        job = execute(circ, backend, shots=shots)

        result = job.result()
        outputstate = result.get_counts(circ)

        if ('0' in outputstate.keys()):
            m_sum = float(outputstate["0"])/shots
        else:
            m_sum = 0

        return 2*m_sum-1

    transpose = False
    dim1 = vec1.shape[0]
    dim2 = vec2.shape[0]
    dimvec2 = len(vec2.shape)
    dimvec1 = len(vec1.shape)
    if dimvec1 == 1 and dimvec2 ==1:
        res = []
        res.append(qcomp(vec1, vec2, shots))    
    elif dimvec1 > 1 and dimvec2 == 1:
        res = []
        for i in range(dim1):
            res.append(qcomp(vec1[i], vec2, shots))
    elif dimvec2 > 1 and dimvec1 == 1:
        res = []
        for i in range(dim2):
            res.append(qcomp(vec1, vec2[i], shots))
    else:
        transpose = True
        res = []
        for j in range(dim2):
            temp = []
            for i in range(dim1):
                temp.append(qcomp(vec1[i], vec2[j], shots))
            res.append(temp)
    res = np.array(res)
    if transpose == False:
        return(res)
    else:
        return(np.transpose(res))


if __name__ == "__main__":
    x = np.arange(0,8,1)
    y = np.arange(100,108,1)


    print(qinner(x, y))


