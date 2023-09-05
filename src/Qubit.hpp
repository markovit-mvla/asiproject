#pragma once

#include <string>
#include <memory>

#include "util.h"

class Qubit {
    private:
        std::string to_encode;
    public:
        Qubit(std::string to_encode) { this->to_encode = to_encode; }
        void encode();
        ~Qubit() = default;
};