#include <boost/graph/adjacency_list.hpp>
#include <iostream>

int main() {
    boost::adjacency_list<> g(3);
    boost::add_edge(0, 1, g);
    std::cout << "Boost Graph test package: " << boost::num_vertices(g) << std::endl;
    return 0;
}