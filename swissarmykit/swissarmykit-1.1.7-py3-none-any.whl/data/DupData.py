from pprint import pprint

class DupData:

    def __init__(self):
        self.data = {}
        self.dup_lst = []
        self.count = 0

    def check(self, data, ref=1):
        ''' data: url or name
            id: ref
        '''

        if data in self.data:
            self.dup_lst.append((ref, data, self.data.get(data)))
            self.count += 1

        self.data[data] = ref

        sorted(self.dup_lst, key=lambda x: x[0])


    def print_dup(self):
        print('Total duplicate: ', self.count)
        for row in self.dup_lst:
            print(row[0], '  ', row[1], '  ', row[2])

if __name__ == '__main__':
    d = DupData()