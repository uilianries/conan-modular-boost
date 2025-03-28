#include <boost/mpi.hpp>
#include <iostream>

int main(int argc, char* argv[]) {
    boost::mpi::environment env(argc, argv);
    boost::mpi::communicator world;
    std::cout << "Boost MPI test package: " << world.rank() << " " << world.size() << std::endl;
    return 0;
}
