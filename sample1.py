import xml.etree.ElementTree as ET

tree = ET.parse(r'C:\python\d.xml') # XMLファイル読み込み
root = tree.getroot() # 親要素rootに代入

ValiableList = [
    ["from","to","balance","amount"], #変数名
    [0,0,0,0], #宣言したか確認用
    ["address","address","mapping(address => uint)","uint"] #変数方対応付け
]
# 変数宣言リスト作成

class Contract: # コントラクト構造体宣言
    def __init__(self,name): # nameのみで宣言可能
        self.name = name
        self.functions = [] # 関数のフィールド
        self.extends = [] # 継承するファイルのフィールド(contract用)
        self.imports = [] # 継承するファイルのフィールド(import用)
        self.valiable = []# 必要となる変数のフィールド

    def add_valiable(self,v):
        self.valiable.append(v) # 変数の追加

    def add_function(self,f):
        self.functions.append(f) # 関数の追加
        self.variable.append(f.variables)

    def add_imports(self,name):
        self.imports.append(name) # 継承の追加
    
    def add_extends(self,name):
        self.extends.append(name) # 継承の追加

    def to_solidity(self):
        print("pragma solidity 0.8.4;\n") # バージョンの宣言、表示
        for i in self.imports:
            print("import \"{imp}\";".format(imp = i)) # importの宣言、表示
        if(self.extends == []): # 継承ファイルが0ではないか確認
            print("contract {name} {{".format(name=self.name)) # 0の場合のコントラクトの表示
        else:
            print("contract {name} is {extends} {{".format(name=self.name, extends=self.extends)) # 0でない場合のコントラクトの表示、2個以上の場合を考える必要がある
        for j in self.valiable: # フィールドに格納されている変数を1つずつ読み込み
            cou=0 # 配列の何個目を表示するか記憶させる
            for k in ValiableList[0]: # 配列の変数を1つずつ読み込み、フィールドで格納した変数があるか確認
                if j==k: # フィールドで格納した変数と一致する場所を探索
                    print("  {type} {valiable};".format(type=ValiableList[2][cou], valiable=ValiableList[0][cou])) #その変数の宣言を表示
                cou+=1 # 1つずつずらす、配列の要素番号を記憶しておき、表示の際に使うため




        for f in self.functions: # 関数の表示
            f.to_solidity() # 関数の構造体(function)の変数表示を使う
        print("}")

class Function:
    def __init__(self,name,visibility,attrs,modifier):
        self.name = name 
        self.args = []
        self.visibility = visibility
        self.attrs = attrs
        self.body = []
        self.modifier = modifier

    def add_body(self,body):
        self.body.append(body)

    def add_args(self,args):
        self.args.append(args)
    

    def to_solidity(self):
        if(self.args != []):
            if(self.attrs != None):
                if(self.modifier != None):
                    print("  function {name} ({args}) {visibility} {attrs} {modifier} {{".format(name=self.name,args=self.args,visibility=self.visibility,attrs=self.attrs,modifier=self.modifier))
                else:
                    print("  function {name} ({args}) {visibility} {attrs} {{".format(name=self.name,args=self.args,visibility=self.visibility,attrs=self.attrs))
            else:
                if(self.modifier != None):
                    print("  function {name} ({args}) {visibility} {modifier} {{".format(name=self.name,args=self.args,visibility=self.visibility,modifier=self.modifier))
                else:
                    print("  function {name} ({args}) {visibility} {{".format(name=self.name,args=self.args,visibility=self.visibility))
        else:
            if(self.attrs != None):
                if(self.modifier != None):
                    print("  function {name} () {visibility} {attrs} {modifier} {{".format(name=self.name,visibility=self.visibility,attrs=self.attrs,modifier=self.modifier))
                else:
                    print("  function {name} () {visibility} {attrs} {{".format(name=self.name,visibility=self.visibility,attrs=self.attrs))
            else:
                if(self.modifier != None):
                    print("  function {name} () {visibility} {modifier} {{".format(name=self.name,visibility=self.visibility,modifier=self.modifier))
                else:
                    print("  function {name} () {visibility} {{".format(name=self.name,visibility=self.visibility))
           

        for tex in self.body:
            print("    {text}".format(text=tex))

        print("  }\n")


i = root.find("xml")
name = i.get("name")
contract = Contract(name)

FunctionList = list()
TextTemplate = [
    ["deposit","to","from","amount","from=to","debit","transfer"],
    ["balance[msg.sender] += msg.value;","to = _to;","from = _from;","amount = _amount;","require(from != to, ""Invalid recipient"");","balance[from] -= amount;","balance[to] += amount;"],
    [["balance"],["to"],["from"],["amount"],["from","to"],["from","balance","amount"],["to","balance","amount"]]
    [[""]]
]
ModifierList = [
    ["onlyOwner"],
    ["Ownable.sol"],
    ["Ownable"]
]

###

funcs = {}

tmp = Function("deposit", "public", "payable", "")
tmp.add_body("""
$(v1)[msg.sender] += msg.value;
""")
tmp.variables = {"v1":Variable("balance", map), "v2":Variable("", address)}
funcs["deposit"] = tmp

tmp = Function("transfer", "public", "", "")
tmp.add_body("""
balance[msg.sender] += msg.value;
""")

funcs["transfer"] = tmp

###

# 正規表現 regular expression


check = 0

for i in root.findall("function"):
    TextList = list()
    name = i.get("name")
    visibility = i.get("visibility")
    attrs = i.get("attrs")
    modifier = i.get("modifier")
    Func = Function(name,visibility,attrs,modifier)
    if check == 0:
        for j in ModifierList[0]:
            if Func.modifier == j:
                check += 1
                contract.add_extends(ModifierList[2][0])
                contract.add_imports(ModifierList[1][0])



    body = i.find("body")
    text1 = body.get("text1")
    TextList.append(text1)
    text2 = body.get("text2")
    TextList.append(text2)
    text3 = body.get("text3")
    TextList.append(text3)
    for by in TextList:
        if(by != "None"):
            count = 0
            for textemp in  TextTemplate[0]:
                if by == textemp:
                    Func.add_body(TextTemplate[1][count])
                    for k in TextTemplate[2][count]:
                        co = 0
                        for j in ValiableList[0]:
                            if j == k and ValiableList[1][co] == 0:
                                ValiableList[1][co] += 1
                                contract.add_valiable(j)
                            co+=1

                count+=1
    FunctionList.append(Func)
    contract.add_function(Func)
contract.to_solidity()









    


    
