from sshcheckers import ssh_checkout, ssh_checkout_negative, upload_files, ssh_getout
import yaml


with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestNegative:
    def save_log(self, start_time, name):
        with open(name, 'w') as file:
            file.write(ssh_getout(data['ip'], data['user'], data['passwd'], f'journalctl --since "{start_time}"'))

    def test_nstep_1(self, start_time):
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
        self.save_log(start_time, 'log_negtest1.txt')
        assert all(res), 'negtest_1 FAIL'

    def test_nstep_2(self, make_folders, clear_folders, make_bad_arx, start_time):
        # ntest2
        self.save_log(start_time, 'log_negtest2.txt')
        assert ssh_checkout_negative(data['ip'], data['user'], data['passwd'],
                                     f'cd {data["folder_out"]}; 7z e {make_bad_arx[0]} -o{data["folder_ext"]} -y',
                                     'ERROR:'), 'negtest_2 FAIL'


    def test_nstep_3(self, clear_folders, make_bad_arx, start_time):
        # ntest3
        self.save_log(start_time, 'log_negtest3.txt')
        assert ssh_checkout_negative(data['ip'], data['user'], data['passwd'],
                                 f'cd {data["folder_out"]}; 7z t {make_bad_arx[0]}', 'ERROR:'), 'negtest_3 FAIL'

    def test_nstep_4(self, start_time):
        # test4
        res = []
        res.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                f'echo {data["passwd"]} | sudo -S dpkg -r {data["package"]}',
                                'Удаляется'))
        res.append(ssh_checkout(data['ip'], data['user'], data['passwd'],
                                f'echo {data["passwd"]} | sudo -S dpkg -s {data["package"]}',
                                'Status: deinstall ok'))
        self.save_log(start_time, 'log_negtest4.txt')
        assert all(res), 'negtest4 FAIL'

