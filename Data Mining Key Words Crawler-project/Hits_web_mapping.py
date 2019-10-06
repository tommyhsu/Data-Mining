from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import requests
from graphviz import Digraph
import networkx as nx
import math
import heapq

avoid_domain = ['facebook', 'twitter', 'linkedin', 'youtube', 'doubleclick', 'ads', '.png', '.jpg', '.svg']
rootSet = []
neighbor = []
G = nx.Graph()
DG = nx.DiGraph()
web = []

def build_Inneighbor_set(root_set, k):
	count = 0
	#url = link
	url = "https://search.yahoo.com/search?q=link:"+root_set
	html = requests.get(url)
	soup = BeautifulSoup(html.text, 'lxml')
	links = soup.find_all('a', attrs={'href': re.compile("^http://")} ,href = True)
	for link in links:
		if link.get('class') and "ac-algo" in link['class']:
			neighbor.append([link['href'], root_set])
			G.add_edges_from([(neighbor[count][0], root_set)])
			count = count + 1
			if count== k/2:
				break
	#print (incidents)
	return 

def build_Outneighbor_set(root_set, k):
	count = 0
	html = requests.get(root_set)
	soup = BeautifulSoup(html.text, 'lxml')
	links = soup.find_all('a', attrs={'href': re.compile("^http://")} )
	for link in links:
		neighbor.append([root_set, link['href']])
		G.add_edges_from([(root_set, neighbor[count][1])])
		count = count + 1
		if count == k:
			break
	#out_neighbor = random.choice(neighbor, k)
	#print(neighboors)
	return 


def build_root_set(search_term):
	count = 1
	header = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11 Chrome/53.0.2785.143 Safari/537.36'}
	url = "https://www.google.com/search?q="+search_term+"&num=60"
	raw_page = requests.get(url, headers = header).text
	results = re.findall(r'(?<=<h3 class="r"><a href="/url\?q=).*?(?=&amp)', str(raw_page))

	for line in results:
		domain_name = line.split('.')[1].split('.')[0]
		if domain_name not in avoid_domain and count <= 30:
			rootSet.append(line)
			count = count + 1
	#print(count)
	#print (len(rootSet))
	return rootSet

class HITSIterator:

	def __init__(self, G):
		self.errorrate = 0.00001
		self.max_iterations = 100
		self.graph = DG
		self.hub = {}
		self.authority = {}
		for node in self.graph.nodes():
			self.hub[node] = 1
			self.authority[node] = 1
		#print (self.authority)

	def hits(self, k):
		flag = False
		for i in range(self.max_iterations):
			change = 0.0
			norm = 0
			tmp = {}
			tmp = self.authority.copy()
			for node in self.graph.nodes():
				self.authority[node] = 0
				for incident_page in self.graph.in_edges(nbunch = None, data = False):
					#print([incident_page[1]])
					#print(self.authority[node])
					self.authority[node] += self.hub[incident_page[0]]
				norm += pow(self.authority[node], 2)

			norm = math.sqrt(norm)
			for node in self.graph.nodes():
				self.authority[node] /= norm
				change += abs(tmp[node] - self.authority[node])
			#=======================================================
			#===========hub=======================================
			norm = 0
			tmp = self.hub.copy()
			for node in self.graph.nodes():
				self.hub[node] = 0
				for neighbor_page in self.graph.out_edges(nbunch = None, data = False):
					self.hub[node] += self.authority[neighbor_page[1]]
				norm += pow(self.hub[node], 2)

			norm = math.sqrt(norm)
			for node in self.graph.nodes():
				self.hub[node] /= norm
				change += abs(tmp[node] - self.hub[node])

			#print("authority\n", self.authority)
			#print("hub\n", self.hub)

			if change < self.errorrate:
				flag = True
				break
		if flag:
			print("finished in %s iterations" % (i + 1))
		#for i in range (0, k):
		print("The top authority page", heapq.nlargest(k,self.authority.items(), key= lambda x:x[1]))
		print("The top hub page", heapq.nlargest(k,self.hub.items(), key= lambda x:x[1]))




def main():

	root_set = build_root_set('big+data+analytics')
	k =5 #input()
	for i in range (0,30):
		web = root_set[i]
		#print("root_web",web)
		#print("=========================================\n")
		build_Outneighbor_set(web, k)
		build_Inneighbor_set(web, k)
		list(nx.connected_components(G))
		#print(list(nx.connected_components(G)))
		#print(neighbor)
		#print("=========================================\n")
	for i in neighbor:
		DG.add_edges_from([(i[0],i[1])])
		#node, neighbors, data= DG.in_edges(nbunch = None, data = False)
		#print(DG.out_edges(nbunch = None, data = False))
		#print(DG.nodes())
		hits = HITSIterator(G)
		hits.hits(k)

if __name__ == '__main__':
	main()