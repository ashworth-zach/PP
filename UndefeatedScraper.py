x=0
KITHURLs = [['https://kith.com/collections/mens-footwear?page=','Shoes'],
['https://kith.com/collections/mens-apparel?page=','Clothes']]
def addOne():
    global x
    x += 1
def listchecker():
    global x
    global KITHURLs
    if x < len(KITHURLs):
        return True
    else:
        x=0
        return False
def getX():
    global x
    return x
def RunUndefeated():
    import UndefeatedSpider
    UndefeatedSpider.SpidInit()
if __name__ == "__main__":
    RunUndefeated()