import math

def additemdata(keyword):
    if keyword == "cartoon":
        return 0
    if keyword == "romantic":
        return 1
    if keyword == "action":
        return 2
    if keyword == "scifi":
        return 3
    if keyword == "war":
        return 4
    if keyword == "history":
        return 5
    if keyword == "family":
        return 6
    if keyword == "documentary":
        return 7
    if keyword == "cook":
        return 8
    if keyword == "comedy":
        return 9
    if keyword == "sports":
        return 10
    if keyword == "variety":
        return 11
    if keyword == "others":
        return 12
        
def not0item(item, data):
    return [x for x in item if data[x - 1001] != 0]

def adduserdata(userid, userdata, itemdata):
    data = [float(x) for x in userdata]
    avg = sum(data) / len(data)
    [itemdata[k] for k in sorted(itemdata.keys())]
    cartoonitem = [int(x) for x in itemdata.keys() if itemdata[x][0] == 1]
    romanticitem = [int(x) for x in itemdata.keys() if itemdata[x][1] == 1]
    actionitem = [int(x) for x in itemdata.keys() if itemdata[x][2] == 1]
    scifiitem = [int(x) for x in itemdata.keys() if itemdata[x][3] == 1]
    waritem = [int(x) for x in itemdata.keys() if itemdata[x][4] == 1]
    historyitem = [int(x) for x in itemdata.keys() if itemdata[x][5] == 1]
    familyitem = [int(x) for x in itemdata.keys() if itemdata[x][6] == 1]
    documentaryitem = [int(x) for x in itemdata.keys() if itemdata[x][7] == 1]
    cookitem = [int(x) for x in itemdata.keys() if itemdata[x][8] == 1]
    comedyitem = [int(x) for x in itemdata.keys() if itemdata[x][9] == 1]
    sportsitem = [int(x) for x in itemdata.keys() if itemdata[x][10] == 1]
    varietyitem = [int(x) for x in itemdata.keys() if itemdata[x][11] == 1]
    othersitem = [int(x) for x in itemdata.keys() if itemdata[x][12] == 1]
    
    cartoon = [(data[x - 1001]- avg) / len(not0item(cartoonitem, data)) for x in not0item(cartoonitem, data)]
    romantic = [(data[x - 1001]- avg) / len(not0item(romanticitem, data)) for x in not0item(romanticitem, data)]
    action = [(data[x - 1001]- avg) / len(not0item(actionitem, data)) for x in not0item(actionitem, data)]
    scifi = [(data[x - 1001]- avg) / len(not0item(scifiitem, data)) for x in not0item(scifiitem, data)]
    war = [(data[x - 1001]- avg) / len(not0item(waritem, data)) for x in not0item(waritem, data)]
    history = [(data[x - 1001]- avg) / len(not0item(historyitem, data)) for x in not0item(historyitem, data)]
    family = [(data[x - 1001]- avg) / len(not0item(familyitem, data)) for x in not0item(familyitem, data)]
    documentary = [(data[x - 1001]- avg) / len(not0item(documentaryitem, data)) for x in not0item(documentaryitem, data)]
    cook = [(data[x - 1001]- avg) / len(not0item(cookitem, data)) for x in not0item(cookitem, data)]
    comedy = [(data[x - 1001]- avg) / len(not0item(comedyitem, data)) for x in not0item(comedyitem, data)]
    sports = [(data[x - 1001]- avg) / len(not0item(sportsitem, data)) for x in not0item(sportsitem, data)]
    variety = [(data[x - 1001]- avg) / len(not0item(varietyitem, data)) for x in not0item(varietyitem, data)]
    others = [(data[x - 1001]- avg) / len(not0item(othersitem, data)) for x in not0item(othersitem, data)]
    return [round(sum(cartoon), 2), round(sum(romantic), 2), round(sum(action), 2), round(sum(scifi), 2),
            round(sum(war), 2), round(sum(history), 2), round(sum(family), 2), round(sum(documentary), 2),
            round(sum(cook), 2), round(sum(comedy), 2), round(sum(sports), 2), round(sum(variety), 2), round(sum(others), 2)]

class ContentBasedCB:
    def __init__(self, item_file, user_file, nitem_file):
        self.item_file = item_file
        self.user_file = user_file
        self.nitem_file = nitem_file
        self.initData()
        self.readItem()

    def initData(self):
        # 读取文件，并生成Item Profiles和User Profiles
        self.item = dict() #Item Profiles
        for line in open(self.item_file):
            token = line.split()
            self.item.setdefault(token[0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            for index in range(1, len(token)):
                self.item[token[0]][additemdata(token[index])] = 1
        self.user = dict() #Item Profiles
        for line in open(self.user_file):
            token = line.split()
            self.user.setdefault(token[0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            self.user[token[0]] = adduserdata(token[0], token[1:], self.item)
        
    def readItem(self):
        # 读取文件，生成New Item Profiles
        self.nitem = dict() #Item Profiles
        for line in open(self.nitem_file):
            token = line.split()
            self.nitem.setdefault(token[0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            for index in range(1, len(token)):
                self.nitem[token[0]][additemdata(token[index])] = 1

    def Similarity(self, thisuserdata, itemdata):
        # 计算用户与物品的余弦相似度
        P = dict()  #该用户的偏好矩阵
        for item in itemdata:
            product, Ua2, Ia2 = 0, 0, 0
            for i in range(0,13):
                product += thisuserdata[i] * itemdata[item][i]
                Ua2 += thisuserdata[i] * thisuserdata[i]
                Ia2 += itemdata[item][i] * itemdata[item][i]
            result = product / math.sqrt( Ua2 * Ia2 )
            P.setdefault(item, result)
        return P

        # 给用户user推荐前K个相关物品
    def Recommend(self, userid, K=8):
        Preference = self.Similarity(self.user[userid], self.nitem)
        rank = sorted(Preference.items(), key = lambda item:item[1], reverse = True)
        return rank[0:K]

# 声明一个ItemBased推荐的对象
Content = ContentBasedCB("itemfile.txt", "userfile.txt", "newitem.txt")
userid = '10848'#input()
recommedDic = Content.Recommend(userid)
for k, v in recommedDic: 
    print(k, "\t", v)
