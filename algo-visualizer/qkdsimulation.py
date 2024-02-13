#!/usr/bin/python3

import os
import time
import warnings
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
from qiskit_aer.noise import NoiseModel, amplitude_damping_error

import numpy as np

# Model

Aer._allow_object_storage = True

def BB84(n, with_eavesdropper, with_losses, 
        with_perturbations, with_sop_uncertainty, 
        source_generation_rate, fiber_length, 
        fiber_loss, detector_efficiency, 
        perturb_probability, sop_mean_deviation):
    start = time.time()
    time_interval = 1 / source_generation_rate
    if not with_losses:
        fiber_length = 0 
        fiber_loss = 0
    
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
            if with_perturbations and perturb_probability > np.random.random():
                alice_table.append('Z')
                time.sleep(time_interval)
                continue
            else:
                alice.h(qr[index])
                alice_table.append('X')
                time.sleep(time_interval)
        else:
            alice_table.append('Z')
            time.sleep(time_interval)
    
    # Need to send Alice's output state to Bob
    bob = QuantumCircuit(qr, cr, name='Bob')
    SendState(alice, bob, qr, fiber_length, fiber_loss)

    bob_table = []
    for index in range(len(qr)):
        if 0.5 < np.random.random(): # 50% chance
            if with_perturbations and perturb_probability > np.random.random():
                bob_table.append('Z')
                time.sleep(time_interval)
                continue
            else:
                bob.h(qr[index])
                bob_table.append('X')
                time.sleep(time_interval)
        else:
            bob_table.append('Z')
            time.sleep(time_interval)

    # Measure all qubits
    for index in range(len(qr)):
        bob.measure(qr[index], cr[index])

    # Execute quantum circuit
    backend = BasicAer.get_backend('qasm_simulator')
    result = execute(bob, backend=backend, shots=1).result()

    bob_key = list(result.get_counts(bob))[0]
    bob_key = bob_key[::-1] # Key is reversed so first qubit is the first element

    # Discard bits
    table_checks(alice_table, bob_table, alice_key, bob_key, with_eavesdropper, n, 1.0)
    
    if with_eavesdropper:
        eve = QuantumCircuit(qr, cr, name='Eve')
        SendState(alice, eve, qr, fiber_length, fiber_loss)

        eve_table = []
        for index in range(len(qr)):
            if 0.5 < np.random.random():
                if with_perturbations and perturb_probability > np.random.random():
                    eve_table.append('Z')
                    time.sleep(time_interval)
                    continue
                else:
                    eve.h(qr[index])
                    eve_table.append('X')
                    time.sleep(time_interval)
            else:
                eve_table.append('Z')
                time.sleep(time_interval)

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

        SendState(eve, bob, qr, fiber_length, fiber_loss)

        bob_table = []
        for index in range(len(qr)):
            if 0.5 < np.random.random():
                if with_perturbations and perturb_probability > np.random.random():
                    bob_table.append('Z')
                    time.sleep(time_interval)
                    continue
                else:
                    bob.h(qr[index])
                    bob_table.append('X')
                    time.sleep(time_interval)
            else:
                bob_table.append('Z')
                time.sleep(time_interval)

        for index in range(len(qr)):
            bob.measure(qr[index], cr[index])

        result = execute(bob, backend=backend, shots=1).result()

        bob_key = list(result.get_counts(bob))[0]
        bob_key = bob_key[::-1]

        # Normal check
        table_checks(alice_table, bob_table, alice_key, bob_key, with_eavesdropper, n, detector_efficiency)

        end = time.time()
        print('Time elapsed (s): ', end - start)

def table_checks(table1, table2, key1, key2, with_eavesdropper, n, detector_efficiency):
    keep = []
    discard = []
    for qubit, basis in enumerate(zip(table1, table2)):
        if detector_efficiency > np.random.random() and basis[0] == basis[1]:
            print("Same choice for qubit: {}, basis: {}" .format(qubit, basis[0])) 
            keep.append(qubit)
        else:
            print("Different choice for qubit: {}, Alice has {}, Bob has {}" .format(qubit, basis[0], basis[1]))
            discard.append(qubit)
    
    acc = 0
    for bit in zip(key1, key2):
        if bit[0] == bit[1] and detector_efficiency :
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

def SendState(qc1, qc2, qr, fiber_length, fiber_loss):
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

    noise_model = NoiseModel()
    damping_prob = 1 - np.exp(-fiber_loss)
    for qubit in qr:
        noise_model.add_quantum_error(amplitude_damping_error(damping_prob), ['id'], [qubit])
    
    qc2.noise_model = noise_model

#BB84(24, True, True, True, True, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

def TM99(n, with_eavesdropper, with_losses, 
        with_perturbations, with_sop_uncertainty, 
        source_generation_rate, source_efficiency, 
        fiber_length, fiber_loss, detector_efficiency, 
        perturb_probability, sop_mean_deviation):
    qr = QuantumRegister(n, name="qr")
    cr = ClassicalRegister(n, name="cr")

    alice = QuantumCircuit(qr, cr, name="Alice")
    bob = QuantumCircuit(qr, cr, name="Alice")

