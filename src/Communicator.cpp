/**
 * @author tohar
 * @brief communicator class for quantum key transfer endpoints
*/

#include <iostream>

#include "Communicator.hpp"

template<typename T, typename K>
inline Communicator<T, K>::Communicator(int nQubits, std::string s) {
    auto n = static_cast<size_t>(nQubits);
    bases_states = std::make_unique<typename Communicator<T, K>::bases_states_T>(n);
    key = std::make_unique<typename Communicator<T, K>::key_T>(n);
    channel = std::make_shared<typename Communicator<T, K>::channel_T>();
    name = s;
}

template<typename T, typename K>
inline Communicator<T, K>::Communicator(std::string s) {
    name = s;
}

template<typename T, typename K>
void Communicator<T, K>::display() {
    using namespace std;
    auto n = static_cast<idx>(bases_states->size());
    const Communicator<T, K>::bases_states_T states = (*bases_states);
    cout << name << "'s states:    ";
    for (idx i = 0; i < n; ++i) {
        std::string state;
        if (states[i].first == 0)
            state = std::to_string(states[i].second);
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

template<typename T, typename K>
inline void Communicator<T, K>::send(Qubit<K> qubit, Photon photon, Communicator<T, K> &endpoint) {
    (*endpoint.channel).emplace_back(static_cast<std::pair<Qubit<K>, Photon>>(std::make_pair(qubit, photon)));
}

template<typename T, typename K>
typename Communicator<T, K>::key_T Communicator<T, K>::get_key() {
    auto n = static_cast<idx>(bases_states->size());
    const Communicator<T, K>::bases_states_T states = (*bases_states);
    Communicator<T, K>::key_T result(n);
    for (idx i = 0; i < n; ++i)
        result[i] = states[i].second;
    return result;
}

template<typename T, typename K>
inline Communicator<T, K>::~Communicator() {
    bases_states.reset();
    key.reset();
}