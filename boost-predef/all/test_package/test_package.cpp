#include <boost/predef.h>
#include <iostream>

int main() {
    std::cout << "Architecture: "
              << (BOOST_ARCH_X86_64 ? "x86_64" : "other")
              << std::endl;
    return 0;
}