from collections import defaultdict
import json
import sys
from os.path import exists
from os.path import isdir
from os import mkdir

def funcErrorWrapper():
    return funcError

def funcError():
    print("Error: invalid command")
    return

def ArgError(err, func):
    if err:
        print("Error: Too few arguments for", func)
    else:
        print("Error: Too many arguments for", func)

def inputCheck(args, func):
    if len(sys.argv) < args:
        ArgError(1, func)
        return 1
    elif len(sys.argv) > args:
        ArgError(0, func)
        return 1
    return 0

def addUser():
    #input checking
    if inputCheck(4, "AddUser"):
        return
    #user and pass
    user = sys.argv[2]
    if not user:
        print("Error: username missing")
        return
    p = sys.argv[3]

    with open(".tables/passwords.json", "a+") as fp:
        fp.seek(0)
        try:
            passwords = json.load(fp)
        except json.decoder.JSONDecodeError:
            #print("json erroed")
            passwords = {}
        
        if user in passwords:
            print("Error: user already exists")
            return
        else:
            passwords[user] = p
            print("Success")
            with open(".tables/passwords.json", "w+") as gp:
                json.dump(passwords, gp)
            return
        
def authenticate():
    #input checking
    if inputCheck(4, "Authenticate"):
        return 
    user = sys.argv[2]
    p = sys.argv[3]
    if not exists(".tables/passwords.json"):
        print("Error: no such user")
        return
    with open(".tables/passwords.json", "r") as fp:
        passwords = json.load(fp)
        if user not in passwords:
            print("Error: no such user")
            return
        print("Error: incorrect password") if passwords[user] != p else print("Success")
        return

def setDomain():
    #input checking
    if inputCheck(4, "SetDomain"):
        return

    #check if domain valid
    user = sys.argv[2]
    domain = sys.argv[3]
    if not domain:
        print("Error: missing domain")
        return

    #check if user exists
    if not exists(".tables/passwords.json"):
        print("Error: no such user")
        return
    with open(".tables/passwords.json", "r") as fp:
        passwords = json.load(fp)
        if user not in passwords:
            print("Error: no such user")
            return
    
    with open(".tables/domains.json", "a+") as fp:
        fp.seek(0)
        try:
            domains = json.load(fp)
        except json.decoder.JSONDecodeError:
            domains = {}
        if domain not in domains:
            domains[domain] = [user]
            print("Success")
            with open(".tables/domains.json", "w+") as gp:
                json.dump(domains, gp)
            return
        else:
            domains[domain].append(user)
            domains[domain] = list(set(domains[domain]))
            print("Success")
            with open(".tables/domains.json", "w+") as gp:
                json.dump(domains, gp)
            return

def domainInfo():
    #input Checking
    if inputCheck(3, "DomainInfo"):
        return
    domain = sys.argv[2]
    if not domain:
        print("Error: missing domain")
        return
    if not exists(".tables/domains.json"):
        return
    with open(".tables/domains.json", "r") as fp:
        domains = json.load(fp)
        if domain not in domains:
            return
        for user in domains[domain]:
            print(user)
        return

def setType():
    #input checking
    if inputCheck(4, "SetType"):
        return
    
    #check if valid values
    object = sys.argv[2]
    type_name = sys.argv[3]
    if not object:
        print("Error: missing object")
        return
    if not type_name:
        print("Error: missing type")
        return
    with open(".tables/types.json", "a+") as fp:
        fp.seek(0)
        try:
            types = json.load(fp)
        except json.decoder.JSONDecodeError:
            types = {}
        if type_name not in types:
            types[type_name] = [object]
            print("Success")
            with open(".tables/types.json", "w+") as gp:
                json.dump(types, gp)
            return
        else:
            types[type_name].append(object)
            types[type_name] = list(set(types[type_name]))
            print("Success")
            with open(".tables/types.json", "w+") as gp:
                json.dump(types, gp)
            return

