from conan import ConanFile
from conan.tools.files import copy, get, download
from conan.tools.layout import basic_layout
from conan.tools.build import check_min_cppstd
import os


required_conan_version = ">=2.4"


class BoostGILConan(ConanFile):
    name = "boost-gil"
    description = "(C++14) Generic Image Library"
    license = "BSL-1.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.boost.org/"
    topics = ("boost", "algorithms", "containers", "generic", "image-processing", "header-only")
    package_type = "header-library"
    languages = "C++"
    settings = "os", "arch", "compiler", "build_type"
    no_copy_source = True

    def layout(self):
        basic_layout(self, src_folder="src")

    def package_id(self):
        self.info.clear()

    def requirements(self):
        self.requires(f"boost-headers/{self.version}")
        self.requires(f"boost-config/{self.version}")
        self.requires(f"boost-assert/{self.version}")
        self.requires(f"boost-concept-check/{self.version}")
        self.requires(f"boost-container-hash/{self.version}")
        self.requires(f"boost-core/{self.version}")
        self.requires(f"boost-filesystem/{self.version}")
        self.requires(f"boost-integer/{self.version}")
        self.requires(f"boost-iterator/{self.version}")
        self.requires(f"boost-mp11/{self.version}")
        self.requires(f"boost-preprocessor/{self.version}")
        self.requires(f"boost-type-traits/{self.version}")
        self.requires(f"boost-variant2/{self.version}")

        self.requires("libpng/[>=1.6 <2]")
        self.requires("libjpeg/9e")
        self.requires("libtiff/[>=4.7.0 <5]")

    def validate(self):
        check_min_cppstd(self, "14")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)
        download(self, **self.conan_data["licenses"][self.version])

    def build(self):
        pass

    def package(self):
        copy(self, "LICENSE_1_0.txt", self.source_folder, os.path.join(self.package_folder, "licenses"))
        copy(self, "*.hpp", os.path.join(self.source_folder, "include"), os.path.join(self.package_folder, "include"))
        copy(self, "*.h", os.path.join(self.source_folder, "include"), os.path.join(self.package_folder, "include"))
        copy(self, "*.ipp", os.path.join(self.source_folder, "include"), os.path.join(self.package_folder, "include"))

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "boost_gil")
        self.cpp_info.set_property("cmake_target_name", "Boost::gil")
        self.cpp_info.defines = ["BOOST_GIL_USE_BOOST_FILESYSTEM"]
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []
