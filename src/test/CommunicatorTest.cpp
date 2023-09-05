#include <iostream>

#include "Communicator.hpp"

int main() {
    Communicator<short>* a = new Communicator<short>(5, "Bob");
    a->display();
    a->get_key();
}