#include <boost/msm/front/state_machine_def.hpp>
#include <boost/msm/back/state_machine.hpp>
#include <boost/mpl/vector.hpp>
#include <iostream>

struct Machine : boost::msm::front::state_machine_def<Machine> {
    struct State {
        typedef boost::mpl::vector<> deferred_events;
        typedef boost::mpl::vector<> internal_transition_table;
    };
    typedef State initial_state;
    typedef boost::mpl::vector<> transition_table;
};

int main() {
    boost::msm::back::state_machine<Machine> machine;
    std::cout << "Boost SMS test package" << std::endl;
    return 0;
}
