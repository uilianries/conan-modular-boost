import os
import subprocess
import argparse
import json
import logging
import sys


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    arg_parser = argparse.ArgumentParser(prog='build_boost',
                    description='Export and build all boost modules')
    arg_parser.add_argument('-bv', '--boost-version', type=str, default='1.87.0', help="Boost project version")
    arg_parser.add_argument('-se', '--skip-export', action='store_true', help="Do not run conan export for all Boost modules")
    arg_parser.add_argument('-sc', '--skip-create', action='store_true', help="Do not run conan create for all Boost modules")
    arg_parser.add_argument('-lb', '--last_build', action='store_true', help="Continue building from the last built module that failed")
    args = arg_parser.parse_args()
    boost_version = args.boost_version
    folder_list = []
    header_libraries = []
    regular_libraries = []
    continue_last_built = args.last_build

    for folder in os.listdir('.'):
        if os.path.isdir(folder) and folder.startswith('boost-'):
            folder_list.append(folder)

    logger.info(f"Found {len(folder_list)} Boost modules in total to be exported.")

    for folder in folder_list:
        conanfile_path = os.path.join(folder, 'all', 'conanfile.py')
        if os.path.exists(conanfile_path):
            with open(conanfile_path, 'r') as conanfile:
                content = conanfile.read()
                if 'header-library' in content:
                    header_libraries.append(folder)
                else:
                    regular_libraries.append(folder)

    logger.info(f"Found {len(header_libraries)} Boost modules that are header-only libraries.")
    logger.info(f"Found {len(regular_libraries)} Boost modules that are regular libraries.")

    if not args.skip_export:
        total = len(folder_list)
        for index, folder in enumerate(folder_list):
            logger.info(f'=== Exporting {folder} ({index + 1}/{total}) ===')
            subprocess.run(f'conan export {folder}/all --version={boost_version}', shell=True, check=True)

    temp_dir = os.getenv('RUNNER_TEMP') or "/tmp"
    conanfile = os.path.join(temp_dir, 'conanfile.txt')
    last_built = os.path.join(temp_dir, 'conan_last_built.txt')

    with open(conanfile, 'w') as fd:
        fd.write("[requires]\n")
        for module in folder_list:
            fd.write(f"{module}/{boost_version}\n")

    logger.info(f"=== Calculating build order for {len(folder_list)} Boost modules. ===")
    context = subprocess.run(f'conan graph build-order {conanfile} --format=json --order-by=recipe --update --build=missing -s compiler.cppstd=20', shell=True, capture_output=True, text=True)
    if context.returncode != 0:
        logger.error(f"Failed to build order: {context.stderr}")
        sys,exit(1)
    graph = json.loads(context.stdout)
    references = []
    for level in graph["order"]:
        for node in level:
            reference = node['ref'][:node['ref'].find('/')]
            if reference.startswith('boost-') and os.path.isdir(reference):
                references.append(reference)

    logger.info(f"=== Build order ({len(references)}): {references} ===")

    if not args.skip_create:
        total = len(references)
        for index, reference in enumerate(references):
            if continue_last_built:
                if os.path.exists(last_built):
                    with open(last_built, 'r') as fd:
                        last_reference = str(fd.read()).strip()
                    if reference == last_reference:
                        continue_last_built = False
                    else:
                        continue
                else:
                    continue_last_built = False
                    logger.error(f'Could not find {last_built} to continue from.')

            logger.info(f'=== Creating {reference} ({index + 1}/{total}) ===')
            with open(last_built, 'w') as fd:
                fd.write(reference)
            subprocess.run(f'conan create {reference}/all --version={boost_version} --build=missing -s compiler.cppstd=20', shell=True, check=True)
