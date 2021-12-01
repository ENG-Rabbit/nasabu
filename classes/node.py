from constant import *
import time

class Node:
    def __init__(self,father=None,mother=None,spouse=None,sex=False,Generation=None,name=None,fatherlaw=None,motherlaw=None):
        self.father = father
        self.mother = mother
        self.sex = sex
        self.spouse = spouse
        if spouse:
            self.get_married(spouse)
        self.location = self.set_location(Generation)
        self.name = name
        self.father_in_law = fatherlaw
        self.mother_in_law = motherlaw
    
    
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

    def get_married(self,spouse)->bool:
        try:
            if self.spouse == spouse:
                #if not spouse.spouse:
                spouse.spouse = self
                return True
            elif spouse.spouse == self:
                #if not self.spouse:
                self.spouse = spouse
                return True
            else:
                self.spouse   = spouse
                spouse.spouse = self
                return True
        except: 
            return False

    def isspouse(self,spouse):
        return True if (self.spouse == spouse or spouse.spouse == self) else False



    def __str__(self):
        return self.name
        
def __flatten(d:dict)->dict:
    result = {}
    for dic in d.values():
        result |= dic
    return result

def __string_to_list_of_int(s:str)->list:
    return [int(i) for i in (s.split(','))]

def nasab_finder(person:Node):
    nasab_list = {}
    mini_nasab = {}
    if person.father:
        mini_nasab[person.father] = '15' if person.sex else '16' 
    if person.mother:
        mini_nasab[person.mother] = '25' if person.sex else '26'
    if person.spouse:
        mini_nasab[person.spouse] = '35' if person.sex else '36'
        
    i = 0
    nasab_list[i] = mini_nasab
    mini_nasab = {}
    while True:
        for person in nasab_list[i].keys():
            if person.father and not person.father in mini_nasab.keys():
                mini_nasab[person.father] = nasab_list[i][person] + ',' + ('15' if person.sex else '16') 
            if person.mother and not person.mother in mini_nasab.keys():
                mini_nasab[person.mother] = nasab_list[i][person] + ',' + ('25' if person.sex else '26')
            #if person.spouse and not person.spouse in mini_nasab.keys():
             #   mini_nasab[person.spouse] = nasab_list[i][person] + ',' + ('35' if person.sex else '36')
                
        if mini_nasab == {}:
            return __flatten(nasab_list)
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

def print_nasab(nasab1:list,nasab2:list,person_num:int=1)->str:
    
    nesbat1 = ''
    nesbat2 = ''
    if person_num == 1:
        pass
    else:
        pass

    return (nesbat2 + nesbat1).strip(' ')

