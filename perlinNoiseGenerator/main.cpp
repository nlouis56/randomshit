#include <iostream>
#include <cmath>
#include <vector>
#include <random>
#include <fstream>
#include <filesystem>

// Function to generate a random gradient vector
std::vector<std::vector<double>> generateRandomGradients(int width, int height) {
    std::vector<std::vector<double>> gradients(height, std::vector<double>(width, 0.0));
    std::default_random_engine generator = std::default_random_engine(std::random_device()());
    std::uniform_real_distribution<double> distribution(-1.0, 1.0);

    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            double angle = 2 * M_PI * distribution(generator);
            gradients[y][x] = std::cos(angle);
        }
    }

    return gradients;
}

// Fade function as defined by Ken Perlin
double fade(double t) {
    return t * t * t * (t * (t * 6 - 15) + 10);
}

// Linear interpolation function
double lerp(double a, double b, double t) {
    return a + t * (b - a);
}

// Function to compute Perlin noise at a specific point
double perlinNoise(double x, double y, const std::vector<std::vector<double>>& gradients) {
    int x0 = static_cast<int>(x);
    int x1 = x0 + 1;
    int y0 = static_cast<int>(y);
    int y1 = y0 + 1;

    double dx0 = x - x0;
    double dx1 = x - x1;
    double dy0 = y - y0;
    double dy1 = y - y1;

    double dot00 = dx0 * gradients[y0][x0] + dy0 * gradients[y0][x0];
    double dot01 = dx0 * gradients[y1][x0] + dy1 * gradients[y1][x0];
    double dot10 = dx1 * gradients[y0][x1] + dy0 * gradients[y0][x1];
    double dot11 = dx1 * gradients[y1][x1] + dy1 * gradients[y1][x1];

    double u = fade(dx0);
    double v = fade(dy0);

    return lerp(lerp(dot00, dot10, u), lerp(dot01, dot11, u), v);
}

std::vector<std::vector<double>> computeNoiseGrid(int height, int width, double frequency, double amplitude) {
    std::vector<std::vector<double>> gradients = generateRandomGradients(width, height);
    std::vector<std::vector<double>> noise(height, std::vector<double>(width, 0.0));

    // Compute Perlin noise for each point in the grid and store the result in the noise vector
    std::cout << "Computing Perlin noise..." << std::endl;
    for (int y = 0; y < height; y++) {
        double ny = y * frequency;
        for (int x = 0; x < width; x++) {
            double nx = x * frequency;
            noise[y][x] = perlinNoise(nx, ny, gradients) * amplitude;
        }
    }
    std::cout << "Noise computed." << std::endl;

    return noise;
}

void makeFileFromNoiseGrid(const std::vector<std::vector<double>>& noise, int width, int height) {
    // Write the noise vector to a PPM file (can be opened with GIMP)
    std::cout << "Writing to file..." << std::endl;
    std::ofstream file("noise.ppm");
    file << "P3" << std::endl;
    file << width << " " << height << std::endl;
    file << "255" << std::endl;
    for (const auto& row : noise) {
        for (const auto& value : row) {
            int color = static_cast<int>((value + 1.0) * 127.5);
            file << color << " " << color << " " << color << std::endl;
        }
    }
    file.close();
    std::cout << "PPM file done." << std::endl;
}

int main() {
    int width = 1024;  // Width of the grid
    int height = 1024; // Height of the grid

    std::vector<std::vector<double>> gradients = generateRandomGradients(width, height);

    double frequency = 0.004; // Adjust the frequency of the Perlin noise
    double amplitude = 1.0; // Adjust the amplitude of the Perlin noise

    std::vector<std::vector<double>> noise = computeNoiseGrid(height, width, frequency, amplitude);

    makeFileFromNoiseGrid(noise, width, height);

    // Print the path to the noise.ppm file
    std::filesystem::path filePath = std::filesystem::current_path() / "noise.ppm";
    std::cout << "File saved at: " << filePath << std::endl;

    return 0;
}
