import subprocess
import os
import shutil
from dotenv import load_dotenv

from pic_upload import upload_pics
from main import generate_all
from config import Config


SOURCE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
TARGET_DIR = os.path.join(Config.SUNRISE_PATH, 'data')

load_dotenv(os.path.join(Config.SUNRISE_PATH, '.env'))
Config.PROJECT_KEY = os.getenv('CTP_PROJECT_KEY')
Config.CLIENT_ID = os.getenv('CTP_CLIENT_ID')
Config.CLIENT_SECRET = os.getenv('CTP_CLIENT_SECRET')


def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f'Error executing command: {command}\n{stderr.decode()}')
    else:
        print(stdout.decode())
    return stdout.decode(), stderr.decode()


def copy_files(source, target):
    print(f'Copying data from {source} to {target}')
    files = os.listdir(source)
    for file in files:
        shutil.copy(os.path.join(source, file), target)


def run():
    # copy .env file to sunrise folder, if it doesn't exist there. If it does, ask user if they want to overwrite it.
    if not os.path.exists(os.path.join(Config.SUNRISE_PATH, '.env')):
        shutil.copy(os.path.join(os.path.dirname(os.path.realpath(__file__)), '.env'),
                    os.path.join(Config.SUNRISE_PATH, '.env'))
    else:
        overwrite_env = input("Overwrite .env file in sunrise folder? (y/n) ")
        if overwrite_env.lower() == 'y':
            shutil.copy(os.path.join(os.path.dirname(os.path.realpath(__file__)), '.env'),
                        os.path.join(Config.SUNRISE_PATH, '.env'))
    run_npm = input("Run cleanup before the import? (y/n) ")
    generate_all()
    copy_files(SOURCE_DIR, TARGET_DIR)
    if run_npm.lower() == 'y':
        npm_clean_commands = ['clean:categories', 'clean:products', 'clean:inventory',
                              'clean:shippingmethods', 'clean:taxCategories']
        for command in npm_clean_commands:
            run_command(f'npm --prefix {Config.SUNRISE_PATH} run {command}')

    npm_import_commands = ['import:categories', 'import:taxCategories', 'import:shippingmethods', 'import:products',
                           'import:inventory']
    for command in npm_import_commands:
        run_command(f'npm --prefix {Config.SUNRISE_PATH} run {command}')

    upload_pics()


if __name__ == '__main__':
    run()
    print("Done!")
