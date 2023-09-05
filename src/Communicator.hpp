#pragma once

#ifndef COMMUNICATOR_HPP
#define COMMUNICATOR_HPP

#include <vector>
#include <tuple>
#include <string>
#include <utility>
#include <memory>

#include "util.h"

template<typename T>
class Communicator {
    private:
        using bases_states_T = std::vector<std::pair<T, T>>;
        using key_T = std::vector<T>;
        std::unique_ptr<bases_states_T> bases_states;
        std::unique_ptr<key_T> key;
        std::string name;
    public:   
        Communicator(int nQubits, std::string s);
        void display();
        key_T get_key();
        ~Communicator();
};

#endif