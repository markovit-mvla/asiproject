#include <cstdlib>

#include "Communicator.hpp"

int main() 
{
    idx n = 100; // Number of qubits Alice sends to Bob
    idx k = 30;  // Number of qubits that will be analyzed (approx. 1/3)
    Communicator<state_T, data_T>* Alice = new Communicator<state_T, data_T>(n, "Alice");
    Communicator<state_T, data_T>* Bob = new Communicator<state_T, data_T>("Bob");
    Communicator<state_T, data_T>* Eve = new Communicator<state_T, data_T>("Eve");
}