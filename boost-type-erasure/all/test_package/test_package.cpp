#include <boost/type_erasure/any.hpp>
#include <boost/type_erasure/relaxed.hpp>
#include <boost/type_erasure/typeid_of.hpp>
#include <boost/type_erasure/callable.hpp>
#include <iostream>

int main() {
    boost::type_erasure::any<boost::type_erasure::copy_constructible<>> value = 42;
    std::cout << "Boost Type Erasure test package" << std::endl;
    return 0;
}