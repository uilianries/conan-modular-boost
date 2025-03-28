#include <boost/accumulators/accumulators.hpp>
#include <boost/accumulators/statistics/stats.hpp>
#include <boost/accumulators/statistics/mean.hpp>
#include <iostream>

int main() {
    boost::accumulators::accumulator_set<double, boost::accumulators::stats<boost::accumulators::tag::mean>> acc;
    acc(1.0);
    acc(2.0);
    std::cout << "Boost Accumulator test package: " << boost::accumulators::mean(acc) << std::endl;
    return 0;
}
