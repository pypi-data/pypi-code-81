import networkx as nx
import copy
# import nxviz

class Person(object):
    def __init__(self, HLID, gender = None, rel_head = None):
        
        self.HLID = HLID
        self.gender = gender
        self.rel_head = rel_head
        
        self.father = None
        self.mother = None
        self.married = None
    
    def has_father(self):
        return(self.father is not None)
    
    def has_mother(self):
        return(self.mother is not None)
    
    def is_married(self):
        if self.married is None:
            return(False)
        
        return(self.married)
    
    def __repr__(self):
        return(str(self.HLID))
                
class Family(object):
    
    def __init__(self, members={}):
        self.members = {}
        self.vgraph = nx.DiGraph()
        self.hgraph = nx.Graph()
        self.head = None
        
        for member_HLID, member in members.items():
            self.add_member(member)
    
    def _add_node(self, member):
        assert isinstance(member, Person)
        self.vgraph.add_node(member.HLID)
        self.hgraph.add_node(member.HLID)
    
    def _has_node(self, member):
        assert isinstance(member, Person)
        return(self.vgraph.has_node(member.HLID))
    
    def _add_edge(self, source, dest, rel_type, graph='v'):
        assert isinstance(source, Person)
        assert isinstance(dest, Person)
        
        if graph == 'v':
            self.vgraph.add_edge(source.HLID, dest.HLID, rel_type=rel_type)
        elif graph == 'h':
            self.hgraph.add_edge(source.HLID, dest.HLID, rel_type=rel_type)
        
    def add_member(self, member):
        assert isinstance(member, Person)
        
        #it is important to update the member 
        #because the member could be present because parent of another member
        #but with no information on member's parent 
        self.members[member.HLID] = member
        
        if not self._has_node(member):
            self._add_node(member)
        
        has_father = False
        has_mother = False
        
        if member.has_father(): #person has father.HLID
            father = member.father
            
            if not self._has_node(father): #father not in the graph
                self.add_member(father)
            self.add_v_edge(father, member, 'father')
            has_father = True
            
        if member.has_mother(): 
            mother = member.mother
            if not self._has_node(mother):
                self.add_member(mother)
            self.add_v_edge(mother, member, 'mother')
            has_mother = True
            
        if has_father and has_mother: 
            if not self.are_partners(mother, father):
                self.add_h_edge(father, mother, 'partner')
            
            children_father = [ch.HLID for ch in self.get_children(father)]
            children_mother = [ch.HLID for ch in self.get_children(mother)]
            
            siblings = set.intersection(set(children_father), set(children_mother))
            
            for s in list(siblings):
                if s != member.HLID:
                    sibling = self.get_person(s)
                    self.add_h_edge(member, sibling, 'sibling')
            
    def is_member(self, member):
        assert isinstance(member, Person)
        return(self._has_node(member))
    
    def find_head(self):
        for member_HLID in self.members.keys():
            member = self.members[member_HLID]
            if member.rel_head == 1:
                self.head = member.HLID
                break

    def get_person(self, member_HLID):
        assert self.vgraph.has_node(member_HLID)
        return(self.members[member_HLID])
    
    def get_node(self, member_HLID):
        assert self.vgraph.has_node(member_HLID)
        return(self.graph[member_HLID])
    
    ############### The following methods operate on the graph
    #HAS RELATIVE
    def has_parent(self, member, parent):
        assert self.is_member(member)
        if parent == 'father':
            return(member.father is not None)
        elif parent == 'mother':
            return(member.mother is not None)
        
        return(False)
    
    def has_father(self, member):
        assert self.is_member(member)
        return(self.has_parent(member, 'father'))
        
    def has_mother(self, member):
        assert self.is_member(member)
        return(self.has_parent(member, 'mother'))
    
    def is_orphan(self, member):
        if self.has_father(member) or self.has_mother(member):
            return(False)
        return(True)
    
    def has_partners(self, member):
        assert self.is_member(member)
        relationships = [data['rel_type'] for source, dest, data in self.hgraph.edges(member.HLID, data=True)]
        if 'partner' in relationships:
            return(True)
        return(False)

    def has_siblings(self, member):
        assert self.is_member(member)
        relationships = [data['rel_type'] for source, dest, data in self.hgraph.edges(member.HLID, data=True)]
        if 'sibling' in relationships:
            return(True)
        return(False)


    def get_partners(self, member):
        assert self.has_partners(member)
        
        partners = []
        for s_HLID, d_HLID, data in self.hgraph.edges(member.HLID, data=True):
            if data['rel_type'] == 'partner':
                partners.append(self.members[d_HLID])
        
        return(partners)
    
    def are_partners(self, member1, member2):
        if not self.has_partners(member1):
            return(False)
        
        if not self.has_partners(member2):
            return(False)
        
        partners = self.get_partners(member1)
        partners_HLID = [p.HLID for p in partners]
                
        return(member2.HLID in partners_HLID)
    
    def requires_partner(self, member, gender='M'):
        #if already has a partner, return False
        if self.has_partners(member):
            return(False)
    
        #TODO manage homosexual couples
        if member.gender == gender:
            return(False)
        
        if member.married: # MICS report it is married but it is not in a union
            return(True)
    
    def requires_parent(self, member, parent='father'):
        if self.has_parent(member, parent):
            return(False)
        return(True)
    
    #GET RELATIVE
    def _get_parent(self, member, parent):
        assert self.is_member(member)
        if parent == 'father':
            if self.has_father(member):
                return(self.get_person(member.father.HLID))
        elif parent == 'mother':
            if self.has_mother(member):
                return(self.get_person(member.mother.HLID))
        return(None)
    
    def get_father(self, member):
        return(self._get_parent(member, 'father'))
    
    def get_mother(self, member):
        return(self._get_parent(member, 'mother'))
    
    def get_parents(self, member):
        assert self.is_member(member)
        parents = [source for source, dest, data in self.vgraph.in_edges(member.HLID, data=True)]
        return([self.get_person(p) for p in parents])
    
    def get_children(self, member):
        assert self.is_member(member)
        children = [dest for source, dest, data in self.vgraph.out_edges(member.HLID, data=True)]
        return([self.get_person(ch) for ch in children])
    
    def get_siblings(self, member):
        assert self.has_siblings(member)
        
        siblings = []
        for s_HLID, d_HLID, data in self.hgraph.edges(member.HLID, data=True):
            if data['rel_type'] == 'sibling':
                siblings.append(self.members[d_HLID])
        
        return(siblings)
   
    #ADD
    def add_h_edge(self, member1, member2, rel_type):
        assert self.is_member(member1)
        assert self.is_member(member2)
        self.hgraph.add_edge(member1.HLID, member2.HLID, rel_type = rel_type)
    
    def add_v_edge(self, parent, child, rel_type):
        assert self.is_member(parent)
        assert self.is_member(child)
        self.vgraph.add_edge(parent.HLID, child.HLID, rel_type = rel_type)
    
    def __repr__(self):
        A = nx.adjacency_matrix(self.vgraph)
        return(str(A.todense()))

