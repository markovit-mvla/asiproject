#!/usr/bin/python3

# Standard Imports

import os
import time
import warnings
import random

# Installs

os.system("pip install colorama")
os.system("pip3 install colorama")
os.system("pip install qiskit")
os.system("pip3 install qiskit")
os.system("pip install qiskit-ibmq-provider")
os.system("pip3 install qiskit-ibmq-provider")
os.system("clear")

# Imports

from qiskit import IBMQ, QuantumCircuit, Aer, execute, \
	QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_bloch_multivector
from qiskit.circuit.random import random_circuit
from qiskit.tools import job_monitor
from colorama import Fore

# Configs

warnings.filterwarnings("ignore")
# IBMQ.save_account('523b6817788914242ceb116ea37ad233af538d961434929fdcee0a827153ab2d612bbf3d1c01865d532a87c114349fe741203c800d346a8f81ca34960c857f96')
provider = IBMQ.load_account()

# Start

s = Fore.GREEN+"""

ASI Research Project by Tohar Markovich
\"Applications of topological quantum computation in improving novel cryptographic algorithms and protocols\"

"""

def main():
	init_screen()
	print("""
1. BB84
2. E91
3. My algorithm
	""")
	choice = int(input("Pick a quantum cryptographic protocol: "))
	s = input("Enter a string to secure: ")
	match choice:
		case 1:
			algo_BB84(s)
		case 2: 
			algo_E91(s)
		case _:
			my_algo(s)

def init_screen():
	print(s)
	i = random.randint(1, 9)
	qc = QuantumCircuit(i, i)
	qc.x(1)
	qc.h(range(i))
	qc.cx(0, 1)
	qc.measure(range(i), range(i))
	print(qc)
	
def algo_BB84(s):
	return

def algo_E91(s):
	return

def my_algo(s):
	return

if __name__ == '__main__':
	main()
