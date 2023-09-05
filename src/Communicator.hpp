#pragma once

#ifndef COMMUNICATOR_HPP
#define COMMUNICATOR_HPP

#include <vector>
#include <tuple>
#include <string>
#include <utility>
#include <memory>

#include "Qubit.hpp"
#include "Photon.h"
#include "util.h"

// T - type of bases states
// K - type of Qubit data to encode
template<typename T, typename K>
class Communicator {
    private:
        using bases_states_T = std::vector<std::pair<T, T>>;
        using key_T = std::vector<T>;
        using channel_T = std::vector<std::pair<Qubit<K>, Photon>>;
        std::unique_ptr<bases_states_T> bases_states;
        std::unique_ptr<key_T> key;
        std::shared_ptr<channel_T> channel;
        std::string name;
    public:   
        inline Communicator(int nQubits, std::string s);
        inline Communicator(std::string s);
        void display();
        inline void send(Qubit<K> qubit, Photon photon, Communicator<T, K> &endpoint);
        key_T get_key();
        inline ~Communicator();
};

#endif