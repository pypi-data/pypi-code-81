import yaml
from testly import rest
import errno
import __main__



class YAMLReader:
    Restly = rest.Restly()

    def read(self, filename):
        try:
            with open(filename) as file:
                instruction_dict = yaml.load(file, Loader=yaml.FullLoader)
                #print(instruction_dict)
                self.testProcessor(instruction_dict)
                return instruction_dict
        except:
            raise FileNotFoundError(
                errno.ENOENT, __main__.os.strerror(errno.ENOENT), filename)

    def validateYAML(self):
        pass
    # def checkExist(self, filename):
    #     pass

    def writeFile(self, filename):
        pass

    def testProcessor(self, test_dictionary):

        for test_id, test_instructions in test_dictionary.items():
            print(" Test ID: {} \n".format(test_id))
            instruction_set = {}
            for key in test_instructions:
    
                instruction_set[key] = test_instructions[key]
                #print(key, test_instructions[key])

            self.Restly.executeTests(instruction_set)
