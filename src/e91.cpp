#include <cstdlib>

#include "Communicator.hpp"

using state_T = short;
using data_T = std::string;

int main()
{
    using namespace qpp;
    idx n = 100; // Number of qubits Alice sends to Bob
    Communicator<state_T, data_T>* Alice = new Communicator<state_T, data_T>(n, "Alice");
    Communicator<state_T, data_T>* Bob = new Communicator<state_T, data_T>("Bob");
    Communicator<state_T, data_T>* Eve = new Communicator<state_T, data_T>("Eve");
}