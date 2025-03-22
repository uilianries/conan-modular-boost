import os
import subprocess
import argparse


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-bv', '--boost-version', type=str, default='1.87.0')
    args = arg_parser.parse_args()
    boost_version = args.boost_version

    for folder in os.listdir('.'):
        if os.path.isdir(folder) and folder.startswith('boost-'):
            print(f'Exporting {folder}')
            subprocess.run(f'conan export {folder}/all --version={boost_version}', shell=True)
    
    for folder in os.listdir('.'):
        if os.path.isdir(folder) and folder.startswith('boost-'):
            print(f'Creating {folder}')
            subprocess.run(f'conan create {folder}/all --version={boost_version} --build=missing', shell=True)
    