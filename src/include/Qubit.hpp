#ifndef QUBIT_HPP
#define QUBIT_HPP

#include <string>
#include <memory>

#include "util.h"

template<typename K>
class Qubit {
    private:
        K data_to_encode;
        K encode(K data_to_encode);
    public:
        inline Qubit(K data_to_encode);
        inline ~Qubit() = default;
};

#endif