from cassandra import cluster

class Connection():
	def __init__(self):
		nodes = []
		db = 'db'
		self.cluster = cluster.Cluster(nodes)
		self.session = self.cluster.connect(db)
	def close(self):
		self.session.shutdown()
		self.cluster.shutdown()

connection = Connection()

def deleteCampaignInDB(cmpId):
	s = connection.session
	s.execute("query 1")

def deleteCreativeInDB(crId):
	s = connection.session
	s.execute("query 2 "+ str(crId))

def getCreativesOfCampaigns(cmpId):
	s = connection.session
	r = s.execute("query 3 " + str(cmpId))
	return r

def cleanUpCampaign(cmpId):
	creatives = getCreativesOfCampaigns(cmpId)
	deleteCampaignInDB(cmpId)
	for c in creatives:
		deleteCreativeInDB(c.creative_id)	

def getSpecificValue(query):
	s = connection.session
	r = s.execute(query)
	return r[0][0]
