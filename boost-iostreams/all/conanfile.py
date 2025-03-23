from conan import ConanFile
from conan.tools.files import copy, get, download
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
import os


required_conan_version = ">=2.4"


class BoostIostreamsConan(ConanFile):
    name = "boost-iostreams"
    description = "Boost.IOStreams provides a framework for defining streams, stream buffers and i/o filters"
    license = "BSL-1.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.boost.org/"
    topics = ("boost", "io", "string")
    package_type = "library"
    languages = "C++"
    settings = "os", "arch", "compiler", "build_type"
    implements = ["auto_shared_fpic"]
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "enable_bzip2": [True, False],
        "enable_lzma": [True, False],
        "enable_zstd": [True, False],
        "enable_zlib": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "enable_bzip2": True,
        "enable_lzma": True,
        "enable_zstd": True,
        "enable_zlib": True,
    }

    def export_sources(self):
        copy(self, "conan_project_include.cmake", self.recipe_folder, self.export_sources_folder)

    def requirements(self):
        self.requires(f"boost-headers/{self.version}")
        # transitive headers: boost/iostreams/filter/line.hpp:19:#include <boost/config.hpp>
        self.requires(f"boost-config/{self.version}", transitive_headers=True)
        # transitive headers: boost/iostreams/tee.hpp:15:#include <boost/assert.hpp>
        self.requires(f"boost-assert/{self.version}", transitive_headers=True)
        # transitive headers: boost/iostreams/chain.hpp:24:#include <boost/core/typeinfo.hpp>
        self.requires(f"boost-core/{self.version}", transitive_headers=True)
        # transitive headers: boost/iostreams/copy.hpp:27:#include <boost/detail/workaround.hpp>
        self.requires(f"boost-detail/{self.version}", transitive_headers=True)
        # transitive headers: boost/iostreams/filter/regex.hpp:16:#include <boost/function.hpp>
        self.requires(f"boost-function/{self.version}", transitive_headers=True)
        # transitive headers: boost/iostreams/seek.hpp:16:#include <boost/integer_traits.hpp>
        self.requires(f"boost-integer/{self.version}", transitive_headers=True)
        # transitive headers: boost/iostreams/chain.hpp:35:#include <boost/next_prior.hpp>
        self.requires(f"boost-iterator/{self.version}", transitive_headers=True)
        # transitive headers: boost/iostreams/invert.hpp:27:#include <boost/mpl/if.hpp>
        self.requires(f"boost-mpl/{self.version}", transitive_headers=True)
        # transitive headers: boost/iostreams/detail/select_by_size.hpp:69:#include <boost/preprocessor/cat.hpp>
        self.requires(f"boost-preprocessor/{self.version}", transitive_headers=True)
        # transitive headers: boost/iostreams/filter/test.hpp:31:# include <boost/random/uniform_smallint.hpp>
        self.requires(f"boost-random/{self.version}", transitive_headers=True)
        # transitive headers: boost/iostreams/detail/resolve.hpp:35:#include <boost/range/iterator_range.hpp>
        self.requires(f"boost-range/{self.version}", transitive_headers=True)
        # transitive headers: boost/iostreams/filter/regex.hpp:19:#include <boost/regex.hpp>
        self.requires(f"boost-regex/{self.version}", transitive_headers=True)
        # transitive headers: boost/iostreams/code_converter.hpp:45:#include <boost/shared_ptr.hpp>
        self.requires(f"boost-smart-ptr/{self.version}", transitive_headers=True)
        # transitive headers: boost/iostreams/tee.hpp:26:#include <boost/static_assert.hpp>
        self.requires(f"boost-static-assert/{self.version}", transitive_headers=True)
        # transitive headers: boost/iostreams/code_converter.hpp:47:#include <boost/throw_exception.hpp>
        self.requires(f"boost-throw-exception/{self.version}", transitive_headers=True)
        # transitive headers: boost/iostreams/close.hpp:27:#include <boost/type_traits/is_convertible.hpp>
        self.requires(f"boost-type-traits/{self.version}", transitive_headers=True)
        # transitive headers: boost/iostreams/stream.hpp:24:#include <boost/utility/base_from_member.hpp>
        self.requires(f"boost-utility/{self.version}", transitive_headers=True)

        self.requires(f"boost-numeric-conversion/{self.version}")

        if self.options.enable_bzip2:
            self.requires("bzip2/1.0.8")
        if self.options.enable_lzma:
            self.requires("xz_utils/[>=5.4.5 <6]")
        if self.options.enable_zstd:
            self.requires("zstd/[>=1.5 <1.6]")
        if self.options.enable_zlib:
            self.requires("zlib/[>=1.2.11 <2]")

    def layout(self):
        cmake_layout(self, src_folder="src")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)
        download(self, **self.conan_data["licenses"][self.version])

    def generate(self):
        tc = CMakeToolchain(self)
        # Boost does not have find_package, so we need to include them manually
        tc.cache_variables["CMAKE_PROJECT_boost_iostreams_INCLUDE"] = os.path.join(self.source_folder, os.pardir, "conan_project_include.cmake")
        tc.cache_variables["BUILD_TESTING"] = False
        tc.cache_variables["BOOST_IOSTREAMS_ENABLE_ZLIB"] = self.options.enable_zlib
        tc.cache_variables["BOOST_IOSTREAMS_ENABLE_BZIP2"] = self.options.enable_bzip2
        tc.cache_variables["BOOST_IOSTREAMS_ENABLE_LZMA"] = self.options.enable_lzma
        tc.cache_variables["BOOST_IOSTREAMS_ENABLE_ZSTD"] = self.options.enable_zstd
        if self.options.enable_zstd:
            tc.cache_variables["BOOST_IOSTREAMS_ZSTD_TARGET"] = "zstd::libzstd_shared" if self.options.shared else "zstd::libzstd_static"
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
        self.cpp_info.set_property("cmake_file_name", "boost_iostreams")
        self.cpp_info.set_property("cmake_target_name", "Boost::iostreams")
        self.cpp_info.libs = ["boost_iostreams"]
        self.cpp_info.defines = [
            "BOOST_IOSTREAMS_NO_LIB",
            "BOOST_IOSTREAMS_DYN_LINK" if self.options.shared else "BOOST_IOSTREAMS_STATIC_LINK"]
