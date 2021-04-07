from typing import List


class Progress(object):
    _id: str
    _overall: dict
    _items: List

    def __init__(self, id, progress=None):
        self._id = id

        if progress:
            self._overall = progress.get('overall')
            self._items = [Progress(id=item['id'], progress=item) for item in progress['items']]
        else:
            self._overall = {
                'ready': False,
                'page': 1,
                'count': 0,
            }
            self._items = []

    def __getitem__(self, item):
        items = [i for i in self._items if i._id == item]
        if len(items) == 0:
            item = Progress(id=item)
            self._items.append(item)
            return item
        if len(items) == 1:
            return items[0]
        return None

    def update(self, ready, count=None, page=None):
        self._overall['ready'] = ready

        if count:
            self._overall['count'] = count
        if page:
            self._overall['page'] = page

    def to_dict(self):
        return {
            'id': self._id,
            'overall': {
                'ready': self.is_ready(),
                'page': self.get_page(),
                'count': self.count(),
                'children_count': self.children_count(),
                'children_ready_count': self.children_ready_count()
            },
            'items': [item.to_dict() for item in self._items]
        }

    def is_ready(self):
        # Leaf node, return ready state
        if len(self._items) == 0:
            return self._overall['ready']
        else:
            # Compute downwards the ready state
            is_ready = True
            for item in self._items:
                is_ready = is_ready and item.is_ready()
            return is_ready

    def get_page(self):
        return self._overall['page']

    # Only for UI
    def count(self):
        return self._overall['count']

    # Only for UI
    def children_count(self):
        return len(self._items)

    # Only for UI
    def children_ready_count(self):
        return len([i for i in self._items if i.is_ready()])
