#ifndef COMMUNICATOR_HPP
#define COMMUNICATOR_HPP

#include <vector>
#include <tuple>
#include <string>
#include <utility>
#include <memory>

#include "Qubit.hpp"
#include "Photon.h"
#include "../dependencies/qpp/include/qpp.h"

// T - type of bases states
// K - type of Qubit data to encode
template<typename T, typename K>
class Communicator {
    private:
        using bases_states_T = std::vector<std::pair<T, T>>;
        using key_T = std::vector<T>;
        using channel_T = std::vector<std::pair<Qubit<K>, Photon>>; 
        std::unique_ptr<Communicator<T, K>::bases_states_T> bases_states; // States for entanglement & transformations
        std::unique_ptr<Communicator<T, K>::key_T> key;                   // List of bit string keys
        static std::shared_ptr<Communicator<T, K>::channel_T> channel;    // Channel itself for communication
        std::string name;                                                 // Name of Communicator
    public:    
        inline Communicator(int nQubits, std::string s);
        inline Communicator(std::string s);
        void display();
        inline void send(Qubit<K> qubit, Photon photon, Communicator<T, K> &endpoint);
        key_T get_key();
        inline bases_states_T get_bases_states();
        inline ~Communicator();
};

#endif