#%%
def create_family(hh_df):
    members = {}
    
    for i_row in range(hh_df.shape[0]):
    
        curr_row = hh_df.iloc[i_row, :]
        member_HLID = curr_row['HLID']
        rel_head = curr_row['HL3']
        gender = curr_row['HL4']
        married = curr_row['MA']<3
        
        gender_MF = 'M' if gender == 1 else 'F'
        
        curr_member = Person(member_HLID, gender=gender_MF, rel_head=rel_head)
        curr_member.married = married
        
        father_HLID = curr_row['father_HLID']
        mother_HLID = curr_row['mother_HLID']
        
        #%
        
        if not father_HLID[-2:] in ['-1', '_0', '99']:
            father = Person(father_HLID, 'M')
            curr_member.father = father
        
        #%
        if not mother_HLID[-2:] in ['-1', '_0', '99']:
            mother = Person(mother_HLID, 'F')
            curr_member.mother = mother
        
        #%
        members[curr_member.HLID] = curr_member    
    
    family = Family(members)
    return(family)
        
def plot_family(family):
    gv = family.vgraph
    gh = family.hgraph
    pos = nx.planar_layout(gv)
    nx.draw(gh, pos, with_labels=True)
    nx.draw(gv, pos, with_labels=True)
    nx.draw_networkx_edge_labels(gh,pos,edge_labels=nx.get_edge_attributes(gh, 'rel_type'))
    nx.draw_networkx_edge_labels(gv,pos,edge_labels=nx.get_edge_attributes(gv, 'rel_type'))

