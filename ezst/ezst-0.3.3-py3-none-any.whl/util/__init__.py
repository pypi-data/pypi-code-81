
def nd_print(A, w=None, h=None):
    if A.ndim==1:
        if w == None :
            return str(A)
        else:
            s ='['+' '*(max(w[-1],len(str(A[0])))-len(str(A[0]))) +str(A[0])
            for i,AA in enumerate(A[1:]):
                s += ' '*(max(w[i],len(str(AA)))-len(str(AA))+1)+str(AA)
            s +='] '
    elif A.ndim==2:
        w1 = [max([len(str(s)) for s in A[:,i]])  for i in range(A.shape[1])]
        w0 = sum(w1)+len(w1)+1
        s= u'\u250c'+u'\u2500'*w0+u'\u2510' +'\n'
        for AA in A:
            s += ' ' + ndtotext(AA, w=w1) +'\n'    
        s += u'\u2514'+u'\u2500'*w0+u'\u2518'
    elif A.ndim==3:
        h=A.shape[1]
        s1=u'\u250c' +'\n' + (u'\u2502'+'\n')*h + u'\u2514'+'\n'
        s2=u'\u2510' +'\n' + (u'\u2502'+'\n')*h + u'\u2518'+'\n'
        strings=[ndtotext(a)+'\n' for a in A]
        strings.append(s2)
        strings.insert(0,s1)
        s='\n'.join(''.join(pair) for pair in zip(*map(str.splitlines, strings)))
    
    print(s)