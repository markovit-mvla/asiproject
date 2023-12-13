#!/usr/bin/python3

import os
import time
import warnings
import random
import re

os.system("pip install tk");
os.system("pip install qiskit")
os.system("pip3 install qiskit")
os.system("pip install qiskit-ibmq-provider")
os.system("pip3 install qiskit-ibmq-provider")
os.system("clear")

import tkinter as tk
from tkinter import *
from tkinter import ttk

from qiskit import IBMQ, QuantumCircuit, Aer, execute, \
	QuantumRegister, ClassicalRegister, BasicAer
from qiskit.tools.visualization import circuit_drawer, plot_histogram, plot_bloch_multivector

import numpy as np

# Model

Aer._allow_object_storage = True

def BB84(n, with_eavesdropper, with_losses, 
        with_perturbations, with_sop_uncertainty):
    qr = QuantumRegister(n, name='qr')
    cr = ClassicalRegister(n, name='cr')

    alice = QuantumCircuit(qr, cr, name='Alice') # Alice's Circuit
    alice_key = np.random.randint(0, high=2**n) # Gen random number in available range of Qubits
    alice_key = np.binary_repr(alice_key, n) # Cast key to binary for encoding

    # Encode key as alice qubits
    for index, digit in enumerate(alice_key):
        if digit == '1':
            alice.x(qr[index]) # If key has '1', change state to |1>
        
    # Apply rotation to half of qubits, switching randomly on diagonal basis
    alice_table = []
    for index in range(len(qr)):
        if 0.5 < np.random.random(): # 50% chance
            alice.h(qr[index])
            alice_table.append('X')
        else:
            alice_table.append('Z')
    
    # Need to send Alice's output state to Bob
    bob = QuantumCircuit(qr, cr, name='Bob')
    SendState(alice, bob, qr)

    bob_table = []
    for index in range(len(qr)):
        if 0.5 < np.random.random(): # 50% chance
            bob.h(qr[index])
            bob_table.append('X')
        else:
            bob_table.append('Z')

    # Measure all qubits
    for index in range(len(qr)):
        bob.measure(qr[index], cr[index])

    # Execute quantum circuit
    backend = BasicAer.get_backend('qasm_simulator')
    result = execute(bob, backend=backend, shots=1).result()

    bob_key = list(result.get_counts(bob))[0]
    bob_key = bob_key[::-1] # Key is reversed so first qubit is the first element

    # Discard bits
    table_checks(alice_table, bob_table, alice_key, bob_key, with_eavesdropper, n)
    
    if with_eavesdropper:
        eve = QuantumCircuit(qr, cr, name='Eve')
        SendState(alice, eve, qr)

        eve_table = []
        for index in range(len(qr)):
            if 0.5 < np.random.random():
                eve.h(qr[index])
                eve_table.append('X')
            else:
                eve_table.append('Z')

        for index in range(len(qr)):
            eve.measure(qr[index], cr[index])
        
        backend = BasicAer.get_backend('qasm_simulator')
        result = execute(eve, backend=backend, shots=1).result()

        eve_key = list(result.get_counts(eve))[0]
        eve_key = eve_key[::-1]

        for qubit, basis in enumerate(zip(alice_table, eve_table)):
            if basis[0] == basis[1]:
                print("Same choice for qubit: {}, basis: {}" .format(qubit, basis[0]))
            else:
                print("Different choice for qubit: {}, Alice has {}, Eve has {}" .format(qubit, basis[0], basis[1]))
                if eve_key[qubit] == alice_key[qubit]:
                    eve.h(qr[qubit])
                else:
                    if basis[0] == 'X' and basis[1] == 'Z':
                        eve.h(qr[qubit])
                        eve.x(qr[qubit])
                    else:
                        eve.x(qr[qubit])
                        eve.h(qr[qubit])

        SendState(eve, bob, qr)

        bob_table = []
        for index in range(len(qr)):
            if 0.5 < np.random.random():
                bob.h(qr[index])
                bob_table.append('X')
            else:
                bob_table.append('Z')

        for index in range(len(qr)):
            bob.measure(qr[index], cr[index])

        result = execute(bob, backend=backend, shots=1).result()

        bob_key = list(result.get_counts(bob))[0]
        bob_key = bob_key[::-1]

        # Normal check
        table_checks(alice_table, bob_table, alice_key, bob_key, with_eavesdropper, n)

