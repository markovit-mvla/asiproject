#!/usr/bin/python3

import os
import time
import warnings
import random

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
	QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_bloch_multivector
from qiskit.circuit.random import random_circuit
from qiskit.tools import job_monitor

# Model

Aer._allow_object_storage = True
circuit = QuantumCircuit(2, 2)

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
