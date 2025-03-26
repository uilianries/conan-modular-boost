#include <boost/process.hpp>
#include <iostream>

int main() {
    boost::process::system("echo 'Boost Process test package'");
    return 0;
}
