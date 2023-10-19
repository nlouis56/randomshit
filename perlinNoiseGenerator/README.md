# perlinNoiseGenerator

## Description

This is a simple perlin noise generator. It is based on the [Perlin noise](https://en.wikipedia.org/wiki/Perlin_noise) algorithm.

The algorithm is implemented using C++. The output is a PPM image, which you can open with an image viewer. You can also export the image to other formats using an image editor (e.g. [GIMP](https://www.gimp.org)).

## Usage

The compilation can be done using CMake.

Once the program is compiled, you can run it without any arguments.

You can adjust the parameters of the generator by modifying the `main.cpp` file, especially the width, height, frequency and amplitude. These variables are defined at the beginning of the `main` function.

