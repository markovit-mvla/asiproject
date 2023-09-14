#ifndef PHOTON_H
#define PHOTON_H

struct Photon {
    bool polarization;
    Photon(bool polar) : polarization(polar) {}
};

#endif