def typeInfo():
    #input Checking
    if inputCheck(3, "DomainInfo"):
        return

    type_name = sys.argv[2]
    if not type_name:
        print("Error: missing type name")
    if not exists(".tables/types.json"):
        return
    with open(".tables/types.json", "r") as fp:
        types = json.load(fp)
        if type_name not in types:
            return
        for obj in types[type_name]:
            print(obj)
        return

#checks if domain exists and adds empty list if not
#checks if type exists and adds empty list if not

def addAccess():
    #input checking
    if inputCheck(5, "AddAccess"):
        return
    operation = sys.argv[2]
    domain = sys.argv[3]
    type_name = sys.argv[4]

    if not operation:
        print("Error: operation missing")
        return
    if not domain:
        print("Error: domain missing")
        return
    if not type_name:
        print("Error: type missing")
        return
    
    with open(".tables/domains.json", "a+") as fp:
        fp.seek(0)
        try:
            domains = json.load(fp)
        except json.decoder.JSONDecodeError:
            domains = {}
        if domain not in domains:
            domains[domain] = []
            with open(".tables/domains.json", "w+") as gp:
                json.dump(domains, gp)
    
    with open(".tables/types.json", "a+") as fp:
        fp.seek(0)
        try:
            types = json.load(fp)
        except json.decoder.JSONDecodeError:
            types = {}
        if type_name not in types:
            types[type_name] = []
            with open(".tables/types.json", "w+") as gp:
                json.dump(types, gp)

    with open(".tables/acm.json", "a+") as fp:
        fp.seek(0)
        try:
            acm = json.load(fp)
        except json.decoder.JSONDecodeError:
            acm = {}
        if domain not in acm:
            acm[domain] = {type_name: [operation]}
            print("Success")
            with open(".tables/acm.json", "w+") as gp:
                json.dump(acm, gp)
            return
        else:
            if type_name not in acm[domain]:
                acm[domain][type_name] = [operation]
                print("Success")
                with open(".tables/acm.json", "w+") as gp:
                    json.dump(acm, gp)
            else:
                acm[domain][type_name].append(operation)
                acm[domain][type_name] = list(set(acm[domain][type_name]))
                print("Success")
                with open(".tables/acm.json", "w+") as gp:
                    json.dump(acm, gp)

def inverse(value, d):
    return [k for (k,v) in d.items() if value in v]

def canAccess():
    #get inversion of domain-> user, type-> object and call acm 
    if inputCheck(5, "CanAccess"):
        return

    op = sys.argv[2]
    user = sys.argv[3]
    obj = sys.argv[4]

    if not exists(".tables/passwords.json") or not exists(".tables/domains.json"):
        print("Error: Access Denied")
        return
    elif not exists(".tables/types.json") or not exists(".tables/acm.json"):
        print("Error: Access Denied")
        return
    with open(".tables/domains.json", "r") as fp:
        domains = json.load(fp)
    with open(".tables/types.json", "r") as fp:
        types = json.load(fp)
    with open(".tables/acm.json", "r") as fp:
        acm = json.load(fp)
        user_domains = inverse(user, domains)
        object_types = inverse(obj, types)
        for d in user_domains:
            if d not in acm:
                continue
            for t in object_types:
                if t not in acm[d]:
                    continue
                elif op in acm[d][t]:
                    print("Success")
                    return
        print("Access Denied")

if __name__ == "__main__":
    #setup 
    functions = defaultdict(funcErrorWrapper)
    functions['AddUser']=addUser
    functions['Authenticate']= authenticate
    functions['SetDomain']=setDomain
    functions['DomainInfo']=domainInfo
    functions['SetType']=setType
    functions['TypeInfo']=typeInfo
    functions['AddAccess']=addAccess
    functions['CanAccess']=canAccess
    if not isdir(".tables"):
        mkdir(".tables", 0o777)
    if len(sys.argv) <2:
        print("Error: Not enough arguments given")
    else:
        functions[sys.argv[1]]()

