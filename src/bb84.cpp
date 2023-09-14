/**
 * @author tohar
 * @brief bb84 quantum key transfer algorithm 
*/

#include <cstdlib>

#include "include/Communicator.hpp"

using state_T = short;            // State index type
using basis_T = short;            // Basis type
using data_T = std::string;       // Type of Qubit data

template<typename T, typename K>
void sift(const Communicator<T, K>* alice, const Communicator<T, K>* bob);

template<typename T, typename K>
qpp::realT 
sample(Communicator<T, K>* alice, Communicator<T, K>* bob, 
    qpp::idx k);

template<typename T, typename K>
auto final(const Communicator<T, K>* alice, const Communicator<T, K>* bob, 
    qpp::idx k);

template<typename T, typename K>
inline void display(const Communicator<T, K>* alice, const Communicator<T, K>* bob);

int main() 
{
    using namespace qpp;

    idx n = 100;   // no. of qubits Alice sends to Bob
    idx k = 20;    // no. of qubits Alice and Bob check for eavesdropping
    realT p = 0.5; // probability of Eve intercepting (and altering) the qubits
    // when we should abort due to eavesdropping; lower in reality
    realT abort_rate = 0.2;

    std::cout << ">> BB84, sending n = " << n
              << " qubits from Alice to Bob, k = " << k
              << " qubits are used for sampling (eavesdrop detection)\n";
    std::cout << ">> With probability p = " << p
              << ", Eve intercepts the qubits and randomly measures them in the"
                 " Z or X basis, then sends them to Bob\n";
    std::cout << ">> Excludes error correction and privacy amplification\n";

    Communicator<state_T, data_T>* alice = new Communicator<state_T, data_T>(n, "Alice");
    Communicator<state_T, data_T>* bob = new Communicator<state_T, data_T>("Bob");
    Communicator<state_T, data_T>* eve = new Communicator<state_T, data_T>("Eve");

    auto alice_bases_states = alice->get_bases_states();
    for (auto& elem : alice_bases_states) {
        // chose a random basis, 0 -> Z basis, 1 -> X basis
        basis_T basis = bernoulli() ? 0 : 1;
        // chose a random state, |0> or |1> in the basis 'basis'
        state_T state = bernoulli() ? 0 : 1;
        elem = std::make_pair(basis, state);
    }

    auto bob_bases_states = bob->get_bases_states();
    for (auto& elem : bob_bases_states) {
        // chose a random basis, 0 -> Z basis, 1 -> X basis
        basis_T basis = bernoulli() ? 0 : 1;
        elem.first = basis;
    }

    // Alice "prepares" the qubits and "sends" them to Bob one by one
    // Eve is in the middle and intercepts/resends the qubits with
    // probability p Bob measures the received qubits one by one
    for (idx i = 0; i < n; ++i) {
        auto basis_A = alice_bases_states[i].first;
        auto state_A = alice_bases_states[i].second;
        ket psi = (state_A == 0) ? 0_ket : 1_ket;
        if (basis_A != 0) // if X basis
            psi = gt.H * psi;

        // Eve intercepts the qubit and randomly measures it in the Z or X
        // basis, then sends it to Bob
        if (bernoulli(p)) {
            // chose a random basis, 0 -> Z basis, 1 -> X basis
            basis_T basis_E = bernoulli();
            cmat U_E = (basis_E == 0) ? gt.Z : gt.H;
            auto measure_E = measure(psi, U_E);
            auto m_E = std::get<RES>(measure_E); // measurement result
            psi = std::get<ST>(measure_E)[m_E];  // update the state accordingly
        }

        // Bob measures the qubit Eve re-sent
        auto basis_B = bob_bases_states[i].first;
        // Bob's measurement eigenvectors
        cmat U_B = (basis_B == 0) ? gt.Z : gt.H;
        auto measure_B = measure(psi, U_B);
        auto m_B = std::get<RES>(measure_B); // measurement result
        bob_bases_states[i].second = static_cast<state_T>(m_B);
    }

    // display the results before bases sifting
    std::cout << ">> Before sifting\n";
    display(alice, bob);

    // sift on same bases
    sift(alice, bob);
    auto sifted_key_size = alice_bases_states.size();

    // display the results after bases sifting
    std::cout << ">> After sifting\n";
    display(alice, bob);

    // check eavesdropping (sampling)
    auto eves_rate = sample(alice, bob, k);
    auto raw_key_size = alice_bases_states.size();
    std::cout << ">> Sampling k = " << k << " qubits...\n";
    std::cout << ">> Detected eavesdropping rate: " << eves_rate << '\n';
    // if rate is too high we should abort here
    if (eves_rate > abort_rate) {
        std::cout
            << ">> Detected eavesdropping rate is too high, aborting...\n";
        return EXIT_FAILURE;
    }

    // display the results after basis sifting and eavesdropping detection
    std::cout << ">> After sifting and eavesdrop detection (raw keys)\n";
    display(alice, bob);

    std::cout << ">> Established keys\n";
    // display the raw final_key on Alice's side
    auto raw_key_A = alice->get_key();
    std::cout << "Alice's raw key: " << disp(raw_key_A, " ", "", "") << '\n';

    // display the raw final_key on Bob's side
    auto raw_key_B = bob->get_key();
    std::cout << "Bob's raw key:   " << disp(raw_key_B, " ", "", "") << '\n';

    // display the final final_key and the corresponding rate
    auto final_key = final(alice, bob, k);
    auto final_key_rate =
        static_cast<realT>(final_key.size()) / static_cast<realT>(n);
    std::cout << "Final key:       " << disp(final_key, " ", "", "") << '\n';
    std::cout << ">> Bits/keys sizes: " << n << '/' << sifted_key_size << '/'
              << raw_key_size << '/' << final_key.size() << '\n';
    std::cout << ">> Final key rate: " << final_key_rate << '\n';
}