def compare_nasabs(s1,s2,p=False)->str:
    nasab1 = __string_to_list_of_int(s1)
    nasab2 = __string_to_list_of_int(s2)
    nesbat = ''
    
    if 0 in nasab2:
        nasab2.remove(0)
    if 0 in nasab1:
        nasab1.remove(0)
    len_nasab1 = len(nasab1)
    len_nasab2 = len(nasab2)
    #if p:
      #  print(nasab1,nasab2)
      #  return
    
    for j in nasab1.copy():
        if j > 30:
            #nasab1.remove(j)
            len_nasab1 -= 1
    for j in nasab2.copy():
        if j > 30:
            #nasab1.remove(j)
            len_nasab2 -= 1

    if len_nasab1 != 0:
        if len_nasab2 != 0:
            if nasab2[0] > 30:
                nesbat += SPOUSE + ' '
                if len(nasab2) % 2 == 1:
                    if nasab2[0] % 10 == 5:
                        nesbat += DAUGHTER + ' '
                    else:
                        nesbat += SON + ' '
                    
                    nesbat += (GRANDCHILD + ' ')*(int((len_nasab2-1)/2))
                else:
                    nesbat += (GRANDCHILD + ' ')*(int((len_nasab2-1)/2))
            else:
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
                    len_nasab1 -= 1
                elif nasab1[-1] % 10 == nasab2[-1] % 10 == 6:
                    nesbat += AMO + ' '
                    nasab1.pop(-1)
                    len_nasab1 -= 1
                elif nasab1[-1] % 10 == 5 and nasab2[-1] % 10 == 6:
                    nesbat += DAEI + ' '
                    nasab1.pop(-1)
                    len_nasab1 -= 1
                elif nasab1[-1] % 10 == 6 and nasab2[-1] % 10 == 5:
                    nesbat += AMME + ' '
                    nasab1.pop(-1)
                    len_nasab1 -= 1
            else:
               
                if nasab2[0] < 30 or (len(nasab2[0:]) >= len(nasab1)):
                    if nasab2[-1] % 10 == 5:
                        nesbat += SISTER + ' '
                    elif nasab2[-1] % 10 == 6:
                        nesbat += BROTHER + ' '

            if len_nasab1 % 2 == 0:
                if nasab1[-1] > 30:
                    nesbat += SPOUSE + ' '
                elif nasab1[-1] > 20: #(30 > nasab1[-1] > 20 and not nasab2[0] > 30) or (20 > nasab1[-1] > 10 and nasab2[0] > 30):
                    nesbat += MOTHER + ' '
                else:
                    nesbat += FATHER + ' '
        else:
            if len_nasab1 % 2 == 1:
                if nasab1[-1] > 30:
                    nesbat += SPOUSE + ' '
                elif nasab1[-1] > 20:
                    if nasab2:
                        if nasab2[0] > 30:
                            nesbat += FATHER + ' '
                        else:
                            nesbat += MOTHER + ' '                          
                    else:
                        nesbat += MOTHER + ' '
                elif 20 > nasab1[-1] > 10:
                    if nasab2:
                        if nasab2[0] > 30:
                            nesbat += MOTHER + ' '
                        else:
                            nesbat += FATHER + ' '                          
                    else:
                        nesbat += FATHER + ' '
                        
                else:
                    nesbat += FATHER + ' '
            #else:
               # nesbat += (GRANDCHILD + ' ')*(int((len(nasab2)-1)/2))
    else:
        if nasab2 and nasab2[0] > 30:
                nesbat += SPOUSE + ' '
        elif len_nasab2 % 2 == 1: #and nasab2[0] < 30:
            if nasab2[0] % 10 == 5:
                nesbat += DAUGHTER + ' '
            else:
                nesbat += SON + ' '
                      
        nesbat += (GRANDCHILD + ' ')*(int((len_nasab2)/2))
    
    nasab1.reverse()
    if len_nasab2:
        a = 1
    else:
        a = 0
    if nasab1 and nasab1[-1] > 30:
        a += 1

    if len_nasab1 % 2 == 1:
        b = 1
    else:
        b = 0
    

    for i in range(int((len(nasab1)-a)/2)):
        if nasab1[2*i+b] > 30:
            nesbat += SPOUSE + ' '
        #elif (nasab1[2*i+b] > 20 or (2*i+b)>=len(nasab1)-1) and (nasab2 and nasab2[0] > 30):#NEW
        elif nasab1[2*i+b] > 20:
            if 2*i+b == 0 and nasab2 and nasab2[0] > 30:
                nesbat += GRANDFATHER + ' '
            else:
                nesbat += GRANDMOTHER + ' '
        else:
            if 2*i+b == 0 and nasab2 and nasab2[0] > 30:
                nesbat += GRANDMOTHER + ' '
            else:
                nesbat += GRANDFATHER + ' '

    if len_nasab1 == 0 and len(nasab2) > 1 and nasab2[0] > 30 and len_nasab2 % 2 == 1:
        if nasab2[1] % 10 == 5:
            nesbat += DAUGHTER
        else:
            nesbat += SON   
    elif len_nasab1 > 3 or (len(nasab1) >= 2 and nasab1[-1] > 30):
        if nasab1[-1] > 30:
            nesbat += SPOUSE
        elif nasab1[-1] > 20:
            nesbat += MATERNAL
        else:
            nesbat += PATERNAL
    else:
        if len_nasab1 >= len_nasab2 and nasab1 and nasab1[-1]>30:
            nesbat += SPOUSE
        
    #if nesbat == '':
    #    nesbat = NO_FAMILY_RELATIONSHIP
    
    return nesbat.strip(' ')
            
def find_relation(person1:Node,person2:Node,p=False):
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
    if person1.isspouse(person2):
        a.insert(0,person1)
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
            
        nasab = compare_nasabs(nasab1,nasab2,p=p)
        if nasab and not nasab in nasabs:
            nasabs.append(nasab)
    return nasabs




mohammad = Node(name='mohammad')
ali = Node(Generation=2,name='ali')
fatemeh = Node(father=mohammad,sex=True,name='fatemeh',spouse=ali)
hasan = Node(father=ali,mother=fatemeh,name='hasan')
hosein = Node(father=ali,mother=fatemeh,name='hosein')
sajad = Node(father=hosein,name='sajad')
amir = Node(father=sajad,name='amir')
sara = Node(Generation=5,name='sara',sex=True)
ali2 = Node(father=sajad,name='ali2',spouse=sara)