def get_floating_nodes(family):
    #check if there are non liked nodes
    gv = family.vgraph
    gh = family.hgraph
    node_to_process = []
    for node in gv.nodes():
        if len(gv.in_edges(node)) == 0 and len(gv.out_edges(node)) == 0 and len(gh.edges(node)) == 0:
            node_to_process.append(node)
    return(node_to_process)

def fix_floating(family, return_pre = False):
    family.find_head()
    
    head = family.members[family.head]
    head_gender = head.gender
    
    node_to_process = get_floating_nodes(family)
    n_pre = len(node_to_process)
    family_before = copy.deepcopy(family)
    
    if n_pre > 0:
        #FIX PARENTS, PARTNERS, CHILDREN
        n_after = n_pre-1
        while(n_after<n_pre):
            n_pre = len(node_to_process)
            
            for nd in node_to_process:
                rel_head = family.members[nd].rel_head
                node = family.members[nd]
               
                if rel_head == 2: #partner
                    family.add_h_edge(head, node, 'partner')
                    
                elif rel_head == 3: #child
                    rel_type = 'father' if head_gender == 'M' else 'mother'
                    family.add_v_edge(head, node, rel_type)
                
                elif rel_head == 4: #child in law
                    #chech if there are married head's child with no union
                    
                    children = family.get_children(head)
                    children_with_no_partner = []
                    for child in children:
                        if family.requires_partner(child, node.gender):
                            children_with_no_partner.append(child)
                            
                    if len(children_with_no_partner) ==  1:
                        child = children_with_no_partner[0]
                        family.add_h_edge(child, node, 'partner')
                        
                    elif len(children_with_no_partner) > 1: #CHECK CORRECT?
                        #just pick the first, lucky him/her!
                        child = children_with_no_partner[0]
                        family.add_h_edge(child, node, 'partner')
                        
                elif rel_head == 6: #parent
                    node_gender = node.gender
                    rel_type = 'father' if node_gender == 'M' else 'mother'
                    family.add_v_edge(node, head, rel_type)
                
                elif rel_head == 7: #parent in law
                    missing_parent = 'father' if node.gender == 'M' else 'mother'
                    
                    if family.has_partners(head): #head has partners
                        
                        partners = family.get_partners(head)
                        
                        #chech if there are partners with no parents
                        partners_with_no_parent = []
                        for partner in partners:
                            if family.requires_parent(partner, missing_parent):
                                partners_with_no_parent.append(partner)
                                
                        if len(partners_with_no_parent) >= 1: #if more then one, pick the first
                            family.add_v_edge(node, partners_with_no_parent[0], missing_parent)
                
                elif rel_head == 9: #sibling in law
                    # partner of sibling ?
                    head_has_siblings = family.has_siblings(head)
                    
                    head_has_partners = False
                    if family.has_partners(head):
                        head_has_partners = True
                    
                    if head_has_siblings and not head_has_partners:
                        #search for married siblings
                        siblings = family.get_siblings(head)
                        candidate_siblings = []
                        for sibling in siblings:
                            if sibling.HLID != head.HLID:
                                if family.requires_partner(sibling, node.gender):
                                    candidate_siblings.append(sibling)
                        
                        if len(candidate_siblings) ==  1:
                            family.add_h_edge(candidate_siblings[0], node, 'partner')
                    
                elif rel_head == 13: #stepchild
                    rel_type = 'father' if head_gender == 'M' else 'mother'
                    family.add_v_edge(head, node, rel_type)
    
            node_to_process = get_floating_nodes(family)
            n_after = len(node_to_process)
        
        #FIX OTHER RELATIONSHIPS
        n_pre = len(node_to_process)
        n_after = n_pre-1
        while(n_after<n_pre):
            n_pre = len(node_to_process)
            
            for nd in node_to_process:
                rel_head = family.members[nd].rel_head
                node = family.members[nd]
                
                if rel_head == 4: #child in law
                    rel_type = 'father-in-law' if head_gender == 'M' else 'mother-in-law'
                    family.add_v_edge(head, node, rel_type)
                        
                elif rel_head == 5: #grandchild
                    #if a grandchild is with no edges, it means his/her parent are missing
                    rel_type = 'grandfather' if head_gender == 'M' else 'grandmother'
                    family.add_v_edge(head, node, rel_type)
                
                elif rel_head == 7: #parent in law
                    # print(nd, rel_head, stop)
                    rel_type = 'father-in-law' if node.gender == 'M' else 'mother-in-law'
                    family.add_v_edge(node, head, rel_type)
                        
                elif rel_head == 8: #sibling
                    family.add_h_edge(head, node, 'sibling')
                
                elif rel_head == 9: #sibling in law
                    # partner of sibling
                    # OR
                    # sibling of partner
                    
                    head_has_siblings = family.has_siblings(head)
                    
                    head_has_partners = False
                    if family.has_partners(head):
                        partners = family.get_partners(head)
                        head_has_partners = True
                    
                    #1.hopefully head has no siblings and has a partner
                    if not head_has_siblings and head_has_partners:
                        
                        #there should be at least one partner with no parents
                        candidate_partners = []
                        for partner in partners:
                            if family.is_orphan(partner):
                                candidate_partners.append(partner)
                        
                        #in case, just assign the node as sibling of the first
                        if len(candidate_partners)>=1:
                            family.add_h_edge(candidate_partners[0], node, 'sibling')
                    
                    elif head_has_siblings and not head_has_partners:
                        pass #this step was considered previously
                    
                    else: #has both partners and siblings
                        family.add_h_edge(head, node, 'sibling_in_law') 
                
                elif rel_head == 10: #uncle/aunt
                    #THIS IS COMPLICATED, 
                    #FOR NOW LETS JUST ADD A LINK
                    rel_type = 'uncle' if node.gender == 'M' else 'aunt'
                    family.add_v_edge(node, head, rel_type)
                    
                    #flag to check later
                    # print(head.HLID, node.HLID, rel_head)
                    #messy code below
                    '''
                    has_father_gp = False
                    has_mother_gp = False
                    
                    if family.has_father(head):
                        father_head = family.get_father(head)
                        if father_head.father is not None or father_head.mother is not None:
                            has_father_gp = True
                       
                    if family.has_mother(head):
                        mother_head = family.get_mother(head)
                        if mother_head.father is not None or mother_head.mother is not None:
                            has_mother_gp = True
                    
                    #the only way to be sure which head's parent the uncle/aunt is sibling of
                    #is if only one of the head's parents has no parents
                    if has_father_gp  != has_mother_gp:
                        if has_father_gp: 
                            if family.has_mother(head):
                                mother_head = family.get_mother(head)
                                family = add_sibling(father_head, node)
                        else:
                            if family.has_mother(head):
                                father_head = family.get_father(head)
                                family = add_sibling(father_head, node)
                            
                    #otherwise... just pick one parent
                    #add_sibling(parent, node)
                    '''
                    
                elif rel_head == 11: #nephew/niece by blood
                    #THIS IS COMPLICATED, 
                    #FOR NOW LETS JUST ADD A LINK
                    rel_type = 'uncle' if head.gender == 'M' else 'aunt'
                    family.add_v_edge(head, node, rel_type)
                    
                    #flag to check later
                    # print(head.HLID, node.HLID, rel_head)
                    '''
                    #child of a sibling of the head
                    
                    #if node has parents
                    #    one of the parent is a sibling of the head's parent
                    
                    #if node has no parents
                    #    do nothing
                    # TODO: Add weights, in this case we could add a childship with low weight
                    '''
                    
                elif rel_head == 15: #nephew/niece by marriage
                    #THIS IS COMPLICATED, 
                    #FOR NOW LETS JUST ADD A LINK
                    rel_type = 'uncle' if head.gender == 'M' else 'aunt'
                    family.add_v_edge(head, node, rel_type)
                    
                    #flag to check later
                    # print(head.HLID, node.HLID, rel_head)
                    '''
                    #child of a sibling of the head's parner
                    
                    #if node has parents
                    #    one of the parent is a sibling of the head's parent
                    
                    #if node has no parents
                    #    do nothing
                    # TODO: Add weights, in this case we could add a childship with low weight
                    '''
                    
                elif rel_head == 12: #other relative
                    #other relative???
                    #add low weight edge?
                    pass
                    
                elif rel_head == 16: #cousin
                    #THIS IS COMPLICATED, 
                    #FOR NOW LETS JUST ADD A LINK
                    family.add_h_edge(head, node, 'cousin')
                    
                    #flag to check later
                    # print(head.HLID, node.HLID, rel_head)
                    '''
                    #if node has parents
                    #   one node parent is a sibling of one head's parent
                    #else
                    # do nothing
                    family.add_relationship(head, node, 'cousin')
                    print(hhid, rel_head)
                    '''
                
                elif rel_head == 17: #grandparent
                    #if a grandparent is with no edges, it means child's parents are missing
                    rel_type = 'grandfather' if node.gender == 'M' else 'grandmother'
                    family.add_v_edge(node, head, rel_type)
    
            node_to_process = get_floating_nodes(family)
            n_after = len(node_to_process)

    if return_pre:
        return(family, family_before)
    else:
        return(family)
    
    
