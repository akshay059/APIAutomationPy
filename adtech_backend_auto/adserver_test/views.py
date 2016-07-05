from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
import json, traceback
import threading

from dbaccess import dbActions
# Create your views here.

#lock = threading.RLock()

def results(request):
	from pyresttest.resttest import RestTest
	params = request.GET
	test_groups = []

	try :
		test_file = params['file']
		#lock.acquire()
		try:
			test_groups = RestTest().main({"url":"", "test":test_file, "absolute_urls" : True, "log" : "debug", "interactive": False, "ssl_insecure" : True}).items()
		finally:
			pass
			#lock.release()
	except OSError as e:
		print e
		traceback.print_exc
	except IOError:
		return HttpResponseServerError("Supplied test file was not found.")
	except MultiValueDictKeyError:
		return HttpResponseBadRequest("File was not supplied in the input params.")
	# execute automated tests and validate responses and generate result json
	passSteps = warnSteps = failSteps = passCount = warnCount = failCount = 0


	import junit_xml as jx
	try:
		res = []
		testSuites = []
		for test_group in test_groups:
			group_name = test_group[0]
			tests = []
			for test in test_group[1]:
				if not test.step:
					testCase = jx.TestCase(test.test.name, test.test._url, 0, test.body)
					if not test.passed:
						testCase.add_failure_info(output = str(test.failures[0].message))
					tests.append(testCase)

				if test.passed:
					res.append({"passed": "passed", "name" : test.test.name, "group" : group_name, "response_code": test.response_code, "step": test.step})
					if not test.step:
						passCount += 1
					else:
						passSteps += 1
				else :
					if test.response_code == 204:
						res.append({"passed": "warning", "name" : test.test.name, "group" : group_name, "response_code": test.response_code, "failures" : test.failures[0].message, "step": test.step})
						if not test.step:
							warnCount += 1
						else:
							warnSteps += 1
					else :
						res.append({"passed": "failed", "name" : test.test.name, "group" : group_name, "response_code": test.response_code, "failures" : test.failures[0].message, "step": test.step})
						if not test.step:
							failCount += 1;
						else :
							failSteps += 1

			testSuites.append(jx.TestSuite(group_name, tests))
		res.append({"pass" : passCount, "warn": warnCount, "fail": failCount, "passSteps" : passSteps, "warnSteps": warnSteps, "failSteps": failSteps})
	except Exception as e:
		print e
		traceback.print_exc()
		return HttpResponseServerError("Some unknown error occured, please verify that test file is correctly structured or not.")

	if params['format'] == 'json':
		return HttpResponse(json.dumps(res)) # return results as json string.
	elif params['format'] == 'xml':
		return HttpResponse(jx.TestSuite.to_xml_string(testSuites))


def fileList(request):
	mypath = request.GET["path"]
	try :
		from os import listdir
		from os.path import isfile, join
		onlyfiles = [join(mypath, f) for f in listdir(mypath) if isfile(join(mypath, f))]
		onlyfiles = sorted(onlyfiles)
	except Exception as e:
		print e
		traceback.print_exc()
		return HttpResponseServerError("Some unknown error occured, please verify if the directory is correct or not.")
	return HttpResponse(json.dumps(onlyfiles))

def dirList(request):
	mypath = request.GET["path"]
	try:
		from os import listdir
		from os.path import isfile, join
		onlyDirs = [join(mypath, d) for d in listdir(mypath) if not isfile(join(mypath, d))]
	except Exception as e:
		print e
		traceback.print_exc()
		return HttpResponseServerError("Some unknown error occured, please verify if the directory is correct or not.")
	return HttpResponse(json.dumps(onlyDirs))

def cleanCampaign(request):
	cmpId = request.GET["cmpId"]
	try:
		dbActions.cleanUpCampaign(cmpId)
	except:
		return HttpResponseServerError("{'success' : false}")
	return HttpResponse("{'success' : true}")

def cleanSeller(request):
	aId = request.GET["aId"]
	try:
		dbActions.cleanUpSeller(aId)
	except:
		return HttpResponseServerError("{'success' : false}")
	return HttpResponse("{'success' : true}")

def getSpecificValueFromDB(request):
	query = request.GET["query"]
	print query
	try:
		value = dbActions.getSpecificValue(query)
	except:
		return HttpResponseServerError("Failed to query the DB or query is not correct.")
	res = {"success" : "True"}
	res["value"] = str(value)
	return HttpResponse(json.dumps(res))