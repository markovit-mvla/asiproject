/**
 * @author tohar
 * @brief e91 quantum key transfer algorithm 
*/

#include <cstdlib>

#include "Communicator.hpp"

using state_T = short;
using basis_T = short;
using data_T = std::string;

template<typename T, typename K>
auto final(const Communicator<T, K>* alice, const Communicator<T, K>* bob, 
    qpp::idx k);

template<typename T, typename K>
inline void display(const Communicator<T, K>* alice, const Communicator<T, K>* bob);

int main()
{
    using namespace qpp;
    idx n = 100; // Number of qubits Alice sends to Bob
    Communicator<state_T, data_T>* Alice = new Communicator<state_T, data_T>(n, "Alice");
    Communicator<state_T, data_T>* Bob = new Communicator<state_T, data_T>("Bob");
    Communicator<state_T, data_T>* Eve = new Communicator<state_T, data_T>("Eve");
}