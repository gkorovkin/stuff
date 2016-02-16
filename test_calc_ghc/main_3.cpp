#include <iostream>
int main() {
	int64_t sum = 0;
	for(int e = 0; e < 200; ++e) {
		sum = 0;
		for(int i = 0; i < 1000000; i += 100 )
			sum += 2 * i + 1;
	}
	std::cout << sum << std::endl;
	return 0;
}
