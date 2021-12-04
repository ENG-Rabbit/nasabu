from constant import *
import pickle


class Nasab:
    def __init__(self,father=None,mother=None,spouse=None,sex=False,Generation=None,name=None,fatherlaw=None,motherlaw=None):
        self.father = father
        self.mother = mother
        self.sex = sex
        self.spouse = spouse
        if spouse:
            self.get_married(spouse)
        self.name = name
        self.father_in_law = fatherlaw
        self.mother_in_law = motherlaw
        self.Generation = self.set_generation(Generation)
        #self.save()

    def set_generation(self,Generation):
        if not Generation:
            if self.father and self.mother:
                Generation = max(self.father.Generation,self.mother.Generation) + 1
            elif self.father:
                Generation = self.father.Generation + 1
            elif self.mother:
                Generation = self.mother.Generation + 1
            elif self.father_in_law and self.mother_in_law:
                Generation = max(self.father_in_law.Generation,self.mother_in_law.Generation) + 1
            elif self.father_in_law:
                Generation = self.father_in_law.Generation + 1
            elif self.mother_in_law:
                Generation = self.mother_in_law.Generation + 1
            else:
                Generation = 1
        return Generation
  
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
                spouse.spouse = self
                return True
            elif spouse.spouse == self:
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

    def save(self,**kwargs):
        try:
            with open('Nasabs.pkl', 'rb') as pickle_file:
                family_list = pickle.load(pickle_file)
        except:
            family_list = []
        if not self in family_list:
            family_list.append(self)
            with open('Nasabs.pkl', 'wb') as pickle_file:
                pickle.dump(family_list,pickle_file)
                return True
        else:
            return False

    def __getstate__(self):
        attributes = self.__dict__.copy()
        return attributes
    
    def __str__(self):
        return self.name
        
def __flatten(d:dict)->dict:
    result = {}
    for dic in d.values():
        result |= dic
    return result

def __string_to_list_of_int(s:str)->list:
    return [float(i) for i in (s.split(','))]

def nasab_finder(person:Nasab):
    nasab_list = {}
    mini_nasab = {}
    if person.father:
        mini_nasab[person.father] = '15' if person.sex else '16' 
    if person.mother:
        mini_nasab[person.mother] = '25' if person.sex else '26'
    if person.spouse:
        mini_nasab[person.spouse] = '35' if person.sex else '36'
    if person.father_in_law:
        mini_nasab[person.father_in_law] = '15.5' if person.sex else '16.5'
    if person.mother_in_law:
        mini_nasab[person.mother_in_law] = '25.5' if person.sex else '26.5'
        
    i = 0
    nasab_list[i] = mini_nasab
    mini_nasab = {}
    while True:
        for person in nasab_list[i].keys():
            if person.father and not person.father in mini_nasab.keys():
                mini_nasab[person.father] = nasab_list[i][person] + ',' + ('15' if person.sex else '16') 
            if person.mother and not person.mother in mini_nasab.keys():
                mini_nasab[person.mother] = nasab_list[i][person] + ',' + ('25' if person.sex else '26')
            if person.father_in_law and not person.father_in_law in mini_nasab.keys():
                mini_nasab[person.father_in_law] = nasab_list[i][person] + ',' + ('15.5' if person.sex else '16.6') 
            if person.mother_in_law and not person.mother_in_law in mini_nasab.keys():
                mini_nasab[person.mother_in_law] = nasab_list[i][person] + ',' + ('25.5' if person.sex else '26.5')
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
    print(nasab1,nasab2)
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
                    if nasab2[0] % 10 < 6:
                        nesbat += DAUGHTER + ' '
                    else:
                        nesbat += SON + ' '
                    if nasab2[0] % 1 == 0.5:
                            nesbat += STEP + ' '
                    
                    nesbat += (GRANDCHILD + ' ')*(int((len_nasab2-1)/2))
                else:
                    nesbat += (GRANDCHILD + ' ')*(int((len_nasab2-1)/2))
            else:
                if len_nasab2 % 2 == 0:
                    if nasab2[0] % 10 < 6:
                        nesbat += DAUGHTER + ' '
                    else:
                        nesbat += SON + ' '
                    if nasab2[0] % 1 == 0.5:
                        nesbat += STEP + ' '
                            
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
                    if nasab2[-1] % 10 < 6:
                        nesbat += SISTER + ' '
                    elif nasab2[-1] % 10 < 7:
                        nesbat += BROTHER + ' '

            if len_nasab1 % 2 == 0:
                if nasab1[-1] > 30:
                    nesbat += SPOUSE + ' '
                elif nasab1[-1] > 20:
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
        elif len_nasab2 % 2 == 1:
            if nasab2[0] % 10 < 6:
                nesbat += DAUGHTER + ' '
            else:
                nesbat += SON + ' '
            if nasab2[0] % 1 == 0.5:
                nesbat += STEP + ' '
                      
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
        if nasab2[1] % 10 < 6:
            nesbat += DAUGHTER
        else:
            nesbat += SON
        if nasab2[1] % 1 == 0.5:
            nesbat += STEP + ' '
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
    for i in nasab1:
        if i % 1 == 0.5:
            if nesbat[-1] != ' ':
                nesbat += ' '
            nesbat += STEP 
    #if nesbat == '':
    #    nesbat = NO_FAMILY_RELATIONSHIP
    
    return nesbat.strip(' ')
            
def find_relation(person1:Nasab,person2:Nasab,p=False):
    if person1 == person2:
        return ['خود']
    
    nasab_person2 = nasab_finder(person2)
    nasab_person1 = nasab_finder(person1)
    a = list(nasab_person1.keys())
    b = list(nasab_person2.keys())
    
    if person1.Generation < person2.Generation:
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

def save_nasabs(nasabs:list, **kwargs):
        import pickle
        try:
            try:
                with open('Nasabs.pkl', 'rb') as pickle_file:
                    family_list = pickle.load(pickle_file)
            except:
                family_list = []
            for nasab in nasabs:
                if not nasab in family_list:
                    family_list.append(nasab)
                    with open('Nasabs.pkl', 'wb') as pickle_file:
                        pickle.dump(family_list,pickle_file)
            return True
        except:
            return False