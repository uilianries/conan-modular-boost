from conan import ConanFile
from conan.tools.files import copy, download, mkdir
import os


required_conan_version = ">=2.4"


BOOST_COMPONENTS = [
    "bind", "algorithm", "optional", "static-assert", "ublas", "proto", "stl-interfaces", "asio", "smart-ptr",
    "signals2", "regex", "multi-array", "convert", "core", "pool", "units", "assign", "circular-buffer", "metaparse",
    "thread", "system", "beast", "assert", "functional", "hana", "geometry", "parameter-python", "lockfree",
    "property-map", "multi-index", "type-index", "fusion", "graph", "multiprecision", "coroutine2", "histogram",
    "wave", "vmd", "variant2", "align", "function", "detail", "property-map-parallel", "redis", "static-string",
    "flyweight", "tuple", "exception", "io", "serialization", "leaf", "xpressive", "compute", "lexical-cast",
    "charconv", "contract", "tokenizer", "winapi", "function-types", "uuid", "polygon", "dynamic-bitset", "log",
    "math", "statechart", "logic", "range", "crc", "mpi", "interprocess", "preprocessor", "intrusive", "random",
    "container", "endian", "concept-check", "mysql", "nowide", "predef", "accumulators", "iostreams",
    "program-options", "json", "type-erasure", "typeof", "spirit", "headers", "atomic", "container-hash",
    "safe-numerics", "icl", "yap", "fiber", "array", "gil", "msm", "bimap", "local-function", "graph-parallel",
    "ptr-container", "callable-traits", "numeric-conversion", "pfr", "iterator", "dll", "describe", "conversion",
    "foreach", "process", "test", "config", "poly-collection", "chrono", "property-tree", "locale", "parameter",
    "scope", "tti", "mpl", "format", "move", "integer", "variant", "filesystem", "url", "outcome", "compat",
    "lambda", "context", "parser", "mp11", "odeint", "cobalt", "utility", "unordered", "python", "scope-exit",
    "ratio", "qvm", "type-traits", "stacktrace", "timer", "date-time", "interval", "lambda2", "any", "sort",
    "rational", "phoenix", "hof", "heap", "coroutine", "throw-exception",
]    


class BoostModularConan(ConanFile):
    name = "boost-modular"
    description = "Englobes all Boost libraries in a single package"
    license = "BSL-1.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.boost.org/"
    topics = ("boost", "packaging")
    package_type = "unknown"
    no_copy_source = True
    options = {f"with_{module}": [True, False] for module in BOOST_COMPONENTS}    
    default_options = {f"with_{module}": True for module in BOOST_COMPONENTS}
    # INFO: Disable modules that are complicated to enabled by default
    # Boost Cobalt requires C++20
    # Boost MPI requires MPI to be installed
    # Boost Graph Parallel requires MPI to be installed
    # Boost ODEInt requires MPI to be installed
    # Boost Property Map Parallel requires MPI to be installed
    _disabled_modules = ["cobalt", "mpi", "graph-parallel", "odeint", "property-map-parallel"]
    default_options.update({f"with_{module}": False for module in _disabled_modules})

    def config_options(self):
        boost_version_modules = self.conan_data["dependencies"][self.version]
        for option, _ in self.options.items():
            # INFO: Translate to module name: with_graph_parallel -> graph-parallel
            module = str(option)[5:].replace("_", "-")
            if module not in boost_version_modules:
                delattr(self.options, str(option))

    def requirements(self):
        for module in self.conan_data["dependencies"][self.version]:
            if self.options.get_safe(f"with_{module}", False):
                self.requires(f"boost-{module}/{self.version}", transitive_headers=True, transitive_libs=True)

    def source(self):
        download(self, **self.conan_data["licenses"][self.version])

    def build(self):
        pass

    def package(self):
        copy(self, "LICENSE_1_0.txt", self.source_folder, os.path.join(self.package_folder, "licenses"))
        # INFO: Create empty folder to avoid errors when using CMakeDeps: Imported target "Boost::<>" includes non-existent path
        mkdir(self, os.path.join(self.package_folder, "include"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "Boost")
        self.cpp_info.set_property("cmake_target_name", "Boost::boost")
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.includedirs = []

        for module in self.conan_data["dependencies"][self.version]:
            if self.options.get_safe(f"with_{module}", False):
                module_under = str(module).replace("-", "_")
                self.cpp_info.components[module_under].set_property("cmake_target_name", f"Boost::{module_under}")
                self.cpp_info.components[module_under].set_property("cmake_module_target_name", module_under)
                self.cpp_info.components[module_under].requires = [f"boost-{module}::boost-{module}"]
