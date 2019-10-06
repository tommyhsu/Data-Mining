from apriori import Apriori

if __name__ == '__main__':

	while 1:
          
	    filePath = input("Please input the file name:")
	    minSupp  = float(input("Please input minimum support:"))
	    minConf  = float(input("Please input minimum confidence:"))

	    print("filePath:",  filePath,  "\n"  "mininum support:", minSupp, "\n"  "mininum confidence:", minConf, "\n")
	    # Run and print
	    Apriori_gen = Apriori(minSupp, minConf)
	    freqSet = Apriori_gen.frequentCount(filePath)
	    for key, value in freqSet.items():
	        print('frequent {}-term set:'.format(key))
	        print('-'*20)
	        for itemset in value:
	            print(list(itemset))
	        print()
	  
	    # Return rules with regard of `rhs`
	    for key,value in freqSet.items():
	    	for item in value:
		        rhs = item
		        association_rules = Apriori_gen.find_Association_Rules(rhs)
		        print('-'*20)
		        print('association_rules refer to {}'.format(list(rhs)))
		        for key, value in association_rules.items():
		            print('{} -> {}: support:{}  confidence:{}'.format(list(key), list(rhs), value[0], value[1]))
	            



