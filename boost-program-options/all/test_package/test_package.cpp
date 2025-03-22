#include <boost/program_options.hpp>
#include <iostream>

int main(int argc, char* argv[]) {
    namespace po = boost::program_options;
    po::options_description desc("Options");
    desc.add_options()("help", "show help");

    po::variables_map vm;
    po::store(po::parse_command_line(argc, argv, desc), vm);

    std::cout << "Boost Program Options test package" << std::endl;
    return 0;
}