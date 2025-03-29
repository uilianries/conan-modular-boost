import os
import subprocess
import argparse
import json
import logging


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    arg_parser = argparse.ArgumentParser(prog='build_boost',
                    description='Export and build all boost modules')
    arg_parser.add_argument('-bv', '--boost-version', type=str, default='1.87.0', help="Boost project version")
    arg_parser.add_argument('-se', '--skip-export', action='store_true', help="Do not run conan export for all Boost modules")
    arg_parser.add_argument('-sc', '--skip-create', action='store_true', help="Do not run conan create for all Boost modules")
    args = arg_parser.parse_args()
    boost_version = args.boost_version
    folder_list = []
    header_libraries = []
    regular_libraries = []

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
        for folder in folder_list:
            logger.info(f'Exporting {folder}')
            subprocess.run(f'conan export {folder}/all --version={boost_version}', shell=True, check=True)

    temp_dir = os.getenv('RUNNER_TEMP') or "/tmp"
    conanfile = os.path.join(temp_dir, 'conanfile.txt')

    with open(conanfile, 'w') as fd:
        fd.write("[requires]\n")
        for module in folder_list:
            fd.write(f"{module}/{boost_version}\n")

    context = subprocess.run(f'conan graph build-order {conanfile} --format=json --build=missing -s compiler.cppstd=20', shell=True, capture_output=True, text=True, check=True)
    graph = json.loads(context.stdout)
    references = []
    for level in graph:
        for node in level:
            reference = node['ref'][:node['ref'].find('/')]
            if reference.startswith('boost-') and os.path.isdir(reference):
                references.append(reference)

    logger.info(f"Build order ({len(references)}): {references}")

    if not args.skip_create:
        for reference in references:
            logger.info(f'Creating {reference}')
            subprocess.run(f'conan create {reference}/all --version={boost_version} --build=missing -s compiler.cppstd=20', shell=True, check=True)
