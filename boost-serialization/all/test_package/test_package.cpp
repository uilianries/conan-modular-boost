#include <boost/archive/text_oarchive.hpp>
#include <boost/serialization/string.hpp>
#include <sstream>
int main() {
    std::stringstream ss;
    boost::archive::text_oarchive oa(ss);
    oa << std::string("Hello, Boost!");
}