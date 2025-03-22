import os
import subprocess
import argparse
import json


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-bv', '--boost-version', type=str, default='1.87.0')
    args = arg_parser.parse_args()
    boost_version = args.boost_version

    for folder in os.listdir('.'):
        if os.path.isdir(folder) and folder.startswith('boost-'):
            print(f'Exporting {folder}')
            subprocess.run(f'conan export {folder}/all --version={boost_version}', shell=True)
    
    temp_dir = os.getenv('RUNNER_TEMP') or "/tmp"
    conanfile = f'{temp_dir}/conanfile.txt'
    boost_modules = []
    for folder in os.listdir('.'):
        if os.path.isdir(folder) and folder.startswith('boost-'):
            boost_modules.append(folder)
    with open(conanfile, 'w') as fd:
        fd.write("[requires]\n")
        for module in boost_modules:
            fd.write(f"{module}/{boost_version}\n")

    context = subprocess.run(f'conan graph build-order {conanfile} --format=json', shell=True, capture_output=True, text=True)
    graph = json.loads(context.stdout)
    references = []
    for level in graph:
        for node in level:
            reference = node['ref'][:node['ref'].find('/')]
            if reference.startswith('boost-') and os.path.isdir(reference):
                references.append(reference)
    
    print("Build order:")
    for reference in references:
        print(reference)

    for reference in references:
        print(f'Creating {reference}')
        subprocess.run(f'conan create {reference}/all --version={boost_version} --build=missing', shell=True)
