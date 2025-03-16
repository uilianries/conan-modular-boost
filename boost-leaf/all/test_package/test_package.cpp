#include <boost/leaf.hpp>
#include <iostream>

boost::leaf::result<int> compute() {
    return boost::leaf::new_error();
}

int main() {
    boost::leaf::try_handle_all(
        []() -> boost::leaf::result<void> {
            BOOST_LEAF_CHECK(compute());
            return {};
        },
        [](const boost::leaf::error_info&) {
            std::cout << "Boost leaf test package" << std::endl;
        }
    );
    return 0;
}