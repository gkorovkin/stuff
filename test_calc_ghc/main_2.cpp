#include <vector>
#include <iostream>
#include <numeric>

std::vector<int64_t> x(1000000);
std::vector<int64_t> y(x.size() - 1);

int main() {
	int64_t sum = 0;

	for(int e = 0; e < 200; e++) {
		sum = 0;
		int i = 0;

		for( i = 0; i < x.size(); ++i )
			x[ i ] = i;

		for( i = 0; i < y.size(); ++i )
			y[ i ] = x[ i ] + x[ i + 1 ];

		for( i = 0; i < y.size(); i+=100 )
			sum += y[ i ];
	}

	std::cout << sum << std::endl;

	return 0;
}
