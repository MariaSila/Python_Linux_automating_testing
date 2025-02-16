from sshcheckers import ssh_checkout, upload_files, ssh_getout
import yaml


with open('config.yaml') as f:
    data = yaml.safe_load(f)

class TestPositive:
    def save_log(self, start_time, name):
        with open(name, 'w') as file:
            file.write(ssh_getout(data['ip'], data['user'], data['passwd'], f'journalctl --since "{start_time}"'))

    def test_step_1(self, start_time):
        # test1 deploy
        res = []
        upload_files(data['ip'], data['user'], data['passwd'], data['package']+".deb",
                     f'/home/{data["user"]}/{data["package"]}.deb')
        res.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                f'echo {data["passwd"]} | sudo -S dpkg -i /home/{data["user"]}/{data["package"]}.deb',
                                'Настраивается пакет'))
        res.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                f'echo {data["passwd"]} | sudo -S dpkg -s {data["package"]}',
                                'Status: install ok installed'))
        self.save_log(start_time, 'log_test1.txt')
        assert all(res), 'test1 FAIL'

    def test_step_2(self, make_folders, clear_folders, make_files, start_time):
        # test2
        res1 = ssh_checkout(data['ip'], data['user'], data['passwd'],
                            f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/arx -t{data["type"]}',
                            'Everything is Ok')
        res2 = ssh_checkout(data['ip'], data['user'], data['passwd'],
                            f'ls {data["folder_out"]}', f'arx.{data["type"]}')
        self.save_log(start_time, 'log_test2.txt')
        assert res1 and res2, 'test2 FAIL'

    def test_step_3(self, clear_folders, make_files, start_time):
        # test3
        res = []
        res.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/arx -t{data["type"]}',
                                'Everything is Ok'))
        res.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                f'cd {data["folder_out"]}; 7z e arx.{data["type"]} -o{data["folder_ext"]} -y',
                                'Everything is Ok'))
        for item in make_files:
            res.append(ssh_checkout(data['ip'], data['user'], data['passwd'], f'ls {data["folder_ext"]}', item))
        self.save_log(start_time, 'log_test3.txt')
        assert all(res), 'test3 FAIL'

    def test_step_4(self, start_time):
        # test4
        self.save_log(start_time, 'log_test4.txt')
        assert ssh_checkout(data['ip'], data['user'], data['passwd'],
                            f'cd {data["folder_out"]}; 7z t arx.{data["type"]}', "Everything is Ok"), 'test4 FAIL'

    def test_step_5(self, start_time):
        # test5
        self.save_log(start_time, 'log_test5.txt')
        assert ssh_checkout(data['ip'], data['user'], data['passwd'],
                            f'cd {data["folder_in"]}; 7z u arx.{data["type"]}', 'Everything is Ok'), 'test5 FAIL'

    def test_step_6(self, clear_folders, make_files, start_time):
        # test6
        res = []
        res.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/arx -t{data["type"]}',
                                'Everything is Ok'))
        for filename in make_files:
            res.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                    f'cd {data["folder_out"]}; 7z l arx.{data["type"]}', filename))
        self.save_log(start_time, 'log_test6.txt')
        assert all(res), 'test6 FAIL'

    def test_step_7(self, clear_folders, make_files, make_subfolder, start_time):
        # test7
        res = []
        res.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                f'cd {data["folder_in"]}; 7z a {data["folder_out"]}/arx -t{data["type"]}',
                                'Everything is Ok'))
        res.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                f'cd {data["folder_out"]}; 7z x arx.{data["type"]} -o{data["folder_ext2"]} -y',
                                'Everything is Ok'))
        for filename in make_files:
            res.append(ssh_checkout(data['ip'], data['user'], data['passwd'], f'ls {data["folder_ext2"]}', filename))
        res.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                f'ls {data["folder_ext2"]}', make_subfolder[0]))
        res.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                f'ls {data["folder_ext2"]}/{make_subfolder[0]}', make_subfolder[1]))
        self.save_log(start_time, 'log_test7.txt')
        assert all(res), 'test7 FAIL'

    def test_step_8(self, start_time):
        # test8
        self.save_log(start_time, 'log_test8.txt')
        assert ssh_checkout(data['ip'], data['user'], data['passwd'],
                            f'cd {data["folder_out"]}; 7z d arx.{data["type"]}', 'Everything is Ok'), 'test8 FAIL'

    def test_step_9(self, clear_folders, make_files, start_time):
        # test9
        res = []
        for filename in make_files:
            res.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                    f'cd {data["folder_in"]}; 7z h {filename}', 'Everything is Ok'))
            hash = ssh_getout(data['ip'], data['user'], data['passwd'],
                              f'cd {data["folder_in"]}; crc32 {filename}').upper()
            res.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                    f'cd {data["folder_in"]}; 7z h {filename}', hash))
        self.save_log(start_time, 'log_test9.txt')
        assert all(res), 'test9 FAIL'

    def test_step_10(self, start_time):
        # test10
        res = []
        res.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                f'echo {data["passwd"]} | sudo -S dpkg -r {data["package"]}',
                                'Удаляется'))
        res.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                f'echo {data["passwd"]} | sudo -S dpkg -s {data["package"]}',
                                'Status: deinstall ok'))
        self.save_log(start_time, 'log_test10.txt')
        assert all(res), 'test10 FAIL'


