#include <vector>
#include <iostream>

int main() {
	int64_t sum = 0;

	for(int e = 0; e < 200; e++) {
		sum = 0;

		std::vector<int64_t> x;
		for(int i = 0; i < 1000000; i++) {
			x.push_back(i);
		}

		std::vector<int64_t> y;
		for(int i = 0; i < 1000000-1; i++) {
			y.push_back(x[i] + x[i+1]);
		}

		for (int i = 0; i < 1000000; i += 100) {
			sum += y[i];
		}
	}

	std::cout << sum << std::endl;
}