'''
#%%
import pandas as pd
hh_df = pd.read_csv('/home/bizzego/UniTn/software/mics_library/sample_hh_df.csv', index_col=0)

family = create_family(hh_df)

plot_family(family)

#%%
family = Family()

for i_row in range(hh_df.shape[0]):#%%    
    curr_row = hh_df.iloc[i_row, :]
    member_HLID = curr_row['HLID']
    rel_head = curr_row['HL3']
    gender = curr_row['HL4']
    married = curr_row['MA']<3
    
    gender_MF = 'M' if gender == 1 else 'F'
    
    curr_member = Person(member_HLID, gender=gender_MF, rel_head=rel_head)
    curr_member.married = married
    
    father_HLID = curr_row['father_HLID']
    mother_HLID = curr_row['mother_HLID']
    
    #%
    
    if not father_HLID[-2:] in ['-1', '_0', '99']:
        father = Person(father_HLID, 'M')
        curr_member.father = father
    
    #%
    if not mother_HLID[-2:] in ['-1', '_0', '99']:
        mother = Person(mother_HLID, 'F')
        curr_member.mother = mother
    
    family.add_member(curr_member)
        
plot_family(family)
i_row+=1

#%%
person1 = family.members['HLID_1']
person2 = Person('HLID_37', 'M')
person2.father = Person('HLID_38', 'M')
person2.mother = Person('HLID_10', 'F')

person3 = family.members['HLID_30']

#%%
assert family.is_member(person1)
assert not family.is_member(Person('HLID_37'))

assert family.has_parent(person1, 'father')
assert family.has_parent(person1, 'mother')

assert not family.has_parent(Person('HLID_30'), 'father')
assert not family.has_parent(Person('HLID_30'), 'mother')

p = family.get_parents(person1)
assert p[0].HLID == 'HLID_8' and p[1].HLID == 'HLID_9'

assert family.get_father(person1).HLID == 'HLID_8'


c = family.get_children(person1)
c_id = [int(x.HLID.split('_')[1]) for x in c]
assert sum(c_id) == 67

assert family.has_partners(person1)
assert not family.has_partners(Person('HLID_10'))

assert family.are_partners(Person('HLID_1'), Person('HLID_2'))

pt = family.get_partners(person1)
assert pt[0].HLID.split('_')[1] == '2'

s = family.get_siblings(person1)
s_id = [int(x.HLID.split('_')[1]) for x in s]
assert sum(s_id) == 23

#%%
'''
'''
1	Head
2	Wife / Husband
3	Son / Daughter
4	Son-In-Law / Daughter-In-Law
5	Grandchild
6	Parent
7	Parent-In-Law
8	Brother / Sister
9	Brother-In-Law / Sister-In-Law
10	Uncle / Aunt
11	Niece / Nephew
15	Niece / Nephew by marriage
12	Other relative
13	Adopted / Foster / Stepchild
16	Cousin
14	Servant
97	Inconsistent
98	DK
99	Missing
96	Non related
17	Grandparent
'''
