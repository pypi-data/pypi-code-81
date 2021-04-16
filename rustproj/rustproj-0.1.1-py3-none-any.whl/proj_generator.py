import os
import shutil


class ProjGenerator:
    def __init__(self, dir_name, is_lib, is_both):
        self.__dir_name = dir_name
        self.__is_lib = is_lib
        self.__is_both = is_both

        self.__src_dir_path = os.path.join(self.__dir_name, "src")

    def generate(self):
        self.__create_root_dir()
        self.__create_src_dir()

        self.__create_contents()

    def __create_dir(self, dir_path=None):
        dir_path = self.__dir_name if dir_path == None else dir_path

        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        
        os.mkdir(dir_path)

    def __create_root_dir(self):
        self.__create_dir()

    def __create_src_dir(self):
        self.__create_dir(dir_path=self.__src_dir_path)

    def __create_contents(self):
        cargo_toml_file_path = os.path.join(self.__dir_name, "Cargo.toml")
        cargo_toml_contents = f"""[package]
name = "{self.__dir_name}"
version = "0.1.0"

# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html

[dependencies]
        """

        with open(cargo_toml_file_path, "w") as file:
            file.write(cargo_toml_contents)

        src_file_names = ["lib.rs", "main.rs"]
        
        if not self.__is_both:
            if self.__is_lib:
                src_file_names = [src_file_names[0]]
            else:
                src_file_names = [src_file_names[1]]

        for src_files_name in src_file_names:
            if src_files_name == "lib.rs":
                lib_rs_file_path = os.path.join(self.__src_dir_path, "lib.rs")
                with open(lib_rs_file_path, "w") as file:
                    pass
            elif src_files_name == "main.rs":
                main_rs_file_path = os.path.join(self.__src_dir_path, "main.rs")
                main_rs_contents = """
fn main() {

}
                """

                with open(main_rs_file_path, "w") as file:
                    file.write(main_rs_contents)

    