from typhoon.env_api.stub import clstub

class EnvironmentAPI:
    def __init__(self):
        super(EnvironmentAPI, self).__init__()

    def get_thcc_version(self):
        return clstub().get_thcc_version()

    def get_sch_examples_path(self):
        return clstub().get_sch_examples_path()

    def get_user_license_path(self):
        return clstub().get_user_license_path()

    def get_integrity_file_path(self):
        return clstub().get_integrity_file_path()

    def get_thcc_build_timestamp(self):
        return clstub().get_thcc_build_timestamp()

    def get_thcc_root_path(self):
        return clstub().get_thcc_root_path()

    def get_typhoon_user_logs_dir(self):
        return clstub().get_typhoon_user_logs_dir()

    def get_current_hil_setup(self):
        return clstub().get_current_hil_setup()

    def disconnect(self):
        return clstub().disconnect()



env_api = EnvironmentAPI()