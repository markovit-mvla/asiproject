/**
 * @author tohar
 * @brief communicator class for quantum key transfer endpoints
*/

#include <vector>
#include <utility>
#include <memory>

#include "../Dependencies/include/qpp.h"

template<typename T>
class Communicator {
    private:
        using bases_states_T = std::vector<std::pair<T, T>>;
        using key_T = std::vector<T>;
        std::unique_ptr<bases_states_T> bases_states;
        std::unique_ptr<key_T> key;
    public: 
        Communicator(int nQubits);
        void display();
        ~Communicator();
};

template<typename T>
Communicator<T>::Communicator(int nQubits) {
    bases_states(new bases_states_T(static_cast<size_t>(nQubits)));
    key(new key_T(static_cast<size_t>(nQubits)));
}

template<typename T>
void Communicator<T>::display() {
    using namespace qpp;
}

template<typename T>
Communicator<T>::~Communicator() {
    delete[] bases_states;
    delete[] key;
}