template<typename T, typename K>
inline void display(const Communicator<T, K>* alice, const Communicator<T, K>* bob) {
    alice->display();
    bob->display();
}

template<typename T, typename K>
void sift(const Communicator<T, K>* alice, const Communicator<T, K>* bob) {
    using namespace qpp;
    auto n = static_cast<idx>(alice_bases_states.size());
    auto alice_bases_states = alice->get_bases_states();
    auto bob_bases_states = bob->get_bases_states();
    typename Communicator<T, K>::bases_states_T result_A, result_B;
    for (idx i = 0; i < n; ++i) {
        if (alice_bases_states[i].first != bob_bases_states[i].first)
            continue;
        result_A.emplace_back(alice_bases_states[i]);
        result_B.emplace_back(bob_bases_states[i]);
    }
    alice_bases_states = result_A;
    bob_bases_states = result_B;
}

template<typename T, typename K>
qpp::realT
sample(Communicator<T, K>* alice, Communicator<T, K>* bob, 
    qpp::idx k) {
    using namespace qpp;
    auto n = static_cast<idx>(alice_bases_states.size());
    auto alice_bases_states = alice->get_bases_states();
    auto bob_bases_states = bob->get_bases_states();

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

    typename Communicator<T, K>::bases_states_T result_A, result_B;
    idx cnt = 0; // how many bits differ
    for (idx i = 0; i < n; ++i) {
        // is current position part of the ones Alice and Bob need to check?
        if (std::binary_search(pos.begin(), std::next(pos.begin(), k), i)) {
            auto basis_AB = alice_bases_states[i].first;
            auto state_A = alice_bases_states[i].second;
            auto state_B = bob_bases_states[i].second;

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
            result_A.emplace_back(alice_bases_states[i]);
            result_B.emplace_back(bob_bases_states[i]);
        }
    }
    alice_bases_states = result_A;
    bob_bases_states = result_B;

    return static_cast<realT>(cnt) / static_cast<realT>(k);
}

template<typename T, typename K>
auto final(const Communicator<T, K>* alice, const Communicator<T, K>* bob, 
    qpp::idx k) {
    using namespace qpp;
    auto n = static_cast<idx>(alice_raw_key.size());
    auto alice_raw_key = alice->get_key();
    auto bob_raw_key = bob->get_key();
    typename Communicator<T, K>::key_T result;
    for (idx i = 0; i < n; ++i) {
        if (alice_raw_key[i] != bob_raw_key[i]) 
            continue;
        result.emplace_back(alice_raw_key[i]);
    }
    return result;
}