from numpy import multiply

def is_valid(pesel):
    p = list(map(int, [char for char in pesel]))
    w = [1,3,7,9,1,3,7,9,1,3,1]
    if (len(p) == 11):
        checksum = list(map(int, [char for char in str(sum(multiply(p,w)))]))
        if(checksum[-1] == 0):
            return True
        else:
            return False 
    else:
        return False

def check_gender(pesel):
    p = list(map(int, [char for char in pesel]))
    if (is_valid(p)==False):
        return 'invalid PESEL'
    else:
        if(p[9]%2==0):
            return 'female'
        else:
            return 'male'

def check_birthdate(pesel):
   p = list(map(int, [char for char in pesel]))
   if (is_valid(p)==False):
       return 'invalid PESEL'
   else:
       year=str(p[0])+str(p[1])
       month=int(str(p[2])+str(p[3]))
       day=str(p[4])+str(p[5])
       if (month >= 81 and month <= 92):
           year=str(18)+year
           month-=80
       elif (month >= 1 and month <= 12):
           year=str(19)+year
       elif (month >= 21 and month <= 32):
           year=str(20)+year
           month-=20
       elif (month >= 41 and month <= 52):
           year=str(21)+year
           month-=40
       elif (month >= 61 and month <= 72):
           year=str(22)+year
           month-=60
       
       return(str(year)+"/"+str(month)+"/"+str(day))
