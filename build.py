import os
import subprocess
import argparse
import json
import logging


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-bv', '--boost-version', type=str, default='1.87.0')
    args = arg_parser.parse_args()
    boost_version = args.boost_version

    for folder in os.listdir('.'):
        if os.path.isdir(folder) and folder.startswith('boost-'):
            logger.info(f'Exporting {folder}')
            subprocess.run(f'conan export {folder}/all --version={boost_version}', shell=True, check=True)

    temp_dir = os.getenv('RUNNER_TEMP') or "/tmp"
    conanfile = os.path.join(temp_dir, 'conanfile.txt')
    boost_modules = []
    for folder in os.listdir('.'):
        if os.path.isdir(folder) and folder.startswith('boost-'):
            boost_modules.append(folder)
    with open(conanfile, 'w') as fd:
        fd.write("[requires]\n")
        for module in boost_modules:
            fd.write(f"{module}/{boost_version}\n")

    context = subprocess.run(f'conan graph build-order {conanfile} --format=json --build=missing -s compiler.cppstd=17', shell=True, capture_output=True, text=True, check=True)
    graph = json.loads(context.stdout)
    references = []
    for level in graph:
        for node in level:
            reference = node['ref'][:node['ref'].find('/')]
            if reference.startswith('boost-') and os.path.isdir(reference):
                references.append(reference)

    logger.info(f"Build order: {references}")

    for reference in references:
        logger.info(f'Creating {reference}')
        subprocess.run(f'conan create {reference}/all --version={boost_version} --build=missing -s compiler.cppstd=17', shell=True, check=True)
