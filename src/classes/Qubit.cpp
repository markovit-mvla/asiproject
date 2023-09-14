/**
 * @author tohar
 * @brief qubit class to simulate quantum bit logic
*/

#include <iostream>

#include "Qubit.hpp"

/**
 * @todo Figure out how to encode the data using the photon
*/
template<typename K>
K Qubit<K>::encode(K data_to_encode) {
    return data_to_encode;
}

template<typename K>
void Qubit<K>::apply_photon(const Photon& photon) {
    if (photon->polarization) 
        state = !state;
}