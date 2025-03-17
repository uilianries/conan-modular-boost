#include <boost/type_index.hpp>
#include <iostream>

int main() {
    std::cout << "Boost Type Index test package: " << boost::typeindex::type_id_with_cvr<int>().pretty_name() << std::endl;
    return 0;
}