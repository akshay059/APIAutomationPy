from cassandra import cluster

class Connection():
	def __init__(self):
		try:
			nodes = ['10.41.87.47', '10.41.87.48']
			db = 'adtech_dsp'
			self.cluster = cluster.Cluster(nodes)
			self.session = self.cluster.connect(db)
		except:
			print "error on connecting to cassandra."
	def close(self):
		self.session.shutdown()
		self.cluster.shutdown()

connection = Connection()

def deleteCampaignInDB(cmpId):
	s = connection.session
	s.execute("delete from campaigns where key = bigintAsBlob("+ str(cmpId) +")")

def deleteCreativeInDB(crId):
	s = connection.session
	s.execute("delete from creatives where creative_id = "+ str(crId))

def getCreativesOfCampaigns(cmpId):
	s = connection.session
	r = s.execute("select creative_id from adtech_dsp.creatives where campaign_id = " + str(cmpId))
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