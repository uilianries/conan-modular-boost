#include <boost/timer/timer.hpp>
#include <iostream>
#include <thread>

int main() {
    boost::timer::cpu_timer timer;
    std::this_thread::sleep_for(std::chrono::microseconds(10));
    timer.stop();
    std::cout << "Boost Timer test package: " << timer.format() << std::endl;
    return 0;
}