from conan import ConanFile
from conan.tools.files import copy, get, download
from conan.tools.layout import basic_layout
import os


required_conan_version = ">=2.4"


class BoostInterprocessConan(ConanFile):
    name = "boost-interprocess"
    description = "Shared memory, memory mapped files, process-shared mutexes, condition variables, containers and allocators"
    license = "BSL-1.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.boost.org/"
    topics = ("boost", "concurrent", "header-only")
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
        self.requires(f"boost-container/{self.version}")
        self.requires(f"boost-intrusive/{self.version}")
        self.requires(f"boost-move/{self.version}")
        self.requires(f"boost-assert/{self.version}")
        if self.settings.os == "Windows":
            self.requires(f"boost-winapi/{self.version}")

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
        self.cpp_info.set_property("cmake_file_name", "boost_interprocess")
        self.cpp_info.set_property("cmake_target_name", "Boost::interprocess")
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []
        if self.settings.os == "Linux":
            self.cpp_info.system_libs = ["rt"]
        elif self.settings.os == "Windows":
            self.cpp_info.system_libs = ["ole32", "oleaut32", "psapi", "advapi32", "user32"]
