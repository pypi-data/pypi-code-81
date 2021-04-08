class pathdict:
    
    def __init__(self, keys=[], values=[]):        
        length  = min(len(keys), len(values))
        self.__keys  = list(keys)[:length]
        self.__values  = list(values)[:length]
        
        self.__no_dupes()
        
     
    def __repr__(self):
        return str(self.todict())
    
    
    def __setitem__(self, key, value):
        if key in self.__keys:
            self.__values[self.__keys.index(key)] = value
        
        elif isinstance(key, tuple):
            try:
                for index, v in zip(key, value):
                    self.__values[self.__keys.index(index)] = v
            except ValueError:
                self.__error(KeyError, index, "key", "not found")
        
        elif isinstance(key, list):
            try:
                if len(key) == 1:
                    self.__values[self.__keys.index(key[0])] = value
                else:
                    self.__values[self.__keys.index(key[0])][key[1:]] = value
            except ValueError:
                self.__error(KeyError, key[0], "key", "not found") 
        
        else:
            self.__error(KeyError, key, "key", "not found")
    
    def __getitem__(self, key):
        if key in self.__keys:
            return self.__values[self.__keys.index(key)]
        
        elif isinstance(key, tuple):
            try: 
                res = []
                for index in key:
                    res.append(self.__values[self.__keys.index(index)])
                return self.pathdict_values(res)
            except ValueError:
                self.__error(KeyError, index, "key", "not found")
        
        elif isinstance(key, list):
            try:
                if len(key) == 1:
                    return self.__values[self.__keys.index(key[0])]
                else:
                    return self.__values[self.__keys.index(key[0])][key[1:]]
            except ValueError:
                self.__error(KeyError, key[0], "key", "not found")             
        
        else:
            self.__error(KeyError, key, "key", "not found")
        
    def __len__(self):
        return len(self.__keys)
    
    def __sizeof__(self):
        return self.__keys.__sizeof__() + self.__values.__sizeof__()
    
    
    # contains
    def __contains__(self, key):
        return self.pathdict_keys(self.__keys).__contains__(key)
    
    
    # iter
    def __iter__(self):
        for keys, value in zip(self.__keys, self.__values):
            yield keys, value
    
    def __reversed__(self):
        return self.pathdict_keys(self.__keys).__reversed__()
    
    
    # equal
    def __eq__(self, other):
        if other.__class__ is self.__class__:
            return self.__keys + self.__values == other._keys + other._values
        elif other.__class__ is dict().__class__:
            return self.__keys + self.__values == list(other.keys()) + list(other.values())
        else:
            return NotImplemented
    
    def __ne__(self, other):
        if other.__class__ is self.__class__:
            return self.__keys + self.__values != other._keys + other._values
        elif other.__class__ is dict().__class__:
            return self.__keys + self.__values != list(other.keys()) + list(other.values())
        else:
            return NotImplemented
    
       
    # add
    def __add__(self, other):
        if other.__class__ is self.__class__:
            return pathdict(self.__keys + other._keys, self.__values + other._values)
        elif other.__class__ is dict().__class__:
            return pathdict(self.__keys + list(other.keys()), self.__values + list(other.values()))
        else:
            return NotImplemented

    def __radd__(self, other):
        if other.__class__ is dict().__class__:
            return pathdict(list(other.keys()) + self.__keys, list(other.values()) + self.__values)
        else:
            return NotImplemented

    def __iadd__(self, other):
        if other.__class__ is self.__class__:
            self.__keys += other._keys
            self.__values += other._keys
            self.__no_dupes()
            return self
        elif other.__class__ is dict().__class__:
            self.__keys += list(other.keys())
            self.__values += list(other.values())
            self.__no_dupes()
        else:
            return NotImplemented


    # private
    def __error(self, error, value, before, after):
        if isinstance(value, (int, float)):
            raise error(f"{before} {value} {after}")
        else:
            raise error(f'{before} "{value}" {after}')
    
    def __no_dupes(self):
        d = self.todict()
        self.__keys, self.__values = list(d.keys()), list(d.values())
    

    
    # items
    def items(self):
        """Return a list-like object of pathdict's items."""
        return self.pathdict_items(self.__keys, self.__values)
    
    def keys(self):
        """Return a list-like object of pathdict's keys."""
        return self.pathdict_keys(self.__keys)
    
    def values(self):
        """Return a list-like object of pathdict's values."""
        return self.pathdict_values(self.__values)
       
    
    # create
    @staticmethod
    def frompairs(pairs):
        """Create a pathdict from key/value pairs."""
        keys, values = zip(*pairs)
        return pathdict(keys, values)
    
    @staticmethod
    def fromkeys(keys, value=None):
        """Create a pathdict from iterable with set values."""
        return pathdict(keys, [value]*len(keys))
    
    @staticmethod
    def fromdict(d: dict):
        """Create a pathdict from dictionary."""
        return pathdict(d.keys(), d.values())
    
    def todict(self):
        """Return the pathdict as a dictionary."""
        return dict(zip(self.__keys, self.__values))
    
         
    # return
    def copy(self):
        """Return a shallow copy of the pathdict."""
        return pathdict(self.__keys, self.__values)
    
    def get(self, key, default=None):
        """Return the value for key if key is in pathdict, else return default."""
        if key in self.__keys:
            return self.__values[self.__keys.index(key)]
        elif default != None:
            return default
            
        
    # update/add
    def update(self, d):
        """Update the pathdict with the elements from another pathdict, dict or an iterable with key/value pairs.
        
        If a key already exists, it's corresponding value gets replaced"""
        if isinstance(d, (pathdict, dict)):
            d = d.items()
        
        for key, value in d:
            self.append(key, value, replace=True)
    
    def append(self, key, value, replace=False):
        """Append a key with a value to the end of the pathdict.
        
        If the key already exists and replace == False, KeyError is raised, otherwise the corresponding value gets replaced."""
        if key not in self.__keys:
            self.__keys.append(key)
            self.__values.append(value)
        
        elif replace:
            self.__values[self.__keys.index(key)] = value
        else:
            self.__error(KeyError, key, "key", "already exists")
    
    def extend(self, keys, values, replace=False):
        """Extend pathdict by appending keys and values from the two iterables.
        
        If one of the keys already exists and replace == False, KeyError is raised, otherwise the corresponding value gets replaced."""
        for key, value in zip(keys, values):
            self.append(key, value, replace)
    
    def insert(self, index: int, key, value):
        """Insert a key with a value before the index.
        
        If the key already exists, KeyError is raised"""
        if key not in self.__keys:
            self.__keys.insert(index, key)
            self.__values.insert(index, value)
        else:
            self.__error(KeyError, key, "key", "already exists")
    
    def replace(self, key, value):
        """Replaces the corresponding value of the key.
        
        If key is not found, KeyError is raised"""
        if key in self.__keys:
            self.__values[self.__keys.index(key)] = value
        else:
            self.__error(KeyError, key, "key", "not found")
            
    def setdefault(self, key, default=None):
        """Append key with a value of default, if key is not in the pathdict, and return default.
        
        If key is in the pathdict, return the corresponding value for key."""
        if key not in self.__keys:
            self.__keys.append(key)
            self.__values.append(default)
            return default
        else:
            return self.__values[self.__keys.index(key)]
    
    
    # remove
    def pop(self, key, default=None):
        """Remove the specified key and return the corresponding value.
        
        If key is not found, return default if given, otherwise KeyError is raised."""
        if key in self.__keys:
            index = self.__keys.index(key)
            self.__keys.pop(index)
            return self.__values.pop(index)
        
        elif default != None:
            return default
        else:
            self.__error(KeyError, key, "key", "not found")
    
    def popitem(self):
        """Remove and return a (key, value) pair as a 2-tuple.
        
        Last pair in the pathdict is returned.
        Raises KeyError if pathdict is empty."""
        if len(self.__keys) == 0:
            raise KeyError(f"pathdict is empty")
        else:
            return self.__keys.pop(-1), self.__values.pop(-1)
    
    def remove(self, value):
        """Remove the first occurrence of value and it's corresponding key.
        
        If value is not found, ValueError is raised"""
        if value in self.__values:
            index = self.__values.index(value)
            self.__keys.pop(index)
            self.__values.pop(index)
        else:
            self.__error(ValueError, value, "value", "not found")
        
    def delete(self, key):
        """Remove the given key and the corresponding value.
        
        If key is not found, KeyError is raised"""
        if key in self.__keys:
            index = self.__keys.index(key)
            self.__keys.pop(index)
            self.__values.pop(index)
        else:
            self.__error(KeyError, key, "key", "not found")
    
    
    def clear(self):
        """Remove all items from pathdict."""
        self.__keys.clear()
        self.__values.clear()
        
    
    # count/find
    def count(self, value):
        """Return number of occurrences of value."""
        return self.__values.count(value)
    
    def find(self, value):
        """Return the first key of value.
        
        If value is not found, ValueError is raised"""
        if value in self.__values:
            return self.__keys[self.__values.index(value)]
        else:
            self.__error(ValueError, value, "value", "not found")
            
    def rfind(self, value):
        """Return the last key of value.
        
        If value is not found, ValueError is raised"""
        if value in self.__values:
            return self.__keys[::-1][self.__values[::-1].index(value)]
        else:
            self.__error(ValueError, value, "value", "not found")
    
    
    # swap/reverse
    def swap(self):
        """Swap keys with values."""
        self.__keys, self.__values = self.__values, self.__keys
    
    def reverse(self):
        """Reverse keys and values in-place."""
        self.__keys.reverse()
        self.__values.reverse()
        
    def reverse_keys(self):
        """Reverse keys in-place."""
        self.__keys.reverse()
        
    def reverse_values(self):
        """Reverse values in-place."""
        self.__values.reverse()
    
    
    # sort
    def sort(self):
        """Sort keys and values in ascending order and in-place."""
        self.__keys.sort()
        self.__values.sort()
        
    def sort_keys(self):
        """Sort keys in ascending order and in-place."""
        self.__keys.sort()
        
    def sort_values(self):
        """Sort values in ascending order and in-place."""
        self.__values.sort()
    
   
   
    # subclass
    class pathdict_keys:
        def __init__(self, keys):
            self.__keys = list(keys)
            
        def __repr__(self):
            return f"pathdict_keys({self.__keys})"
        
        def __getitem__(self, key):
            if isinstance(key, int):
                return self.__keys[key]
            elif isinstance(key, slice):
                return pathdict_keys(self.__keys[key])
            elif isinstance(key, (tuple, list)):
                try: 
                    res = []
                    for index in key:
                        res.append(self.__keys[index])
                    return pathdict_keys(res)
                except IndexError:
                    raise IndexError(f"key index out of range")
            else:
                raise TypeError(f"key indices must be integers, slices or tuples, not {key.__class__.__name__}")
                
        def __len__(self):
            return len(self.__keys)
        
        
        def __iter__(self):
            for key in self.__keys:
                yield key
        
        def __reversed__(self):
            for key in self.__keys.__reversed__():
                yield key
                
        def __contains__(self, key):
            return self.__keys.__contains__(key)
        
        
        def topathdict(self, value):
            return pathdict(self.__keys, [value]*len(self.__keys))
            
         
    class pathdict_values:
        def __init__(self, values):
            self.__values = list(values)
            
        def __repr__(self):
            return f"pathdict_values({self.__values})"
        
        
        def __getitem__(self, key):
            if isinstance(key, int):
                return self.__values[key]
            elif isinstance(key, slice):
                return pathdict_values(self.__values[key])
            elif isinstance(key, tuple):
                try: 
                    res = []
                    for index in key:
                        res.append(self.__values[index])
                    return pathdict_values(res)
                except IndexError:
                    raise IndexError(f"value index out of range")
            else:
                raise TypeError(f"value indices must be integers, slices or tuples, not {key.__class__.__name__}")
        
        def __len__(self):
            return len(self.__values)        
        
        
        def __iter__(self):
            for value in self.__values:
                yield value
        
        def __reversed__(self):
            for value in self.__values.__reversed__():
                yield value
            

    class pathdict_items:
        def __init__(self, keys, values):
            self.__items = list(zip(keys, values))

        def __repr__(self):
            return f"pathdict_items({list(self.__items)})"

        def __getitem__(self, key):
            if isinstance(key, int):
                return self.__items[key]
            elif isinstance(key, slice):
                return pathdict_items(self.__items[key])
            elif isinstance(key, (tuple, list)):
                try: 
                    res = []
                    for index in key:
                        res.append(self.__items[index])
                    return pathdict_items(res)
                except IndexError:
                    raise IndexError(f"value index out of range")
            else:
                raise TypeError(f"value indices must be integers, slices or tuples, not {key.__class__.__name__}")

        def __len__(self):
            return len(self.__items)
            
            
        def __iter__(self):
            for item in self.__items:
                yield item
        
        def __reversed__(self):
            for item in self.__items.__reversed__():
                yield item
                
        def __contains__(self, key):
            return self.__items.__contains__(key)
            
        def topathdict(self):
            keys, values = zip(*self.__items)
            return pathdict(keys, values)
        



