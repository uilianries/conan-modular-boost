#include <boost/multi_index_container.hpp>
#include <boost/multi_index/ordered_index.hpp>
#include <boost/multi_index/member.hpp>
#include <iostream>
using namespace boost::multi_index;

struct Message { int id; std::string name; };
typedef multi_index_container<Message,
    indexed_by<ordered_unique<member<Message, int, &Message::id>>>> msg_set;

int main() {
    msg_set ps;
    ps.insert({1, "Boost Multi-Index test package"});
    std::cout << ps.find(1)->name << std::endl;
    return 0;
}