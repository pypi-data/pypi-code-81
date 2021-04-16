from pencil_pusher.process_util import ProcessUtil


class Documenter:
    @staticmethod
    def install():
        """
        installs the correct pydoc-markdown package
        to the python version being used to execute
        the commands
        """
        ProcessUtil.execute(
            ["python3", "-m", "pip", "install", "pydoc-markdown"]
        )

    @staticmethod
    def generate(module: str, title: str = "", output_dir: str = "./"):
        """
        Generates markdown documentation for a given
        module (.py file) and creates a file with the
        name title as the documentation output

        Args:
            module (str): the name of the module the file is being
                imported from
            title (str): the title of the document file to output
            output_dir (str): the directory to write the output file to
        """
        options = '{renderer: {type: markdown,descriptive_class_title: false,render_toc: true, header_level_by_type: {"Module": 1,"Class": 2,"Method": 3,"Function": 2,"Data": 2}}}'
        if not output_dir.endswith("/"):
            output_dir += "/"

        fp = open(f"{output_dir}{title}.md", "w")
        ProcessUtil.execute(
            ["pydoc-markdown", "-m", f"{module}", options], stdout=fp
        )
        fp.close()
