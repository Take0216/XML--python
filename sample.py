import xml.etree.ElementTree as ET

tree = ET.parse(r'C:\python\a.xml')
root = tree.getroot()

class Function(object):
    def __init__(self,name,restrict):
        self.name = name
        self.restrict = restrict

FunctionList = list()

for i in root.findall("function"):
    name = i.get("name")
    restrict = i.get("restrict")
    Func = Function(name,restrict)
    FunctionList.append(Func)
print("pragma solidity 0.8.4;")
print("import './Ownable.sol'\n")
print("contract myfile is Ownable{")
print("address to;")
print("address from;")
print("uint amount = 0;")
print("mapping(address => uint) balance;\n")

for vg in FunctionList:
    if(vg.name == "deposit"):
        print(" function deposit() public payable {")
        if(vg.restrict == "owner"):
            print("     require(msg.sender == owner,\"You are not the owner\");")
        print("     balance[msg.sender] += msg.balue;")
        print(" }\n")
    
    elif(vg.name == "regist"):
        print(" function regist(address _to, uint _amount,address _from) public {")
        print("     to = _to;")
        print("     from = _from;")
        print("     amount = _amount;")
        print(" }\n")
    
    elif(vg.name == "transfer"):
        print(" function transfer() public {")
        if(vg.restrict == "owner"):
            print("     require(msg.sender == owner,\"You are not the owner\");")
        print("     require(from != to, \"Invalid recipient\"")
        print("     balance[from] -= amount;")
        print("     balance[to] += amount;")
        print(" }")
print("}")






