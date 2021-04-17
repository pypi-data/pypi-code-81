

class NodesLabelling:
    def lastName_and_bibKey(DG):
        def _node_lbl(u):
            data = DG.get_node_some_data(u, key_list=['year', 'name'])
            if 'name' in data:
                lbl = data['name'].split(' ')
                try:
                    int(lbl[-1])
                    lbl = lbl[-2]
                except ValueError:
                    lbl = lbl[-1]
            else:
                authors = DG[u]
                bibkey = []
                for v in authors:
                    bibkey.append(_node_lbl(v)[0])
                bibkey.sort()
                lbl = ''.join(bibkey)
                lbl += data['year'][2:]
            return lbl
        return _node_lbl
