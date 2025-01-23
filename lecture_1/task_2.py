import subprocess
import argparse


def check_command(command, content):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if result.returncode == 0:
        out = result.stdout
        for text in content:
            if text not in out:
                print('False')
                break
        else:
            print('True')
    else:
        print('False')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check command and output content')
    parser.add_argument('command', metavar='command', type=str, nargs=1, help='enter command')
    parser.add_argument('content', metavar='content', type=str, nargs='*', help='enter text for check')
    args = parser.parse_args()
    check_command(args.command, args.content)

