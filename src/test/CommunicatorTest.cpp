#include <iostream>

#include "Communicator.hpp"

int main()
{
    Communicator<short, std::string>* a = new Communicator<short, std::string>(5, "Bob");
    Communicator<short, std::string>* b = new Communicator<short, std::string>(5, "Alice");
    Qubit<std::string>* c = new Qubit<std::string>("A");
    a->send(*c, Photon {}, *b);
    a->display();
    a->get_key();
}