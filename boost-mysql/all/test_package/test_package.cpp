#include <boost/mysql.hpp>
#include <iostream>

int main() {
    boost::mysql::with_params("SELECT * FROM users WHERE id = ?");
    std::cout << "Boost MySQL test package" << std::endl;
    return 0;
}
