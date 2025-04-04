from conan import ConanFile
from conan.tools.files import copy, get, download
from conan.tools.layout import basic_layout
import os


required_conan_version = ">=2.4"


class BoostDateTimeConan(ConanFile):
    name = "boost-date-time"
    description = "A set of date-time libraries based on generic programming concepts"
    license = "BSL-1.0"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://www.boost.org/"
    topics = ("boost", "domain", "time", "header-only")
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
        # transitive headers: boost/date_time/compiler_config.hpp:12:#include <boost/config.hpp>
        self.requires(f"boost-config/{self.version}")
        # transitive headers: boost/date_time/time_facet.hpp:25:#include <boost/algorithm/string/erase.hpp>
        self.requires(f"boost-algorithm/{self.version}")
        # transitive headers: boost/date_time/time_facet.hpp:21:#include <boost/assert.hpp>
        self.requires(f"boost-assert/{self.version}")
        # transitive headers: boost/date_time/time_duration.hpp:12:#include <boost/core/enable_if.hpp>
        self.requires(f"boost-core/{self.version}")
        # transitive headers: boost/date_time/date_formatting.hpp:14:#include <boost/io/ios_state.hpp>
        self.requires(f"boost-io/{self.version}")
        # transitive headers: boost/date_time/time_facet.hpp:22:#include <boost/lexical_cast.hpp>
        self.requires(f"boost-lexical-cast/{self.version}")
        # transitive headers: boost/date_time/c_local_time_adjustor.hpp:20:#include <boost/numeric/conversion/cast.hpp>
        self.requires(f"boost-numeric-conversion/{self.version}")
        # transitive headers: boost/date_time/time_facet.hpp:24:#include <boost/range/as_literal.hpp>
        self.requires(f"boost-range/{self.version}")
        # transitive headers: boost/date_time/tz_db_base.hpp:18:#include <boost/shared_ptr.hpp>
        self.requires(f"boost-smart-ptr/{self.version}")
        # transitive headers: boost/date_time/time_duration.hpp:18:#include <boost/static_assert.hpp>
        self.requires(f"boost-static-assert/{self.version}")
        # transitive headers: boost/date_time/c_time.hpp:20:#include <boost/throw_exception.hpp>
        self.requires(f"boost-throw-exception/{self.version}")
        # transitive headers: boost/date_time/date_parsing.hpp:17:#include <boost/tokenizer.hpp>
        self.requires(f"boost-tokenizer/{self.version}")
        # transitive headers: boost/date_time/constrained_value.hpp:17:#include <boost/type_traits/is_base_of.hpp>
        self.requires(f"boost-type-traits/{self.version}")
        # transitive headers: boost/date_time/compiler_config.hpp:13:#include <boost/detail/workaround.hpp>
        self.requires(f"boost-utility/{self.version}")
        # transitive headers: boost/date_time/microsec_time_clock.hpp:24:#include <boost/winapi/time.hpp>
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
        self.cpp_info.set_property("cmake_file_name", "boost_date_time")
        self.cpp_info.set_property("cmake_target_name", "Boost::date_time")
        self.cpp_info.bindirs = []
        self.cpp_info.libdirs = []
