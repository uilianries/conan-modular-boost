#include <boost/interprocess/managed_shared_memory.hpp>
#include <iostream>

int main() {
    boost::interprocess::shared_memory_object::remove("MySharedMemory");
    boost::interprocess::managed_shared_memory shm(boost::interprocess::create_only, "MySharedMemory", 1024);
    std::cout << "Boost Interprocess test package: " << std::endl;
    return 0;
}