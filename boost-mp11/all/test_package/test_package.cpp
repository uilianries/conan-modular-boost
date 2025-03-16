#include <boost/mp11.hpp>
#include <iostream>

using L = boost::mp11::mp_list<int, float, double>;
using F = boost::mp11::mp_first<L>;

int main() {
    std::cout << "Boost MP11 test pacakge: " << std::is_same_v<F, int> << std::endl;
    return 0;
}