warnings.filterwarnings("ignore")
# IBMQ.save_account('523b6817788914242ceb116ea37ad233af538d961434929fdcee0a827153ab2d612bbf3d1c01865d532a87c114349fe741203c800d346a8f81ca34960c857f96')
# provider = IBMQ.load_account()

# View

class QuantumSimulatorApp:
    def __init__(self, root):
        self.system_parameters = []
        self.protocol = ""
        self.settings = {}
        self.num_qubits = 0
        self.qber_cross_check = 0

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

        self.entries = []

        for i, param in enumerate(params):
            label = ttk.Label(frame, text=param + ": ")
            label.grid(row=i, column=0, padx=5, pady=5, sticky="e")

            entry = ttk.Entry(frame)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")

            self.entries.append(entry)

        save_button = ttk.Button(frame, text="Submit System Parameters", command=self.save_data)
        save_button.grid(row=len(params), columnspan=2, padx=5, pady=10)

    def save_data(self):
        print("System parameters: ")
        for entry in self.entries:
            self.system_parameters.append(entry.get())
            print(entry.get())

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
        self.protocol_dropdown = ttk.Combobox(frame, values=protocol_values)
        self.protocol_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        self.protocol_dropdown.set(protocol_values[0])

        settings = ["Losses Enabled", "Perturbations Enabled", "Eavesdropping Enabled",
                    "SOP Uncertainty Enabled"]

        self.checkboxes = []

        for i, setting in enumerate(settings):
            checkbox = ttk.Checkbutton(frame, text=setting)
            checkbox.grid(row=i + 1, column=0, columnspan=2, padx=5, pady=2, sticky="w")
            self.checkboxes.append(checkbox)

        num_qubits_label = ttk.Label(frame, text="Number of Qubits: ")
        num_qubits_label.grid(row=len(settings) + 1, column=0, padx=5, pady=5, sticky="e")

        self.num_qubits_entry = ttk.Entry(frame) # num qubits
        self.num_qubits_entry.grid(row=len(settings) + 1, column=1, padx=5, pady=5, sticky="w")

        qber_label = ttk.Label(frame, text="QBER Cross-Check Fraction: ")
        qber_label.grid(row=len(settings) + 2, column=0, padx=5, pady=5, sticky="e")

        self.qber_entry = ttk.Entry(frame)
        self.qber_entry.grid(row=len(settings) + 2, column=1, padx=5, pady=5, sticky="w")

        save_button = ttk.Button(frame, text="Submit Simulation Settings", command=self.save_simulation_settings)
        save_button.grid(row=len(settings) + 3, columnspan=2, padx=5, pady=10)

    def save_simulation_settings(self):
        print("Simulation Settings: ")
        print("Protocol:", self.protocol_dropdown.get())
        self.protocol = self.protocol_dropdown.get();
        for checkbox in self.checkboxes:
            print(checkbox.cget("text"), checkbox.instate(['selected']))
            self.settings[checkbox.cget("text")] = checkbox.instate(['selected'])
        print("Number of Qubits:", self.num_qubits_entry.get())
        self.num_qubits = self.num_qubits_entry.get()
        print("QBER Cross-Check Fraction:", self.qber_entry.get())
        self.qber_cross_check = self.qber_entry.get()

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
        run_button.grid(row=0, column=2, columnspan=2, pady=10)

        view_button = ttk.Button(frame, text="View Sample", command=self.view_sample)
        view_button.grid(row=1, column=2, columnspan=2, pady=5, sticky="we")

    def run_simulation(self):
        if "BB84" == self.protocol:
            BB84(int(float(self.system_parameters[1])*int(self.num_qubits)), self.settings["Eavesdropping Enabled"], self.settings["Losses Enabled"], self.settings["Perturbations Enabled"], 
                self.settings["SOP Uncertainty Enabled"], float(self.system_parameters[0]), float(self.system_parameters[2]), float(self.system_parameters[3]), 
                float(self.system_parameters[4]), float(self.system_parameters[5]), float(self.system_parameters[6]))
            # Need to save the results either by returning them or saving in a variable
            # Need Key Length, Key Rate, and QBER
        elif "TM99" == self.protocol:
            TM99(self.num_qubits, self.settings["Eavesdropping Enabled"], self.settings["Losses Enabled"], self.settings["Perturbations Enabled"], 
                self.settings["SOP Uncertainty Enabled"], self.system_parameters[0], self.system_parameters[1], self.system_parameters[2], self.system_parameters[3], 
                self.system_parameters[4], self.system_parameters[5], self.system_parameters[6])
        else:
            print("Not enough data provided to run protocol")

    def view_sample(self):
        # Implement the logic for viewing the sample here
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = QuantumSimulatorApp(root)
    root.mainloop()