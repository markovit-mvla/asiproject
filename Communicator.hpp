#pragma once

#ifndef COMMUNICATOR_HPP
#define COMMUNICATOR_HPP

#include <vector>
#include <tuple>
#include <string>
#include <utility>
#include <memory>

#if defined(QPP_IDX_DEFAULT)
using idx = std::size_t;
#elif defined(QPP_IDX_SHORT)
using idx = short int;
#elif defined(QPP_IDX_INT)
using idx = int;
#elif defined(QPP_IDX_LONG)
using idx = long int;
#elif defined(QPP_IDX_LONG_LONG)
using idx = long long int;
#elif defined(QPP_IDX_USHORT)
using idx = unsigned short int;
#elif defined(QPP_IDX_UINT)
using idx = unsigned int;
#elif defined(QPP_IDX_ULONG)
using idx = unsigned long int;
#elif defined(QPP_IDX_ULONG_LONG)
using idx = unsigned long long int;
#else // build without CMake
using idx = std::size_t;
#endif
static_assert(std::is_integral_v<idx>, "Type must be integral");
static_assert(sizeof(idx) > 1, "Type must be at least 2 bytes long");

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