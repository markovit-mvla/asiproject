#include <cstdlib>
#include <iostream>
#include <numeric>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

#include "../Dependencies/include/qpp.h"

using basis_T = short;
using state_T = short;
// (basis, state) pair collection type ; 0 -> Z basis, 1 -> X basis
using bases_states_T = std::vector<std::pair<basis_T, state_T>>;
using key_T = std::vector<short>;

// display Alice's and Bob's bases choices and states
void display(const bases_states_T& Alice_bases_states,
             const bases_states_T& Bob_bases_states);

// key sifting, removes the locations where the bases do not coincide
void sift(bases_states_T& Alice_bases_states, bases_states_T& Bob_bases_states);

// Alice and Bob sample a subset (of size k) of their qubits and estimate how
// much Eve eavesdropped; returns the number of positions where they disagree
qpp::realT sample(bases_states_T& Alice_bases_states,
                  bases_states_T& Bob_bases_states, qpp::idx k);

// compute the final key; technically, here is where we do error correction and
// privacy amplification; however, here we simply discard the bits that differ
key_T final(const key_T& Alice_raw_key, const key_T& Bob_raw_key);

// helper, retrieves the key from a collection of (basis, state) pairs
key_T get_key(const bases_states_T& bases_states);

int main() {
    using namespace qpp;
    
    idx n = 100;   // no. of qubits Alice sends to Bob
    idx k = 20;    // no. of qubits Alice and Bob check for eavesdropping
    realT p = 0.5; // probability of Eve intercepting (and altering) the qubits
    // when we should abort due to eavesdropping; lower in reality
    realT abort_rate = 0.2;

    std::cout << ">> E91, sending n = " << n
              << " qubits from Alice to Bob, k = " << k
              << " qubits are used for sampling (eavesdrop detection)\n";
    std::cout << ">> With probability p = " << p
              << ", Eve intercepts the qubits and randomly measures them in the"
                 " Z or X basis, then sends them to Bob\n";
    std::cout << ">> Excludes error correction and privacy amplification\n";

    // Actual E91 algorithm here
}

void display(const bases_states_T& Alice_bases_states,
             const bases_states_T& Bob_bases_states) {
    using namespace qpp;
    auto n = static_cast<idx>(Alice_bases_states.size());
    std::cout << "Alice's states:  ";
    for (idx i = 0; i < n; ++i) {
        std::string state;
        if (Alice_bases_states[i].first == 0) // Z basis
            state = std::to_string(Alice_bases_states[i].second);
        else // X basis
            state = Alice_bases_states[i].second == 0 ? "+" : "-";
        std::cout << state << ' ';
    }
    std::cout << '\n';
    std::cout << "Alice's bases:   ";
    for (idx i = 0; i < n; ++i)
        std::cout << (Alice_bases_states[i].first == 0 ? 'Z' : 'X') << ' ';
    std::cout << '\n';
    std::cout << "Bob's bases:     ";
    for (idx i = 0; i < n; ++i)
        std::cout << (Bob_bases_states[i].first == 0 ? 'Z' : 'X') << ' ';
    std::cout << '\n';
    std::cout << "Bob's states:    ";
    for (idx i = 0; i < n; ++i) {
        std::string state;
        if (Bob_bases_states[i].first == 0) // Z basis
            state = std::to_string(Bob_bases_states[i].second);
        else // X basis
            state = Bob_bases_states[i].second == 0 ? "+" : "-";
        std::cout << state << ' ';
    }
    std::cout << '\n';
}

void sift(bases_states_T& Alice_bases_states, 
          bases_states_T& Bob_bases_states) {
    using namespace qpp;
    auto n = static_cast<idx>(Alice_bases_states.size());
    bases_states_T result_A, result_B;
    for (idx i = 0; i < n; ++i) {
        if (Alice_bases_states[i].first != Bob_bases_states[i].first)
            continue;
        result_A.emplace_back(Alice_bases_states[i]);
        result_B.emplace_back(Bob_bases_states[i]);
    }
    Alice_bases_states = result_A;
    Bob_bases_states = result_B;
}

qpp::realT sample(bases_states_T& Alice_bases_states, 
                  bases_states_T& Bob_bases_states) {
    using namespace qpp;
    auto n = static_cast<idx>(Alice_bases_states.size());

    if (k > n) {
        std::cout << ">> Not enough check qubits (k too large), aborting...\n";
        exit(EXIT_FAILURE);
    }

    std::vector<idx> pos(n);
    std::iota(pos.begin(), pos.end(), 0);
    auto& gen =
#ifdef NO_THREAD_LOCAL_
        RandomDevices::get_instance().get_prng();
#else
        RandomDevices::get_thread_local_instance().get_prng();
#endif
    // first k elements label the qubits we want to check
    std::shuffle(pos.begin(), pos.end(), gen);
    // sort (first k of them) for std::binary_search() later
    std::sort(pos.begin(), std::next(pos.begin(), k));

    bases_states_T result_A, result_B;
    idx cnt = 0; // how many bits differ
    for (idx i = 0; i < n; ++i) {
        // is current position part of the ones Alice and Bob need to check?
        if (std::binary_search(pos.begin(), std::next(pos.begin(), k), i)) {
            auto basis_AB = Alice_bases_states[i].first;
            auto state_A = Alice_bases_states[i].second;
            auto state_B = Bob_bases_states[i].second;

            ket psi_A = (state_A == 0) ? 0_ket : 1_ket;
            ket psi_B = (state_B == 0) ? 0_ket : 1_ket;
            cmat U = gt.Z;     // measurement basis
            if (basis_AB != 0) // if X basis
            {
                U = gt.H;
                psi_A = gt.H * psi_A;
                psi_B = gt.H * psi_B;
            }

            auto measure_A = measure(psi_A, U);
            auto m_A = std::get<RES>(measure_A); // Alice's measurement result

            auto measure_B = measure(psi_B, U);
            auto m_B = std::get<RES>(measure_B); // Bob's measurement result

            if (m_A != m_B)
                ++cnt;
        } else {
            result_A.emplace_back(Alice_bases_states[i]);
            result_B.emplace_back(Bob_bases_states[i]);
        }
    }
    Alice_bases_states = result_A;
    Bob_bases_states = result_B;

    return static_cast<realT>(cnt) / static_cast<realT>(k);
}

key_T final(const key_T& Alice_raw_key, const key_T& Bob_raw_key) {
    using namespace qpp;
    auto n = static_cast<idx>(Alice_raw_key.size());
    key_T result;
    for (idx i = 0; i < n; ++i) {
        if (Alice_raw_key[i] != Bob_raw_key[i])
            continue;
        result.emplace_back(Alice_raw_key[i]);
    }
    return result;
}

key_T get_key(const bases_states_T& bases_states) {
    using namespace qpp;
    auto n = static_cast<idx>(bases_states.size());
    key_T result(n);
    for (idx i = 0; i < n; ++i)
        result[i] = bases_states[i].second;
    return result;
}