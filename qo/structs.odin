package main

import "core:fmt"
import "core:mem"

Pair :: struct ($A, $B: typeid) { a: A, b: B }

bases_states_T($A, $B: typeid) :: distinct [dynamic]Pair(A, B)
key_T($T: typeid)              :: distinct [dynamic](T)
channel_T($T: typeid)          :: distinct [dynamic]Pair(Qubit(T), Photon)

Communicator :: struct ($T, $K: typeid) #packed {
    bases_states:      ^bases_states_T,
    key:               ^key_T,
    channel:           ^channel_T 

}

new_communicator :: #force_inline proc(num_qubits: int, $T, $K: typeid) -> ^Communicator {
    return Communicator { 
        make(bases_states_T(T, K), 0, num_qubits),
        make(key_T(T), 0, num_qubits),
        make(channel_T(T), 0, num_qubits)
    }
}

Qubit :: struct ($K: typeid) {

}

Photon :: struct {

}

main :: proc() {
    fmt.println("Hello, World!")
}