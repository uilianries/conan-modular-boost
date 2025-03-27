#include <boost/wave.hpp>
#include <boost/wave/cpplexer/cpp_lex_token.hpp>
#include <boost/wave/cpplexer/cpp_lex_iterator.hpp>
#include <iostream>

int main() {
    std::string input = "42";
    using token_type = boost::wave::cpplexer::lex_token<>;
    using lex_iterator_type = boost::wave::cpplexer::lex_iterator<token_type>;
    boost::wave::context<std::string::iterator, lex_iterator_type> ctx(input.begin(), input.end());
    std::cout << "Boost Wave test package: " << *ctx.begin() << std::endl;
    return 0;
}
