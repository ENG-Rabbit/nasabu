from constant import *




class Node:
    def __init__(self,father=None,mother=None,sex=False,Generation=None,name=None):
        self.father = father
        self.mother = mother
        self.sex = sex
        #self.Generation = Generation
        self.location = self.set_location(Generation)
        self.name = name
    
    def set_location(self,Generation):
        #try:
            if not Generation:
                if self.father and self.mother:
                    Generation = max(self.father.location[0],self.mother.location[0]) + 1
                elif self.father:
                    Generation = self.father.location[0] + 1
                elif self.mother:
                    Generation = self.mother.location[0] + 1
                else:
                    Generation = 1
            if self.father and self.mother:
                num = max(self.father.location[1],self.mother.location[1]) + 1
            elif self.father:
                num = self.father.location[1] + 1
            elif self.mother:
                num = self.mother.location[1] + 1
            else:
                num = 1
            return (Generation,num)
        #except:
        #    if not Generation:
         #       Generation = 1
        #    return (Generation,1)
        
    def isfather(self,child=None,father=None):
        if father and not father.sex:
            if self.father == father: return True
        elif child:
            if child.father == self: return True
        return False
    
    def ismother(self,child=None,mother=None):
        if mother and mother.sex:
            if self.mother == mother: return True
        elif child:
            if child.mother == self: return True
        return False
    
    def isparent(self,child=None,parent=None):
        if parent:
            if parent.sex and self.mother == parent: return True
            elif not parent.sex and self.father == parent: return True
        elif child:
            if self.ismother(child=child) or self.isfather(child=child): return True
        return False
    
    def isson(self,parent=None,son=None):
        if son and not son.sex:
            return self.isparent(child=son)
        elif parent and not self.sex:
            return self.isparent(parent=parent)
        return False
    
    def isdaughter(self,parent=None,daughter=None):
        if daughter and daughter.sex:
            return self.isparent(child=daughter)
        elif parent and self.sex:
            return self.isparent(parent=parent)
        return False
    
    def ischild(self,parent=None,child=None):
        if parent:
            return self.isparent(parent=parent)
        elif child:
            return self.isparent(child=child)
        return False
    
    def isbrother(self,brother):
        if not self.sex and self != brother:
            if (self.father and brother.father and self.father == brother.father):
                if (self.mother and brother.mother and self.mother == brother.mother) or not (self.mother or brother.mother):
                    return True
        return False
    
    def issister(self,sister):
        if self.sex and self != sister:
            if (self.father and sister.father and self.father == sister.father):
                if (self.mother and sister.mother and self.mother == sister.mother) or not (self.mother or sister.mother):
                    return True
        return False

    def __str__(self):
        return self.name
        
def flatten(d:dict)->dict:
    result = {}
    for dic in d.values():
        result |= dic
    return result

def string_to_list_of_int(s:str)->list:
    return [int(i) for i in (s.split(','))]

def nasab_finder(person):
    nasab_list = {}
    mini_nasab = {}
    
    if person.father:
        mini_nasab[person.father] = '15' if person.sex else '16' 
    if person.mother:
        mini_nasab[person.mother] = '25' if person.sex else '26' 
    i = 0
    nasab_list[i] = mini_nasab
    mini_nasab = {}
    while True:
        for person in nasab_list[i].keys():
            if person.father:
                mini_nasab[person.father] = nasab_list[i][person] + ',' + ('15' if person.sex else '16') 
            if person.mother:
                mini_nasab[person.mother] = nasab_list[i][person] + ',' + ('25' if person.sex else '26')
        if mini_nasab == {}:
            return flatten(nasab_list)
        i += 1
        nasab_list[i] = mini_nasab
        mini_nasab = {}

def find_common_nasab(nasab_person1:list,nasab_person2:list):
    
    for person in nasab_person2.copy():
        if not person in nasab_person1:
            nasab_person2.remove(person)
    
    nasab_person2.reverse()
    for person in nasab_person2.copy():
        for persn2 in nasab_person2[1:]:
            if person.sex and person.ismother(persn2):
                nasab_person2.remove(person)
                break
            elif not person.sex and person.isfather(persn2):
                nasab_person2.remove(person)
                break
    nasab_person2.reverse()
    
    return nasab_person2

