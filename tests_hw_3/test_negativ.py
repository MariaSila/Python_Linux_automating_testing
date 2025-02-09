from checkers import checkout_negative
import yaml


with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestNegative:
    def test_nstep1(self, make_folders, clear_folders, make_bad_arx):
        # ntest1
        assert checkout_negative(f'cd {data["folder_out"]}; 7z e {make_bad_arx[0]} -o{data["folder_ext"]} -y', 'ERROR:'), 'ntest_1 FAIL'


    def test_nstep2(self, clear_folders, make_bad_arx):
        # ntest2
        assert checkout_negative(f'cd {data["folder_out"]}; 7z t {make_bad_arx[0]}', 'ERROR:'), 'ntest_2 FAIL'

