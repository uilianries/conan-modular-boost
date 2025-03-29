from conan import ConanFile
from conan.tools.files import copy, get, download
from conan.tools.layout import basic_layout
from conan.tools.build import check_min_cppstd
import os


required_conan_version = ">=2.4"


class BoostBeastConan(ConanFile):
    name = "boost-beast"
    description = "Portable HTTP, WebSocket, and network operations using only C++11 and Boost.Asio"
    license = "BSL-1.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.boost.org/"
    topics = ("boost", "concurrent", "io", "header-only")
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
        self.requires(f"boost-asio/{self.version}")
        self.requires(f"boost-assert/{self.version}")
        self.requires(f"boost-bind/{self.version}")
        self.requires(f"boost-container/{self.version}")
        self.requires(f"boost-core/{self.version}")
        self.requires(f"boost-endian/{self.version}")
        self.requires(f"boost-intrusive/{self.version}")
        self.requires(f"boost-logic/{self.version}")
        self.requires(f"boost-mp11/{self.version}")
        self.requires(f"boost-optional/{self.version}")
        self.requires(f"boost-smart-ptr/{self.version}")
        self.requires(f"boost-static-assert/{self.version}")
        self.requires(f"boost-static-string/{self.version}")
        self.requires(f"boost-system/{self.version}")
        self.requires(f"boost-throw-exception/{self.version}")
        self.requires(f"boost-type-traits/{self.version}")
        self.requires(f"boost-winapi/{self.version}")
        self.requires(f"boost-container-hash/{self.version}")
        self.requires(f"boost-preprocessor/{self.version}")
        self.requires(f"boost-type-index/{self.version}")

    def validate(self):
        check_min_cppstd(self, "11")

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
        self.cpp_info.set_property("cmake_file_name", "boost_beast")
        self.cpp_info.set_property("cmake_target_name", "Boost::beast")
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []
