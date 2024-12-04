###################################################################################################
# Settings                                                                                        #
###################################################################################################

import neo4j
import os.path
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.core import PropertyGraphIndex
from llama_index.core import SimpleDirectoryReader
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.indices.property_graph import SimpleLLMPathExtractor

using_openai = True

llm_path = os.path.dirname(__file__) + "/../models/Llama-3.2-1B"
embed_path = os.path.dirname(__file__) + "/../models/bert-base-uncased"

openai_key_path = os.path.dirname(__file__) + "/../util/openai_key"

neo4j_uri = "bolt://localhost:7687"
neo4j_username = "neo4j"
neo4j_password_path = os.path.dirname(__file__) + "/../util/password"

###################################################################################################
# Database Setup                                                                                  #
###################################################################################################
# First, we're going to connect to the local neo4j database. To do this, we'll have to store some
# information in a file in /util.

def GetTxt(path):
	if os.path.isfile(path):
		return open(path, "r").read()
	return ""

def ConnectDriver(uri, auth):
	return neo4j.GraphDatabase.driver(uri, auth)

###################################################################################################
# Extraction                                                                                      #
###################################################################################################

# ...

###################################################################################################
# Main                                                                                            #
###################################################################################################

def main():
	# First, we grab the password from the local password file.
	neo4j_password = GetTxt(neo4j_password_path)
	if (neo4j_password == ""):
		print("Password file not found.")
		return

	# Now, if we're using OpenAI, we load the key and set up our
	# LLM and Embedding Model.
	if using_openai:
		openai_key = GetTxt(openai_key_path)
		if (openai_key == ""):
			print("OpenAI API Key not found.")
			return
		os.environ["OPENAI_API_KEY"] = openai_key

		llm = llm=OpenAI(model="gpt-3.5-turbo", temperature=0.0)
		embed_model = OpenAIEmbedding(model_name="text-embedding-3-small")
	else:
		llm = HuggingFaceLLM(model_name=llm_path)
		embed_model = HuggingFaceEmbedding(model_name=embed_path)

	Settings.llm = llm

	# Next, we feed in our documents,
	documents = SimpleDirectoryReader(os.path.dirname(__file__) + "/../data/").load_data()

	# connect to the graph database,
	graph_store = Neo4jPropertyGraphStore(
		username=neo4j_username,
		password=neo4j_password,
		url=neo4j_uri,
	)
	
	# and then parse each document into the database.
	index = PropertyGraphIndex.from_documents(
		documents,
		embed_model=embed_model,
		kg_extractors = [SimpleLLMPathExtractor(
    		llm=llm,
    		max_paths_per_chunk=10,
    		num_workers=4)],
		property_graph_store=graph_store,
		show_progress=True
		)

	# This is just an example query.
	retriever = index.as_retriever(include_text=False)
	results = retriever.retrieve("What motivates people to become radicalized?")
	for record in results:
		print(record.text)

	query_engine = index.as_query_engine(include_text=True)
	response = query_engine.query("What motivates people to become radicalized?")
	print(str(response))
	
if __name__ == '__main__':
    main()