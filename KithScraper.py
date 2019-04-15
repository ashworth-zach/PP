x=0
KITHURLs = [['https://kith.com/collections/mens-footwear?page=','Shoes'],['https://kith.com/collections/mens-apparel-tees','Tees'],['https://kith.com/collections/mens-apparel-outerwear=', 'Outerwear'],['https://kith.com/collections/mens-apparel-hoodies?page=','Hoodies'],['https://kith.com/collections/mens-apparel-tees?page=', 'Clothes'], ['https://kith.com/collections/mens-apparel-crewnecks?page=', 'CrewNecks']]
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
def RunKith():
    import KithSpider
    KithSpider.SpidInit()
if __name__ == "__main__":
    RunKith()