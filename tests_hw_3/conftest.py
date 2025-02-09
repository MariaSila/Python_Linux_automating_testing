from checkers import checkout, getout
from datetime import datetime
import random, string, pytest, yaml


with open('config.yaml') as f:
    data = yaml.safe_load(f)

@pytest.fixture()
def make_folders():
    return checkout(f'mkdir {data["folder_in"]} {data["folder_out"]} '
                    f'{data["folder_ext"]} {data["folder_ext2"]}', '')

@pytest.fixture()
def clear_folders():
    return checkout(f'rm -rf {data["folder_in"]}/* {data["folder_out"]}/* '
                    f'{data["folder_ext"]}/* {data["folder_ext2"]}/*', '')

@pytest.fixture()
def make_files():
    list_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout(f'cd {data["folder_in"]}; dd if=/dev/urandom of={filename} '
                    f'bs={data["bs"]} count=1 iflag=fullblock', ''):
            list_files.append(filename)
    return list_files

@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout(f'cd {data["folder_in"]}; mkdir {subfoldername}', ''):
        return None, None
    if not checkout(f'cd {data["folder_in"]}/{subfoldername}; dd if=/dev/urandom '
                    f'of={testfilename} bs=1M count=1 iflag=fullblock', ''):
        return subfoldername, None
    return subfoldername, testfilename

@pytest.fixture(autouse=True)
def print_time():
    print(f'Start: {datetime.now().strftime("%H:%M:%S.%f")}')
    yield
    print(f'Finish: {datetime.now().strftime("%H:%M:%S.%f")}')

@pytest.fixture()
def make_bad_arx():
    checkout(f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/arxbad -t{data["type"]}', 'Everything is Ok')
    checkout(f'truncate -s 1 {data["folder_out"]}/arxbad.{data["type"]}', 'Everything is Ok')
    yield "arxbad"
    checkout(f'rm -f {data["folder_out"]}/arxbad.{data["type"]}', '')

@pytest.fixture(autouse=True)
def write_stat():
    yield
    stat = getout("cat /proc/loadavg")
    checkout(f"echo 'time: {datetime.now().strftime('%H:%M:%S.%f')} count:{data['count']} size: {data['bs']} load: {stat}' >> stat.txt", "")
