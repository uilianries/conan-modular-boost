# Conan Modular Boost


## Introduction

This is a modularized version of the [Boost](https://www.boost.org/) library for [Conan](https://conan.io/). The original Boost Conan package is a monolit that contains a lot of different modules. This Conan package splits the Boost library into multiple packages, each containing a single module. This allows you to only depend on the modules that you actually need, reducing the size of your dependencies and the build time of your project.

## Modules

The dependencies levels are split into the following modules: https://pdimov.github.io/boostdep-report/boost-1.87.0/module-levels.html

## License

[MIT](LICENSE)