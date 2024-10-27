###################################################################################################
# Settings                                                                                        #
###################################################################################################

import os.path

neo4j_uri = "bolt://localhost:7687"
neo4j_username = "neo4j"
neo4j_password_path = os.path.dirname(__file__) + "/../util/password"

###################################################################################################
# Database Setup                                                                                  #
###################################################################################################
# First, we're going to connect to the local neo4j database. To do this, we'll have to store some
# information in a file in /util.

import neo4j

def GetTxt(path):
	if os.path.isfile(path):
		return open(path, "r").read()
	return ""

def ConnectDriver(uri, auth):
	return neo4j.GraphDatabase.driver(uri, auth)

###################################################################################################
# Main                                                                                            #
###################################################################################################

def main():
	# First, we grab the password from the local password file.
	neo4j_password = GetTxt(neo4j_password_path)
	if (neo4j_password == ""):
		print("Password file not found.")
		return
	credentials = (neo4j_username, neo4j_password)
	
	# Now, we connect to the Neo4j database.
	with neo4j.GraphDatabase.driver(neo4j_uri, auth=credentials) as driver:
		try:
			driver.verify_connectivity()
		except:
			print("Unable to the driver. Check that you are using the correct password and that the database is active.")
		print("Successfully connected to the database.")

		with driver.session(database="neo4j") as session:

			# Here is where we would run our code, extracting units of meaning and connecting them
			# in the database.

			session.close()

		driver.close

if __name__ == '__main__':
    main()