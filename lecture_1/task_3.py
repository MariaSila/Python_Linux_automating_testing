import subprocess
import argparse
import string
import re


def check_output_command(command, content, flag=False):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    out = result.stdout
    if not flag:
        if result.returncode == 0:
            for text in content:
                if text not in out:
                    print('False')
                    break
            else:
                print('True')
    else:
        regex = re.compile('[%s]' % re.escape(string.punctuation))
        text = ' '.join(out.split())
        s = regex.sub(' ', text)
        set_words = set(s.split())
        for word in content:
            if word not in set_words:
                print('False')
                break
        else:
            print('True')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check command and output content')
    parser.add_argument('command', metavar='command', type=str, nargs=1, help='enter command')
    parser.add_argument('content', metavar='content', type=str, nargs='*', help='enter text for check')
    parser.add_argument('-w', '--word', action='store_true', help='enter word for check')
    args = parser.parse_args()
    check_output_command(args.command, args.content, args.word)
