#include <iostream>
#include <fstream>

using namespace std;

int main()
{   
    ofstream myfile;
    myfile.open ("output.txt");
    int x, y;
    cin >> x;
    cin >> y;
    myfile << x+y;
    myfile.close();

    return 0;
}
