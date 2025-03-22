#include <boost/metaparse/string.hpp>
#include <boost/metaparse/int_.hpp>
#include <boost/metaparse/start.hpp>
#include <boost/metaparse/get_result.hpp>
#include <iostream>

int main() {
    typedef boost::metaparse::get_result<boost::metaparse::int_::apply<BOOST_METAPARSE_STRING("123"), boost::metaparse::start>>::type result;
    std::cout << "Boost Metaparse test package: " << result::value;
    return 0;
}