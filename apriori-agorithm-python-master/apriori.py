from collections import defaultdict
import csv


class Apriori(object):

    def __init__(self, minSupp, minConf):
 
        self.minSupp = minSupp 
        self.minConf = minConf  


    def frequentCount(self, filePath):
        #Run the apriori algorithm

        # Initialize
        itemCount = defaultdict(int)         # Count all the items
        freqSet       = dict()                   # store Frequent item sets
        transactionSet  = self.readDatabase(filePath)   # find all transactions sets
        #print(transactionSet)
        itemSet       = self.find_one_itemSet(transactionSet) # find 1-item set
        
        self.transLength = len(transactionSet)     # number of transactions
        #print(self.transLength)
        self.itemSet     = itemSet

        # L1 is Frequent one set
        L1 = self.find_frequent_itemsets(transactionSet, itemSet, itemCount, self.minSupp)
        #print(L1)
        # Find frequent itemset Lk, until is empty
        Lk = 1
        currFreqTermSet = L1
        while currFreqTermSet != set():
            freqSet[Lk] = currFreqTermSet  
            Lk += 1
            currCandiItemSet = self.link_item_sets(currFreqTermSet, Lk) # get new k-terms set eq: two items set three item sets and so on
            currFreqTermSet  = self.find_frequent_itemsets(transactionSet, currCandiItemSet, itemCount, self.minSupp) # frequent k-terms set
            
        self.itemCount = itemCount # using to get the confidence
        self.freqSet   = freqSet   # using to get the association rules 

        return  freqSet


    def readDatabase(self, filePath):

        transaction = []
        with open(filePath, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for line in reader:

                transaction.append(set(line[1:]))   

        return transaction    
        

    def find_one_itemSet(self, transactionSet):
        # Find the 1-term item first

        itemSet = set()

        for line in transactionSet:
            for item in line:
                itemSet.add(frozenset([item]))

        return itemSet


    def link_item_sets(self, currentFreqSet, Lk):
        # Check the item is linkable or not

        JoinSet = set()
        localSet = defaultdict(int)

        for itemSet1 in currentFreqSet:
            for itemSet2 in currentFreqSet:

                if(len(itemSet1.union(itemSet2)) == Lk):
                    set([itemSet1.union(itemSet2)])
                    
                    for item in set([itemSet1.union(itemSet2)]):
                        
                        JoinSet.add(item)
        #print (JoinSet)
        return JoinSet  


    def find_Association_Rules(self, rhs):
                
        rules = dict()
        
        for key, value in self.freqSet.items():
            for item in value:
                if rhs.issubset(item) and len(item) > len(rhs):
                    rhs_sup = self.itemCount[item] / self.transLength 
                    lfs = item.difference(rhs)
                    lfs_sup = self.itemCount[lfs] / self.transLength
                    conf = rhs_sup / lfs_sup
                    if conf >= self.minConf:
                        rules[lfs] = (rhs_sup, conf)
            
        return rules            
                
    
    def find_frequent_itemsets(self, transactionSet, itemSet, freqSet, minSupp):
        # Find all the frequent item sets

        FreqitemSet  = set()
        localSet = defaultdict(int)
        
        for item in itemSet:
            for trans in transactionSet:
                if item.issubset(trans):
                    freqSet[item] += sum([1]) 
                    localSet[item] += sum([1])

        # using localset to store the item first, and if the count is >= than minsup
        ## then store to the FreqitemSet
        Num_of_trans = len(transactionSet)
        
        for item, count in localSet.items():
            if float(count)/Num_of_trans >= minSupp:
                FreqitemSet.add(item) 
        
        return FreqitemSet