reza = Node(father=ali2,name='reza',mother=sara)
zahra = Node(father=ali2,sex=True,name='zahra',mother=sara)
narges = Node(father=hasan,sex=True,name='narges')
roya = Node(name='roya',father=reza,sex=True)
sahar = Node(name='sahar',spouse=amir,sex=True,Generation=5)

#print(ali2.spouse,sara.spouse)

#a = nasab_finder(sara)
#b = find_relation(sara,roya)
#print(b)

person1 = roya
person2 = narges

start = time.time()
for _ in range(100000):
    a = find_relation(person1,person2)
endt = time.time() - start
print('time spend: ',float(endt))
#print("#####")
print(person1,person2)
for person in a:
    print(person)
  
"""persons1 = [mohammad,fatemeh,ali,hasan,hosein,sajad,ali2,amir,narges,reza,zahra,roya,sara,sahar]
persons2 = [mohammad,fatemeh,ali,hasan,hosein,sajad,ali2,amir,narges,reza,zahra,roya,sara,sahar]
result = {
          mohammad:{mohammad:'خود',
                    fatemeh:'دختر',
                    ali:'همسر دختر',
                    hasan:'نوه',
                    hosein:'نوه',
                    sajad:'پسر نوه',
                    ali2:'نوه نوه',
                    amir:'نوه نوه',
                    narges:'دختر نوه',
                    reza:'پسر نوه نوه',
                    zahra:'دختر نوه نوه',
                    roya:'نوه نوه نوه',
                    sara:'همسر نوه نوه',
                    sahar:'همسر نوه نوه'},
          fatemeh:{mohammad:'پدر',
                   fatemeh:'خود',
                   ali:'همسر',
                   hasan:'پسر',
                   hosein:'پسر',
                   sajad:'نوه',
                   ali2:'پسر نوه',
                   amir:'پسر نوه',
                   narges:'نوه',
                   reza:'نوه نوه',
                   zahra:'نوه نوه',
                   roya:'دختر نوه نوه',
                   sara:'همسر نوه پسر',
                   sahar:'همسر نوه پسر'},
          ali:{mohammad:'پدر همسر',
               fatemeh:'همسر',
               ali:'خود',
               hasan:'پسر',
               hosein:'پسر',
               sajad:'نوه',
               ali2:'پسر نوه',
               amir:'پسر نوه',
               narges:'نوه',
               reza:'نوه نوه',
               zahra:'نوه نوه',
               roya:'دختر نوه نوه',
               sara:'همسر نوه پسر',
               sahar:'همسر نوه پسر'},
          hasan:{mohammad:'پدربزرگ',
                 fatemeh:'مادر',
                 ali:'پدر',
                 hasan:'خود',
                 hosein:'برادر',
                 sajad:'پسر برادر',
                 ali2:'نوه برادر',
                 amir:'نوه برادر',
                 narges:'دختر',
                 reza:'پسر نوه برادر',
                 zahra:'دختر نوه برادر',
                 roya:'نوه نوه برادر',
                 sara:'همسر نوه برادر',
                 sahar:'همسر نوه برادر'},
          hosein:{mohammad:'پدربزرگ',
                  fatemeh:'مادر',
                  ali:'پدر',
                  hasan:'برادر',
                  hosein:'خود',
                  sajad:'پسر',
                  ali2:'نوه',
                  amir:'نوه',
                  narges:'دختر برادر',
                  reza:'پسر نوه',
                  zahra:'دختر نوه',
                  roya:'نوه نوه',
                  sara:'همسر نوه',
                  sahar:'همسر نوه'},
          sajad:{mohammad:'پدر مادربزرگ',
                 fatemeh:'مادربزرگ',
                 ali:'پدربزرگ',
                 hasan:'عمو',
                 hosein:'پدر',
                 sajad:'خود',
                 ali2:'پسر',
                 amir:'پسر',
                 narges:'دختر عمو',
                 reza:'نوه',
                 zahra:'نوه',
                 roya:'دختر نوه',
                 sara:'همسر پسر',
                 sahar:'همسر پسر'},
          ali2:{mohammad:'پدربزرگ پدربزرگ پدری',
                fatemeh:'مادر پدربزرگ',
                ali:'پدر پدربزرگ',
                hasan:'عمو پدر',
                hosein:'پدربزرگ',
                sajad:'پدر',
                ali2:'خود',
                amir:'برادر',
                narges:'دختر عمو پدر',
                reza:'پسر',
                zahra:'دختر',
                roya:'نوه',
                sara:'همسر',
                sahar:'همسر برادر'},
          amir:{mohammad:'پدربزرگ پدربزرگ پدری',
                fatemeh:'مادر پدربزرگ',
                ali:'پدر پدربزرگ',
                hasan:'عمو پدر',
                hosein:'پدربزرگ',
                sajad:'پدر',
                ali2:'برادر',
                amir:'خود',
                narges:'دختر عمو پدر',
                reza:'پسر برادر',
                zahra:'دختر برادر',
                roya:'نوه برادر',
                sara:'همسر برادر',
                sahar:'همسر'},
          narges:{mohammad:'پدر مادربزرگ',
                  fatemeh:'مادربزرگ',
                  ali:'پدربزرگ',
                  hasan:'پدر',
                  hosein:'عمو',
                  sajad:'پسر عمو',
                  ali2:'نوه عمو',
                  amir:'نوه عمو',
                  narges:'خود',
                  reza:'پسر نوه عمو',
                  zahra:'دختر نوه عمو',
                  roya:'نوه نوه عمو',
                  sara:'همسر نوه عمو',
                  sahar:'همسر نوه عمو'},
          reza:{mohammad:'پدر مادربزرگ پدربزرگ پدری',
                fatemeh:'مادربزرگ پدربزرگ پدری',
                ali:'پدربزرگ پدربزرگ پدری',
                hasan:'عمو پدربزرگ',
                hosein:'پدر پدربزرگ',
                sajad:'پدربزرگ',
                ali2:'پدر',
                amir:'عمو',
                narges:'دختر عمو پدربزرگ',
                reza:'خود',
                zahra:'خواهر',
                roya:'دختر',
                sara:'مادر',
                 sahar:'همسر عمو'},
          zahra:{mohammad:'پدر مادربزرگ پدربزرگ پدری',
                 fatemeh:'مادربزرگ پدربزرگ پدری',
                 ali:'پدربزرگ پدربزرگ پدری',
                 hasan:'عمو پدربزرگ',
                 hosein:'پدر پدربزرگ',
                 sajad:'پدربزرگ',
                 ali2:'پدر',
                 amir:'عمو',
                 narges:'دختر عمو پدربزرگ',
                 reza:'برادر',
                 zahra:'خود',
                 roya:'دختر برادر',
                 sara:'مادر',
                 sahar:'همسر عمو'},
          roya:{mohammad:'پدربزرگ پدربزرگ پدربزرگ پدری',
                fatemeh:'مادر پدربزرگ پدربزرگ پدری',
                ali:'پدر پدربزرگ پدربزرگ پدری',
                hasan:'عمو پدر پدربزرگ پدری',
                hosein:'پدربزرگ پدربزرگ پدری',
                sajad:'پدر پدربزرگ',
                ali2:'پدربزرگ',
                amir:'عمو پدر',
                narges:'دختر عمو پدر پدربزرگ پدری',
                reza:'پدر',
                zahra:'عمه',
                roya:'خود',
                sara:'مادربزرگ',
                sahar:'همسر عمو پدر'},
          sara:{mohammad:'پدربزرگ پدربزرگ همسر',
                fatemeh:'مادر پدربزرگ همسر',
                ali:'پدر پدربزرگ همسر',
                hasan:'عمو پدر همسر',
                hosein:'پدربزرگ همسر',
                sajad:'پدر همسر',
                ali2:'همسر',
                amir:'برادر همسر',
                narges:'دختر عمو پدر همسر',
                reza:'پسر',
                zahra:'دختر',
                roya:'نوه',
                sara:'خود',
                sahar:'همسر برادر همسر'},
          sahar:{mohammad:'پدربزرگ پدربزرگ همسر',
                fatemeh:'مادر پدربزرگ همسر',
                ali:'پدر پدربزرگ همسر',
                hasan:'عمو پدر همسر',
                hosein:'پدربزرگ همسر',
                sajad:'پدر همسر',
                amir:'همسر',
                ali2:'برادر همسر',
                narges:'دختر عمو پدر همسر',
                reza:'پسر برادر همسر',
                zahra:'دختر برادر همسر',
                roya:'نوه برادر همسر',
                sahar:'خود',
                sara:'همسر برادر همسر'}
          }
try:
    counter = 0
    for person1 in persons1:
        for person2 in persons2:
            result_new = find_relation(person1,person2)
            try:
                if result[person1][person2] != result_new[0]:
                    
                    print('{} and {}:{}-->{}'.format(person1,person2,result[person1][person2],result_new[0]))
                    find_relation(person1,person2,p=True)
                #if result
                    #for person in result:
                    #    print(person,end='')
                    #    if len(result)>1:
                    #        print(' OR ')
                    counter += 1
                    print('#########')
            except:
                continue
                
    print('Counter = ',counter)
except:
    print(result_new)"""