def table_checks(table1, table2, key1, key2, with_eavesdropper, n):
    keep = []
    discard = []
    for qubit, basis in enumerate(zip(table1, table2)):
        if basis[0] == basis[1]:
            print("Same choice for qubit: {}, basis: {}" .format(qubit, basis[0])) 
            keep.append(qubit)
        else:
            print("Different choice for qubit: {}, Alice has {}, Bob has {}" .format(qubit, basis[0], basis[1]))
            discard.append(qubit)
    
    acc = 0
    for bit in zip(key1, key2):
        if bit[0] == bit[1]:
            acc += 1
    
    print('Percentage of qubits to be discarded according to table comparison: ', len(keep)/n)
    print('Measurement convergence by additional chance: ', acc/n)   

    new_alice_key = [key1[qubit] for qubit in keep]
    new_bob_key = [key2[qubit] for qubit in keep]

    acc = 0
    for bit in zip(new_alice_key, new_bob_key):
        if bit[0] == bit[1]:
            acc += 1 
    
    print('Percentage of similarity between the keys: ', acc/len(new_alice_key))   

    if (acc//len(new_alice_key) == 1):
        print("Key exchange has been successfull")
        print("New Alice's key: ", new_alice_key)
        print("New Bob's key: ", new_bob_key)
    else:
        if with_eavesdropper:
            print("Key exchange has been tampered! Check for eavesdropper or try again")
        else:
            print("Key exchange has been tampered! Try again")
        print("New Alice's key is invalid: ", new_alice_key)
        print("New Bob's key is invalid: ", new_bob_key)

def SendState(qc1, qc2, qr):
    ''' 
    * Function takes output of qc1 and initializes qc2 with the same state
    '''

    # Retrieve quantum state from qc1 qasm code
    qs = qc1.qasm().split(sep=";")[4:-1]

    for index, instruction in enumerate(qs):
        qs[index] = instruction.lstrip()
    
    for instruction in qs:
        if instruction[0] == 'x':
            old_qr = int(instruction[5:-1])
            qc2.x(qr[old_qr])
        elif instruction[0] == 'h':
            old_qr = int(instruction[5:-1])
            qc2.h(qr[old_qr])
        elif instruction[0] == 'm': # Exclude measuring
            pass
        else:
            raise Exception('Unable to parse instruction')

BB84(24, True, True, True, True)

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

E91(24, False, True, True, True)

warnings.filterwarnings("ignore")
# IBMQ.save_account('523b6817788914242ceb116ea37ad233af538d961434929fdcee0a827153ab2d612bbf3d1c01865d532a87c114349fe741203c800d346a8f81ca34960c857f96')
# provider = IBMQ.load_account()

# View

class QuantumSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quantum Simulator")

        self.notebook = ttk.Notebook(root)

        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Single Simulation")

        # System Parameters
        self.create_system_parameters()

        # Simulation Settings
        self.create_simulation_settings()

        # Results
        self.create_results()

        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="Multiple Simulations")

        # Multiple Simulation Parameters
        self.create_multiple_system_parameters()

        self.notebook.pack(expand=1, fill="both")

    def create_system_parameters(self):
        frame = ttk.LabelFrame(self.tab1, text="System Parameters")
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        params = [
            "Source Generation Rate", "Source Efficiency", "Fiber Length",
            "Fiber Loss", "Detector Efficiency", "Perturb Probability",
            "SOP Mean Deviation"
        ]

        for i, param in enumerate(params):
            label = ttk.Label(frame, text=param + ": ")
            label.grid(row=i, column=0, padx=5, pady=5, sticky="e")

            entry = ttk.Entry(frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")

    def create_multiple_system_parameters(self):
        frame = ttk.LabelFrame(self.tab2, text="Parameters")
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        params = [
            "Select X-Parameter", "Select Y-Parameter", "Initial X", 
            "Final X", "Number of Points"
        ]

        for i, param in enumerate(params):
            label = ttk.Label(frame, text=param + ": ")
            label.grid(row=i, column=0, padx=5, pady=5, sticky="e")

            entry = ttk.Entry(frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")

    def create_simulation_settings(self):
        frame = ttk.LabelFrame(self.tab1, text="Simulation Settings")
        frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Dropdown for Protocol
        protocol_label = ttk.Label(frame, text="Protocol: ")
        protocol_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        protocol_values = ["BB84", "E91", "TM99"]
        protocol_dropdown = ttk.Combobox(frame, values=protocol_values)
        protocol_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        protocol_dropdown.set(protocol_values[0])

        settings = ["Losses Enabled", "Perturbations Enabled", "Eavesdropping Enabled",
                    "SOP Uncertainty Enabled"]

        for i, setting in enumerate(settings):
            checkbox = ttk.Checkbutton(frame, text=setting)
            checkbox.grid(row=i + 1, column=0, columnspan=2, padx=5, pady=2, sticky="w")

        num_qubits_label = ttk.Label(frame, text="Number of Qubits: ")
        num_qubits_label.grid(row=len(settings) + 1, column=0, padx=5, pady=5, sticky="e")

        num_qubits_entry = ttk.Entry(frame)
        num_qubits_entry.grid(row=len(settings) + 1, column=1, padx=5, pady=5, sticky="w")

        qber_label = ttk.Label(frame, text="QBER Cross-Check Fraction: ")
        qber_label.grid(row=len(settings) + 2, column=0, padx=5, pady=5, sticky="e")

        qber_entry = ttk.Entry(frame)
        qber_entry.grid(row=len(settings) + 2, column=1, padx=5, pady=5, sticky="w")

    def create_results(self):
        frame = ttk.LabelFrame(self.tab1, text="Results")
        frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        results = ["Key Length", "Key Rate", "QBER", "Combined Efficiency"]
        for i, result in enumerate(results):
            label = ttk.Label(frame, text=result + ": ")
            label.grid(row=i, column=0, padx=5, pady=5, sticky="e")

            empty_text = tk.StringVar()
            entry = ttk.Entry(frame, textvariable=empty_text, state="readonly")
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")

        run_button = ttk.Button(frame, text="Run Simulation", command=self.run_simulation)
        run_button.grid(row=len(results), column=0, columnspan=2, pady=10)

        view_button = ttk.Button(frame, text="View Sample", command=self.view_sample)
        view_button.grid(row=len(results) + 1, column=0, columnspan=2, pady=5)

    def run_simulation(self):
        # Implement the logic for running the simulation here
        pass

    def view_sample(self):
        # Implement the logic for viewing the sample here
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = QuantumSimulatorApp(root)
    root.mainloop()