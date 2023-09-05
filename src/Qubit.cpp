#include <iostream>

#include "Qubit.hpp"

template<typename K>
inline Qubit<K>::Qubit(K data_to_encode) {
    this->data_to_encode = encode(data_to_encode);
}

template<typename K>
K Qubit<K>::encode(K data_to_encode) {
    
}