def compare_nasabs(s1,s2)->str:
    nasab1 = string_to_list_of_int(s1)
    nasab2 = string_to_list_of_int(s2)
    nesbat = ''
    if 0 in nasab2:
        nasab2.remove(0)
    if 0 in nasab1:
        nasab1.remove(0)
    len_nasab1 = len(nasab1)
    len_nasab2 = len(nasab2)
    
    
    if nasab1:
        if nasab2:
            if len_nasab2 % 2 == 0:
                if nasab2[0] % 10 == 5:
                    nesbat += DAUGHTER + ' '
                else:
                    nesbat += SON + ' '
                nesbat += (GRANDCHILD + ' ')*(int((len_nasab2-2)/2))
            else:
                nesbat += (GRANDCHILD + ' ')*(int((len_nasab2-1)/2))
            if len_nasab2 > 0 and len_nasab1 > 1:
                if nasab1[-1] % 10 == nasab2[-1] % 10 == 5:
                    nesbat += KHALE + ' '
                    nasab1.pop(-1)
                    len_nasab1 = len(nasab1)
                elif nasab1[-1] % 10 == nasab2[-1] % 10 == 6:
                    nesbat += AMO + ' '
                    nasab1.pop(-1)
                    len_nasab1 = len(nasab1)
                elif nasab1[-1] % 10 == 5 and nasab2[-1] % 10 == 6:
                    nesbat += DAEI + ' '
                    nasab1.pop(-1)
                    len_nasab1 = len(nasab1)
                elif nasab1[-1] % 10 == 6 and nasab2[-1] % 10 == 5:
                    nesbat += AMME + ' '
                    nasab1.pop(-1)
                    len_nasab1 = len(nasab1)
            else:
                if nasab2[-1] % 10 == 5:
                    nesbat += SISTER + ' '
                elif nasab2[-1] % 10 == 6:
                    nesbat += BROTHER + ' '
            if len_nasab1 % 2 == 0:
                if nasab1[-1] > 20:
                    nesbat += MOTHER + ' '
                else:
                    nesbat += FATHER + ' '
        else:
            if len_nasab1 % 2 == 1:
                if nasab1[-1] > 20:
                    nesbat += MOTHER + ' '
                else:
                    nesbat += FATHER + ' '
            #else:
               # nesbat += (GRANDCHILD + ' ')*(int((len(nasab2)-1)/2))
    else:
        if len_nasab2 % 2 == 1:
            if nasab2[0] % 10 == 5:
                nesbat += DAUGHTER + ' '
            else:
                nesbat += SON + ' '
                
        nesbat += (GRANDCHILD + ' ')*(int((len_nasab2)/2))
    
    nasab1.reverse()
    if nasab2:
        a = 1
    else:
        a = 0
    if len_nasab1 % 2 == 1:
        b = 1
    else:
        b = 0
    for i in range(int((len_nasab1-a)/2)):
        if nasab1[2*i+b] > 20:
            nesbat += GRANDMOTHER + ' '
        else:
            nesbat += GRANDFATHER + ' '
    if len_nasab1 > 3:
        if nasab1[-1] > 20:
            nesbat += MATERNAL
        else:
            nesbat += PATERNAL
    
    if nesbat == '':
        nesbat = NO_FAMILY_RELATIONSHIP

    return nesbat
    


            
def find_relation(person1:Node,person2:Node):
    if person1 == person2:
        return ['خود']
    
    nasab_person2 = nasab_finder(person2)
    nasab_person1 = nasab_finder(person1)
    a = list(nasab_person1.keys())
    b = list(nasab_person2.keys())
    
    if person1.location[0] < person2.location[0]:
        a.insert(0,person1)
    else:
        b.insert(0,person2)
    common_nasabs = find_common_nasab(a,b)
    nasabs = []
    for common_nasab in common_nasabs:
        if common_nasab == person1:
            nasab1 = '0'
            nasab2 = nasab_person2[common_nasab] 
        else:
            nasab1 = nasab_person1[common_nasab]
            
            if common_nasab == person2:
                nasab2 = '0'
            else:
                nasab2 = nasab_person2[common_nasab] 
            
        nasab = compare_nasabs(nasab1,nasab2)
        if not nasab in nasabs:
            nasabs.append(nasab)
    return nasabs

mohammad = Node(name='mohammad')
fatemeh = Node(father=mohammad,sex=True,name='fatemeh')
ali = Node(Generation=2,name='ali')
hasan = Node(father=ali,mother=fatemeh,name='hasan')
hosein = Node(father=ali,mother=fatemeh,name='hosein')
sajad = Node(father=hosein,name='sajad')
ali2 = Node(father=sajad,name='ali2')
amir = Node(father=sajad,name='amir')
sara = Node(Generation=5,name='sara',sex=True)
reza = Node(father=ali2,name='reza',mother=sara)
zahra = Node(father=ali2,sex=True,name='zahra',mother=sara)
narges = Node(father=hasan,sex=True,name='narges')
roya = Node(name='roya',father=reza,sex=True)
#print(zahra.isdaughter(ali2))
#print(zahra.issister(reza))
#print(fatemeh.ismother(hasan))
#print(mohammad.location,ali2.location)
#print(Relation_Check(zahra,sajad))
#a = nasab_finder(narges)
person1 = ali
person2 = mohammad
a = find_relation(person1,person2)

#print("#####")
print(person1,person2)
for person in a:
    print(person)
  
"""persons1 = [mohammad,fatemeh,ali,hasan,hosein,sajad,ali2,amir,narges,reza,zahra,roya]
persons2 = [mohammad,fatemeh,ali,hasan,hosein,sajad,ali2,amir,narges,reza,zahra,roya]
for person1 in persons1:
    for person2 in persons2:
        result = find_relation(person1,person2)
        print('{} and {}:'.format(person1,person2),end=' ')
        #if result
        for person in result:
           print(person)
        print('#########')"""