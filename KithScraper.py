x=0
KITHURLs = [['https://kith.com/collections/mens-footwear?page=','Shoes'],['https://kith.com/collections/womens-footwear?page=', 'Shoes'],['https://kith.com/collections/mens-apparel?page=','Clothes'],['https://kith.com/collections/womens-apparel?page=', 'Clothes'], ['https://kith.com/collections/mens-accessories?page=', 'Accessories'], ['https://kith.com/collections/womens-accessories', 'Accessories']]
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