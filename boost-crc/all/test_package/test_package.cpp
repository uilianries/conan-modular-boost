#include <boost/crc.hpp>
#include <iostream>

int main() {
    boost::crc_32_type crc;
    crc.process_bytes("Hello World", 11);
    std::cout << "CRC32 (Hello World): " << crc.checksum() << std::endl;
    return 0;
}
