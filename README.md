# Conan Modular Boost


## Introduction

This is a modularized version of the [Boost](https://www.boost.org/) library for [Conan](https://conan.io/). The original Boost Conan package is a monolit that contains a lot of different modules. This Conan package splits the Boost library into multiple packages, each containing a single module. This allows you to only depend on the modules that you actually need, reducing the size of your dependencies and the build time of your project.

## Modules

The Boost 1.87.0 is composed by 153 modules, where 123 are header-only and 30 are compiled. Plus, in terms of dependencies, we have 21 levels of interdependencies.

For visualization, first you can check the [Boost Dependency Report](https://pdimov.github.io/boostdep-report/boost-1.87.0/module-levels.html).
Its extracted content is available in JSON format in the file [boost_module_dependencies.json](boost_module_dependencies.json).

Plus, you can check the [Boost Dependency Graph](docs/conan_boost_graph_info.html) and [Boost Build Order](docs/conan_boost_build_order.html).

## Building

The script [build_boost.py](build_boost.py) automates the process of building the Boost modules.
It exports all modules first, then it calculates the dependencies and builds them in the correct order.

In case wanting to build manually, you can follow these steps:

```bash
find . -type d -name "boost-*" -exec conan export {}/all --version=1.87 \;
find . -type d -name "boost-*" -exec conan create {}/all --version=1.87 --build=missing -s compiler.cppstd=20 \;
```

These commands will export all modules and create the packages for each module. The `--build=missing` option will build any missing dependencies.
It does not respect the build order, so it is recommended to use the script `build_boost.py` instead.

The C++20 is required due [Boost Cobalt](https://www.boost.org/doc/libs/1_87_0/libs/cobalt/doc/html/index.html) only.

## Grouping all modules in a single package

This is an open discussion, but [boost-modular](boost-modular) is the current workaround:
It groups all modules in a single Conan package, then generates a CMakeDeps respecting the original Boost structure.

- See https://cmake.org/cmake/help/v3.31/module/FindBoost.html#boost-cmake


## License

[MIT](LICENSE)