#include <boost/graph/use_mpi.hpp>
#include <boost/graph/parallel/algorithm.hpp>
#include <boost/graph/adjacency_list.hpp>
#include <iostream>

int main(void) {
    using Graph = boost::adjacency_list<boost::vecS, boost::vecS, boost::undirectedS>;
    Graph g(3);
    add_edge(0, 1, g);
    std::cout << "Boost Graph Parallel test package" << std::endl;
    return 0;
}
