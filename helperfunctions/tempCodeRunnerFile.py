#include <iostream>
#include <vector>
using namespace std;

int main() {
int size;
cin >> size;
vector<int> arr;

for (int i = 0; i < size; i++) {
int element;
cin >> element;
arr.push_back(element);
}

for (int i = 0; i < size; i++) {
int element = arr[i];
bool found = false;  // Variable to track if a higher element is found

for (int j = i + 1; j < size; j++) {
if (arr[j] > element) {
    cout << arr[j] << " ";
    found = true;  // Set found to true if a higher element is found
    break;         // Break the loop as we found the first higher element
}
}

if (!found) {
cout << "No higher value" << " ";
}
}

return 0;
}
