#include <boost/statechart/state_machine.hpp>
#include <boost/statechart/simple_state.hpp>
#include <iostream>

struct State1;
struct Machine : boost::statechart::state_machine<Machine, State1> {};

struct State1 : boost::statechart::simple_state<State1, Machine> {
    State1() { std::cout << "Boost Statechart test package" << std::endl; }
};

int main() {
    Machine m;
    m.initiate();
    return 0;
}