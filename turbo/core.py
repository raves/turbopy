#
# Script to dump all settings for all entities individually 
#
import logging, os, sys, requests, base64, json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import constants, utils

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
baseURL = constants.URL_BASE_APIV2
sessionMap = {}		# Dictionary of Arrays indexed by hostname containing session values

"""Connect to an instance of Turbonomic, returning a new session.

	:param hostname: A string, the Turbonomic hostname.
	:param username: A string, the Turbonomic username.
	:param epassword: A string, the encrypted Turbonomic password.
	:param auth: A string, the authentication type to use.
	:param validateCert: A boolean, whether to validate Certifcates or not.
	"""
def connect(epassword, hostname='localhost', username='administrator', auth='Basic', validateCert='True'):
	session = requests.Session()
	sessionMap.setdefault(hostname, []).append(session)		# Save the session so we can disconnect gracefully later
	logging.info("Connecting to Turbonomic..")
	logging.debug(username + ":XXXXXXX@" + hostname)
	try:
		if (auth == "Basic"): 
			session.auth = (username, utils.decrypt(epassword))
		else:
			logging.error(auth + " not supported at this time. Use Basic.")
			raise NotImplementedError("Only Basic Auth is implemented at this time")
		session.headers.update({"Accept":"application/json"})	
		session.verify = validateCert
		r = session.get("https://" + hostname + baseURL + "/admin/versions")	# This call requires no authentication
		logging.debug("GET https://" + hostname + baseURL + "/admin/versions responded with " + str(r.json()))
		r = session.get("https://" + hostname + baseURL + "/markets")			# Must pass authentication 
		logging.debug("GET https://" + hostname + baseURL + "/markets responded with " + str(r.json()))
		logging.debug(r.headers)
		logging.debug(session.cookies)
	except Exception as e:
		logging.error("Failed to connect to " + hostname)
		raise
	logging.info("..session established to "+hostname)
	return session

"""Disconnect from an instance of Turbonomic, closing all open sessions, returning True if successful

	:param hostname: A string, the Turbonomic hostname.
	"""
def disconnect(hostname='localhost'):
	logging.info("Closing Turbonomic sessions to hostname " + hostname + "..")
	try:
		for session in sessionMap[hostname]:
	# TODO: Check back if Turbo API has implemented session control. Currently times out after 24 hours
	#	session.delete("https://" + hostname + "/api/sessions")
			session.close()
			logging.debug("Session closed")
		logging.info(".. " + str(len(sessionMap[hostname])) + " session(s) closed")
		del sessionMap[hostname]
	except KeyError as e:
		logging.warn("No sessions found for hostname " + hostname)
		return False
	return True

if __name__ == "__main__":
	if __package__ is None:		# For running this module directly
		import __init__
	logging.info("Starting..")
	connect(hostname='hostname',epassword='XXXXX',validateCert=False)
	disconnect('hostname')
	logging.info("..all done!")
