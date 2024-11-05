#include <iostream>
#include <fstream>
#include <string>

int main()
{
    const int npts = 128;
    double* ph = new double[npts](); // Dynamically allocate and initialize to zero

    double accu = 0;
    const double coeff[2] = {0.5, 0.05};

    // Set values at specific positions, adjusting for larger array size
    ph[npts / 6] = 1000;
    ph[npts / 2] = 500;
    //ph[100] = 700;
    //ph[800] = 700;

    // Smoothing process
    for (int j = 0; j < 2; ++j) {
        accu = ph[0];
        for (int i = 0; i < npts; ++i) {
            accu += coeff[j] * (ph[i] - accu);
            ph[i] = accu;
        }
    }

    // Write output to file
    std::ofstream outFile("data.dat");
    for (int i = 0; i < npts; ++i) outFile << ph[i] << std::endl;
    outFile.close();

    std::cout << "Data written to data.dat file successfully." << std::endl;

    // Clean up dynamically allocated memory
    delete[] ph;
    return 0;
}
