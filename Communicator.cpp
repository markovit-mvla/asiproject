/**
 * @author tohar
 * @brief communicator class for quantum key transfer endpoints
*/

#include <iostream>
#include "Communicator.hpp"

template<typename T>
Communicator<T>::Communicator(int nQubits, std::string s) {
    bases_states = std::make_unique<typename Communicator<T>::bases_states_T>(static_cast<size_t>(nQubits));
    key = std::make_unique<typename Communicator<T>::key_T>(static_cast<size_t>(nQubits));
    name = s;
}

template<typename T>
void Communicator<T>::display() {
    using namespace std;
    auto n = static_cast<idx>(bases_states->size());
    const Communicator<T>::bases_states_T states = (*bases_states);
    cout << name << "'s states:    ";
    for (idx i = 0; i < n; ++i) {
        std::string state;
        if (states[i].first == 0)
            state = std::to_string((*bases_states)[i].second);
        else 
            state = states[i].second == 0 ? "+" : "-";
        std::cout << state << ' ';
    }
    cout << "\n";
    cout << name << "'s bases:    ";
    for (idx i = 0; i < n; ++i)
        cout << (states[i].first == 0 ? 'Z' : 'X') << ' ';
    cout << "\n";
}

template<typename T>
typename Communicator<T>::key_T Communicator<T>::get_key() {
    auto n = static_cast<idx>(bases_states->size());
    const Communicator<T>::bases_states_T states = (*bases_states);
    Communicator<T>::key_T result(n);
    for (idx i = 0; i < n; ++i)
        result[i] = states[i].second;
    return result;
}

template<typename T>
Communicator<T>::~Communicator() {
    bases_states.reset();
    key.reset();
}