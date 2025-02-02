from checkers import checkout
from save_output import save_crc

path_files = '/home/user/lecture/l_2/zerg/tst'
path_archive = '/home/user/lecture/l_2/zerg/out/'
path_extract = '/home/user/lecture/l_2/zerg/folder1'
text_check = 'Everything is Ok'
name_archive = 'arx2.7z'
lst_files = ['file1.txt', 'file2.txt']


def test_step_1():
    # test1 add files to archive
    result1 = checkout(f'cd {path_files} && 7z a {path_archive}{name_archive}', text_check)
    result2 = checkout(f'ls {path_archive}', name_archive)
    assert result1 and result2, 'test_1 FAIL'


def test_step_2():
    # test2 extract files from archive
    result1 = checkout(f'cd {path_archive}; 7z e {name_archive} -o{path_extract} -y', text_check)
    for file in lst_files:
        if checkout(f'ls {path_extract}', file):
            result2 = True
        else:
            result2 = False
            break
    assert result1 and result2, 'test_2 FAIL'


def test_step_3():
    # rest3 test integrity of archive
    assert checkout(f'cd {path_archive}; 7z t {name_archive}', text_check), 'test_3 FAIL'


def test_step_4():
    # test5 update files to archive
    assert checkout(f'cd {path_archive}; 7z u {name_archive}', text_check), 'test_4 FAIL'


def test_step_5():
    # test5 list contents of archive
    for file in lst_files:
        if checkout(f'cd {path_archive}; 7z l {name_archive}', file):
            result = True
        else:
            result = False
            break
    assert result, 'test_5 FAIL'


def test_step_6():
    # test6 extract files with full paths
    assert checkout(f'cd {path_archive}; 7z x {name_archive} -o{path_extract} -y',
                    text_check), 'test_6 FAIL'


def test_step_7():
    # test7 calculate hash values for files equal crc32
    result1 = checkout(f' cd {path_archive}; 7z h {name_archive}', text_check)
    if result1:
        result2 = save_crc(f'cd {path_archive}; crc32 {name_archive}')
        result3 = checkout(f' cd {path_archive}; 7z h {name_archive}', result2.upper())
    assert result1 and result3, 'test_7 FAIL'


def test_step_8():
    # test4 delete files from archive
    assert checkout(f'cd {path_archive}; 7z d {name_archive}', text_check), 'test_8 FAIL'



