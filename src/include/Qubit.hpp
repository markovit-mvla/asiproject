#ifndef QUBIT_HPP
#define QUBIT_HPP

#include <string>
#include <memory>
#include "Photon.h"

// K - type of Qubit data to encode
template<typename K>
class Qubit {
    private:
        bool state; 
        K data_to_encode;
        K encode(K data_to_encode);
    public:
        inline Qubit(K data_to_encode) : state(false), data_to_encode(encode(data_to_encode)) {}
        void apply_photon(const Photon& photon);
        inline bool get_state() const { return state; }
        inline ~Qubit() = default;
};

#endif