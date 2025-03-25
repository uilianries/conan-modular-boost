from conan import ConanFile
from conan.tools.files import copy, get, download, replace_in_file
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.build import check_min_cppstd
from conan.tools.microsoft import is_msvc
import os


required_conan_version = ">=2.4"


class BoostCobaltConan(ConanFile):
    name = "boost-cobalt"
    description = "Coroutines. Basic Algorithms & Types"
    license = "BSL-1.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.boost.org/"
    topics = ("boost", "concurrent", "coroutines", "awaitables", "asynchronous")
    package_type = "library"
    languages = "C++"
    settings = "os", "arch", "compiler", "build_type"
    implements = ["auto_shared_fpic"]
    options = {"shared": [True, False], "fPIC": [True, False], "use_boost_container": [True, False]}
    default_options = {"shared": False, "fPIC": True, "use_boost_container": True}
    options_description = {
        "use_boost_container": "Boost.Cobalt: Use boost.container instead of std::pmr"
    }

    def export_sources(self):
        copy(self, "conan_project_include.cmake", self.recipe_folder, self.export_sources_folder)

    def requirements(self):
        self.requires(f"boost-headers/{self.version}", transitive_headers=True)
        self.requires(f"boost-config/{self.version}", transitive_headers=True)
        self.requires(f"boost-asio/{self.version}", transitive_headers=True)
        self.requires(f"boost-callable-traits/{self.version}", transitive_headers=True)
        self.requires(f"boost-circular-buffer/{self.version}", transitive_headers=True)
        self.requires(f"boost-core/{self.version}", transitive_headers=True)
        self.requires(f"boost-intrusive/{self.version}", transitive_headers=True)
        self.requires(f"boost-leaf/{self.version}", transitive_headers=True)
        self.requires(f"boost-mp11/{self.version}", transitive_headers=True)
        self.requires(f"boost-preprocessor/{self.version}", transitive_headers=True)
        self.requires(f"boost-smart-ptr/{self.version}", transitive_headers=True)
        self.requires(f"boost-system/{self.version}", transitive_headers=True)
        self.requires(f"boost-throw-exception/{self.version}", transitive_headers=True)
        self.requires(f"boost-variant2/{self.version}", transitive_headers=True)
        self.requires(f"boost-context/{self.version}", transitive_headers=True)
        if self.options.use_boost_container:
            # INFO: Transitive libs to avoid undefined symbol boost::container::pmr::get_default_resource()
            self.requires(f"boost-container/{self.version}", transitive_headers=True, transitive_libs=True)


    def layout(self):
        cmake_layout(self, src_folder="src")

    def validate(self):
        check_min_cppstd(self, "20")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)
        download(self, **self.conan_data["licenses"][self.version])
        # INFO: Avoid building inlined Boost.Cobalt
        replace_in_file(self, os.path.join(self.source_folder, "CMakeLists.txt"), "set(BOOST_COBALT_IS_ROOT ON)", "")

    def generate(self):
        tc = CMakeToolchain(self)
        # Boost does not have find_package, so we need to include them manually
        tc.cache_variables["CMAKE_PROJECT_boost_cobalt_INCLUDE"] = os.path.join(self.source_folder, os.pardir, "conan_project_include.cmake")
        tc.cache_variables["BOOST_COBALT_USE_BOOST_CONTAINER"] = self.options.use_boost_container
        tc.cache_variables["BUILD_TESTING"] = False
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
        self.cpp_info.set_property("cmake_file_name", "boost_cobalt")
        self.cpp_info.set_property("cmake_target_name", "Boost::cobalt")
        self.cpp_info.libs = ["boost_cobalt"]
        if self.settings.os in ["Linux", "FreeBSD"]:
            self.cpp_info.system_libs = ["pthread"]
        self.cpp_info.defines = [
            "BOOST_COBALT_NO_LIB",
            "BOOST_COBALT_DYN_LINK" if self.options.shared else "BOOST_COBALT_STATIC_LINK"]
        if self.options.use_boost_container:
            self.cpp_info.defines.append("BOOST_COBALT_USE_BOOST_CONTAINER_PMR=1")
        if is_msvc(self):
            self.cpp_info.defines.append("_WIN32_WINNT=0x0601")
