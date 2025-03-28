from conan import ConanFile
from conan.tools.files import copy, get, download
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.files import collect_libs
import os
import re


required_conan_version = ">=2.4"


class BoostPythonConan(ConanFile):
    name = "boost-python"
    description = "The Boost Python Library is a framework for interfacing Python and C++"
    license = "BSL-1.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.boost.org/"
    topics = ("boost", "miscellaneous", "time")
    package_type = "library"
    languages = "C++"
    settings = "os", "arch", "compiler", "build_type"
    implements = ["auto_shared_fpic"]
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    def export_sources(self):
        copy(self, "conan_project_include.cmake", self.recipe_folder, self.export_sources_folder)

    def requirements(self):
        self.requires(f"boost-headers/{self.version}", transitive_headers=True)
        self.requires(f"boost-config/{self.version}", transitive_headers=True)
        self.requires(f"boost-align/{self.version}", transitive_headers=True)
        self.requires(f"boost-bind/{self.version}", transitive_headers=True)
        self.requires(f"boost-conversion/{self.version}", transitive_headers=True)
        self.requires(f"boost-core/{self.version}", transitive_headers=True)
        self.requires(f"boost-detail/{self.version}", transitive_headers=True)
        self.requires(f"boost-foreach/{self.version}", transitive_headers=True)
        self.requires(f"boost-function/{self.version}", transitive_headers=True)
        self.requires(f"boost-iterator/{self.version}", transitive_headers=True)
        self.requires(f"boost-lexical-cast/{self.version}", transitive_headers=True)
        self.requires(f"boost-mpl/{self.version}", transitive_headers=True)
        self.requires(f"boost-numeric-conversion/{self.version}", transitive_headers=True)
        self.requires(f"boost-preprocessor/{self.version}", transitive_headers=True)
        self.requires(f"boost-smart-ptr/{self.version}", transitive_headers=True)
        self.requires(f"boost-static-assert/{self.version}", transitive_headers=True)
        self.requires(f"boost-tuple/{self.version}", transitive_headers=True)
        self.requires(f"boost-type-traits/{self.version}", transitive_headers=True)
        self.requires(f"boost-utility/{self.version}", transitive_headers=True)

        self.requires(f"boost-graph/{self.version}")
        self.requires(f"boost-integer/{self.version}")
        self.requires(f"boost-property-map/{self.version}")

    def layout(self):
        cmake_layout(self, src_folder="src")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)
        download(self, **self.conan_data["licenses"][self.version])

    def generate(self):
        tc = CMakeToolchain(self)
        # Boost does not have find_package, so we need to include them manually
        tc.cache_variables["CMAKE_PROJECT_boost_python_INCLUDE"] = os.path.join(self.source_folder, os.pardir, "conan_project_include.cmake")
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, "LICENSE_1_0.txt", self.source_folder, os.path.join(self.package_folder, "licenses"))
        copy(self, "*.hpp", os.path.join(self.source_folder, "include"), os.path.join(self.package_folder, "include"))
        copy(self, "*.h", os.path.join(self.source_folder, "include"), os.path.join(self.package_folder, "include"))
        copy(self, "*.ipp", os.path.join(self.source_folder, "include"), os.path.join(self.package_folder, "include"))
        if self.options.shared:
            copy(self, "*.so*", self.build_folder, os.path.join(self.package_folder, "lib"))
            copy(self, "*.dylib*", self.build_folder, os.path.join(self.package_folder, "lib"))
            copy(self, "*.dll", self.build_folder, os.path.join(self.package_folder, "bin"))
            copy(self, "*.dll.a", self.build_folder, os.path.join(self.package_folder, "lib"))
        else:
            copy(self, "*.a", self.build_folder, os.path.join(self.package_folder, "lib"))
        copy(self, "*.lib", self.build_folder, os.path.join(self.package_folder, "lib"))


    def package_info(self):
        # INFO: Boost python genetares libraries using python version as suffix.
        # When intalling, the python version may not match the one used to build the library.
        # So we need to set the library name based on what is packaged.

        # INFO: It's expected 2 libs: boost_python<version> and boost_numpy<version> (optional)
        all_libs = collect_libs(self)
        boost_python_lib = [lib for lib in all_libs if "boost_python" in lib]
        match = re.search(r"(\d+)", boost_python_lib[0])
        python_version = match.group(1)
        boost_numpy_lib = None
        if len(all_libs) > 1:
            boost_numpy_lib = [lib for lib in all_libs if "boost_numpy" in lib]

        self.cpp_info.set_property("cmake_file_name", "boost_python")
        self.cpp_info.components["python"].set_property("cmake_target_name", "Boost::python")
        self.cpp_info.components["python"].set_property("cmake_target_aliases", [f"Boost::python{python_version}"])
        self.cpp_info.components["python"].libs = boost_python_lib
        self.cpp_info.components["python"].defines = [
            "BOOST_PYTHON_NO_LIB",
            "BOOST_PYTHON_DYN_LINK" if self.options.shared else "BOOST_PYTHON_STATIC_LINK"
        ]
        if not self.options.shared:
            self.cpp_info.components["python"].defines.append("BOOST_PYTHON_STATIC_LIB")
        self.cpp_info.components["python"].requires = [
            "boost-headers::boost-headers",
            "boost-config::boost-config",
            "boost-core::boost-core",
            "boost-align::boost-align",
            "boost-bind::boost-bind",
            "boost-conversion::boost-conversion",
            "boost-detail::boost-detail",
            "boost-foreach::boost-foreach",
            "boost-function::boost-function",
            "boost-iterator::boost-iterator",
            "boost-lexical-cast::boost-lexical-cast",
            "boost-mpl::boost-mpl",
            "boost-numeric-conversion::boost-numeric-conversion",
            "boost-preprocessor::boost-preprocessor",
            "boost-smart-ptr::boost-smart-ptr",
            "boost-static-assert::boost-static-assert",
            "boost-tuple::boost-tuple",
            "boost-type-traits::boost-type-traits",
            "boost-utility::boost-utility",
            "boost-graph::boost-graph",
            "boost-integer::boost-integer",
            "boost-property-map::boost-property-map",
        ]

        if boost_numpy_lib:
            self.cpp_info.components["numpy"].set_property("cmake_target_name", "Boost::numpy")
            self.cpp_info.components["numpy"].set_property("cmake_target_aliases", [f"Boost::numpy{python_version}"])
            self.cpp_info.components["numpy"].libs = boost_numpy_lib
            self.cpp_info.components["numpy"].defines = [
                "BOOST_NUMPY_NO_LIB",
                "BOOST_NUMPY_DYN_LINK" if self.options.shared else "BOOST_NUMPY_STATIC_LINK"
            ]
            if not self.options.shared:
                self.cpp_info.components["numpy"].defines.append("BOOST_NUMPY_STATIC_LIB")
            self.cpp_info.components["numpy"].requires = [
                "python",
                "boost-headers::boost-headers",
                "boost-config::boost-config",
                "boost-core::boost-core",
                "boost-detail::boost-detail",
                "boost-mpl::boost-mpl",
                "boost-smart-ptr::boost-smart-ptr",
            ]
