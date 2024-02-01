#ignore
def E91(n, with_eavesdropper, with_losses,
        with_perturbations, with_sop_uncertainty):
    qr = QuantumRegister(2, name='qr')
    cr = ClassicalRegister(4, name='cr')
    singlet = QuantumCircuit(qr, cr, name='singlet')
    singlet.x(qr[0])
    singlet.x(qr[1])
    singlet.h(qr[0])
    singlet.cx(qr[0], qr[1])
    
    ## Alice's Measurement Circuits

    # Measure X basis
    measureX = QuantumCircuit(qr, cr, name='measureX')
    measureX.h(qr[0])
    measureX.measure(qr[0], cr[0])

    # Measure W basis A2 Direction
    measureW2 = QuantumCircuit(qr, cr, name='measureW2')
    measureW2.s(qr[0])
    measureW2.h(qr[0])
    measureW2.t(qr[0])
    measureW2.h(qr[0])
    measureW2.measure(qr[0], cr[0])

    # Measure Standard Z basis A3 Direction
    measureZ3 = QuantumCircuit(qr, cr, name='measureZ3')
    measureZ3.measure(qr[0], cr[0])

    ## Bob's Measurement Circuits

    # Measure W basis B1 Direction
    measureW1 = QuantumCircuit(qr, cr, name='measureW1')
    measureW1.s(qr[1])
    measureW1.h(qr[1])
    measureW1.t(qr[1])
    measureW1.h(qr[1])
    measureW1.measure(qr[1], cr[1])

    # Measure Standard Z basis B2 Direction
    measureZ2 = QuantumCircuit(qr, cr, name='measureZ2')
    measureZ2.measure(qr[1], cr[1])

    # Measure V basis
    measureV = QuantumCircuit(qr, cr, name='measureV')
    measureV.s(qr[1])
    measureV.h(qr[1])
    measureV.tdg(qr[1])
    measureV.h(qr[1])
    measureV.measure(qr[1],cr[1])

    ## Resulting Measurements
    aliceMeasurements = [measureX, measureW2, measureZ3]
    bobMeasurements = [measureW1, measureZ2, measureV]

    aliceMeasurementChoices = [random.randint(1, 3) for i in range(n)] 
    bobMeasurementChoices = [random.randint(1, 3) for i in range(n)] 
    
    circuits = []
    for i in range(n):
        circuitName = str(i) + ':A' + str(aliceMeasurementChoices[i]) + '_B' + str(bobMeasurementChoices[i])
        circuitName = singlet + aliceMeasurements[aliceMeasurementChoices[i]-1] + bobMeasurements[bobMeasurementChoices[i]-1] 
        circuits.append(circuitName)

    backend=BasicAer.get_backend('qasm_simulator')
    result = execute(circuits, backend=backend, shots=1).result()  
    abPatterns = [
        re.compile('..00$'), # search for the '..00' output (Alice obtained -1 and Bob obtained -1)
        re.compile('..01$'), # search for the '..01' output
        re.compile('..10$'), # search for the '..10' output (Alice obtained -1 and Bob obtained 1)
        re.compile('..11$')  # search for the '..11' output
    ]

    aliceResults = [] # Alice's results (string a)
    bobResults = [] # Bob's results (string a')

    for i in range(n):
        res = list(result.get_counts(circuits[i]).keys())[0] # extract the key from the dict and transform it to str; execution result of the i-th circuit
        
        if abPatterns[0].search(res): # check if the key is '..00' (if the measurement results are -1,-1)
            aliceResults.append(-1) # Alice got the result -1 
            bobResults.append(-1) # Bob got the result -1
        if abPatterns[1].search(res):
            aliceResults.append(1)
            bobResults.append(-1)
        if abPatterns[2].search(res): # check if the key is '..10' (if the measurement results are -1,1)
            aliceResults.append(-1) # Alice got the result -1 
            bobResults.append(1) # Bob got the result 1
        if abPatterns[3].search(res): 
            aliceResults.append(1)
            bobResults.append(1)

# E91(24, False, True, True, True)