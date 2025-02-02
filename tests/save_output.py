import subprocess


def save_crc(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if result.returncode == 0:
        return result.stdout


if __name__ == '__main__':
    print(save_crc('cd /home/user/lecture/l_2/zerg/out/; crc32 arx2.7z'))

