#include <vector>
#include <iostream>

int main()
{
	std::vector<int64_t> x(10);
	std::vector<int64_t> y(x.size() - 1);
	int i = 0;
	std::generate( x.begin(), x.end(), [&i](){ return i++; } );

	std::transform( x.begin(), x.end() - 1, x.begin() + 1, y.begin(), []( const uint64_t& x1, const uint64_t& x2 ) { return x1 + x2; } );

	std::copy( x.begin(), x.end(), std::ostream_iterator<
	std::cout << "\n";
}
