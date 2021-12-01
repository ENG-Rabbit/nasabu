"""def Relation_Check(person1:Node,person2:Node):
    results = []
    check_list = []
    road_list = []
    
    def checker(person1:Node,person2:Node,results,check_list,road_list):
        if person1.location[0] == person2.location[0]:
            
            if person1 in road_list:
                road_list.remove(person1)
            if person1 == person2:
                #road_list.append(0)
                pass
            elif person1.isbrother(person2):
                print(person1,person2)
                road_list.append(3)
            elif person1.issister(person2):
                road_list.append(4)
            #elif person1.isson(person2):
        #     return [6]
            #elif person1.isdaughter(person2):
            #   return [5]
            else:
                return [0]
        elif person1.location[0] > person2.location[0]:
            if person2.isfather(person1):
                results.append(1)
                return
            elif person2.ismother(person1):
                results.append(2)
                return
            if person1.father and person1.father.location[1] > person2.father.location[1]:
                check_list.append(person1.father)
                print(person1.father)
            if person1.mother and person1.mother.location[1] > person2.mother.location[1]:
                check_list.append(person1.mother)
                print(person1.mother)
            
            for person in check_list:
                if person2.isfather(person1):
                    road_list.append(1)
                elif person2.ismother(person1):
                    road_list.append(2)
                else:
                    road_list = checker(person,person2,results,check_list,road_list)
                if 0 in road_list:
                    results.append(road_list)

        
        
        
        
        return results
    
    return checker(person1,person2,check_list=check_list,results=results,road_list=road_list)"""
    
"""def flatten(t):
    return [item for sublist in t for item in sublist] 
 
def nasab_finder(person):
    nasab_list = []
    mini_nasab = []
    if person.father:
        mini_nasab.append(person.father)
    if person.mother:
        mini_nasab.append(person.mother)
    nasab_list.append(mini_nasab)
    mini_nasab = []
    i = 0
    while True:
        for person in nasab_list[i]:
            if person.father:
                mini_nasab.append(person.father)
            if person.mother:
                mini_nasab.append(person.mother)
        if mini_nasab == []:
            return flatten(nasab_list)
        nasab_list.append(mini_nasab)
        mini_nasab = []
        i += 1

def common_nasab(person1:Node,person2:Node):
    
    nasab_person1 = nasab_finder(person1)

    nasab_person2 = nasab_finder(person2)
    
    nasab_person2.insert(0,person2)
    
    
    for person in nasab_person2:
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
    
    
    return nasab_person2"""

"""def process_on_dict(d:dict):
    #flat_dict = flatten(d)
    new_dict = {}
    for key, val in d.items():
        new_dict[key]=string_to_list_of_int(val)
    return new_dict"""
    
    
    """def compare_nasabs(s1,s2)->str:
    nasab1 = string_to_list_of_int(s1)
    nasab2 = string_to_list_of_int(s2)
    print(nasab1,nasab2)
    nesbat = ''
    if 0 in nasab2:
        nasab2.remove(0)
    if 0 in nasab1:
        nasab1.remove(0)
    if nasab2:
        if len(nasab2) > 1 and len(nasab1) > 2 and len(nasab2) % 2 == 0:
            if nasab2[0] % 10 == 5:
                nesbat += DAUGHTER
                nesbat += ' '
            elif nasab2[0] % 10 == 6:
                nesbat += SON
                nesbat += ' '
            else:
                nesbat += ''
            if nasab1:
                a = 2
            else:
                a = 0
            nesbat += (GRANDCHILD + ' ')*(int((len(nasab2)-a)/2))
        else:
            if len(nasab2) > 1:
                if nasab1:
                    a = 1
                else:
                    a = 0
                nesbat += (GRANDCHILD + ' ')*(int((len(nasab2)-a)/2))
                
        if nasab1 and nasab2 and len(nasab1) > 2 + len(nasab2) > 1:
            if nasab1[-1] % 10 == nasab2[-1] % 10 == 5:
                nesbat += KHALE + ' '
            elif nasab1[-1] % 10 == nasab2[-1] % 10 == 6:
                nesbat += AMO + ' '
            elif nasab1[-1] % 10 == 5 and nasab2[-1] % 10 == 6:
                nesbat += DAEI + ' '
            elif nasab1[-1] % 10 == 6 and nasab2[-1] % 10 == 5:
                nesbat += AMME + ' '
        else:
            if not nasab1 and len(nasab2) % 2 == 1:
                if nasab2[0] % 10 == 5:
                    nesbat += DAUGHTER + ' '
                else:
                    nesbat += SON + ' '
            elif len(nasab1) % 2 == 1:
                if nasab2[-1] % 10 == 5:
                    nesbat += SISTER
                    nesbat += ' '
                elif nasab2[-1] % 10 == 6:
                    nesbat += BROTHER
                    nesbat += ' '
                
        if len(nasab1) >0:    
            nasab1.pop(-1)
        if nasab1 and len(nasab1) % 2 == 0:
            if nasab1[-1] > 20:
                nesbat += MOTHER + ' '
            else:
                nesbat += FATHER + ' '
    else:
        if len(nasab1) % 2 == 1:
            if nasab1[-1] > 20:
                nesbat += MOTHER + ' '
            else:
                nesbat += FATHER + ' '
                
    nasab1.reverse()
    if nasab2:
        a = 1
    else:
        a = 0
    for i in range(int((len(nasab1)-a)/2)):
        if nasab1[2*i] > 20:
            nesbat += GRANDMOTHER + ' '
        else:
            nesbat += GRANDFATHER + ' '
    if len(nasab1) > 3:
        if nasab1[-1] > 20:
            nesbat += MATERNAL
        else:
            nesbat += PATERNAL
    return nesbat"""