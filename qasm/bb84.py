from qiskit import QuantumCircuit, Aer, transpile, assemble

qc = QuantumCircuit.from_qasm_file('bb84.qasm')
backend = Aer.get_backend('qasm_simulator')
transpiled_qc = transpile(qc, backend)
qobj = assemble(transpiled_qc)
result = backend.run(qobj).result()
counts = result.get_counts()
print(counts)