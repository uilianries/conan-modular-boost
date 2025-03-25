#include <boost/cobalt.hpp>
#include <boost/cobalt/main.hpp>
#include <iostream>

boost::cobalt::main co_main(int argc, char ** argv)
{
    std::cout << "Boost Cobalt test package" << std::endl;
    co_return 0;
}
