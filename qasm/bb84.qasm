OPENQASM 2.0;
//defcalgrammar "openpulse";

//const float q0_freq = 5.0e9;

qreg q[1];    // Single qubit pulse
creg c[1]; // Classical bit for shared key

creg alice_basis[1];
creg bob_basis[1];

// Prepare qubit with random polarization 
reset q[0];
alice_basis[0] = random[2]; // Evaluated on random basis 
if (alice_basis[0] == 1) {
    h q[0];
}

// Send qubits
// Transfer qubits using specific frequency
u3(pi/2, 0, pi) q[0]; // pi/2 superposition pulse

// Measure sent qubits in a random polarization basis
reset c[0];
bob_basis[0] = random[2]
if (bob_basis[0] == 0) {
    // HV
    measure q[0] -> c[0];
} else {
    // AD
    h q[0];
    measure q[0] -> c[0];
}

// Communicate bases
reset c[0];
c[0] = alice_basis[0];

reset bob_basis[1];
bob_basis[0] = c[0];

// Discard qubits with different bases
if (alice_basis[0] == bob_basis[0]) {
    c[0] = c[0] ^ alice_basis[0];
}