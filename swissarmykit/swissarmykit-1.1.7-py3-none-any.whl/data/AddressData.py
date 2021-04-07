
import usaddress
import json

class AddressData:

    def __init__(self, addr=''):
        self.addr_text = addr
        self.addr = usaddress.parse(addr)
        self.data = {}
        for item in self.addr:
            k, v = item
            self.data[v] = k

    def get_state(self):
        state =  self.data.get('StateName')
        if not state:
            s = self.addr_text.split(', ')[-1].split(' ')[0].strip()
            if len(s) == 2:
                return s
        return state

    def __str__(self):
        return json.dumps(self.addr)

if __name__ == '__main__':
    addr = '123 Main St. Suite 100 Chicago, IL'
    a = AddressData(addr)
    print(a.data)
    print(a.get_state())