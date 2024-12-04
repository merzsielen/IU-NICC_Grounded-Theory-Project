# IU-NICC_Grounded-Theory-Project
 LING-L665

# Setup
## Neo4j
 To begin, you'll need to set up a local Neo4j project and database by following [this tutorial](https://neo4j.com/docs/desktop-manual/current/operations/create-dbms/).
 Once this is done, go into your project's folder and click on the name of the DBMS you have set up (which will be "Graph DBMS" by default). This should pull up a window
 to the right with three tabs: Details, Plugins, and Upgrade. Go to "Plugins," select "APOC" and hit "Install." This will allow the program to interface properly with
 your new Neo4j database.

## Models
 ...

## Data & Credentials
 Before running the script, set up two folders in the same directory as this README file. Name them "data" and "util." In the former, place the files from which you want
 the script to extract knowledge graphs. In the latter, place at least one txt file labelled "password" (with no '.txt' ending). Within this file, write the password you
 set up for your local Neo4j database. In addition, if you are using the OpenAI API, you may also include a file in "util" called "openai_key" (again with no '.txt' ending).
 In this file, paste your OpenAI API key.

## Running
 Before running 'main.py', make sure your Neo4j database is running by going to the desktop app, clicking on your particular project, then clicking the blue "Start" button
 next to the name of your DBMS (which, again, is "Graph DBMS" by default). A yellow "STARTING" symbol will appear next to the name of your database and, if startup is
 successful, this will be replaced by a green "ACTIVE" symbol.
 
 Now, you can run the 'main.py' script in the "scripts" folder. This will load the database using the password stored in "util/password" then process the documents placed in
 "data" and, if using the OpenAI, connect to their API using the key stored "util/openai_key". The script will extract knowledge graphs from the provided data and save them
 in the database.
 
 To see the knowledge graphs in Neo4j, open your Neo4j Desktop app, open your project, go to "Graph DBMS" (or whatever you've named your local database) and select the
 blue "Open" button which appears next to the "Stop" button. This will open a Neo4j Browser window. Once there, click on the "Database Information" button on the left-side
 panel (the topmost button, above the star). This will open up a second panel, where you will (immediately) see three sections: Use database, Node labels, and Relationship
 types. Under Node labels, the first button should be light brown and feature an asterisk followed by a number in parentheses. This represents the number of nodes in the
 database (for example: "*(2,000)"). Clicking on this will bring up an interactive display representing certain "chunks" (indicating each document in the "data" file).
 Clicking on these will open up a menu: "Unlock", "Remove", and "Expand / Collapse." Clicking this last option will open up all the nodes connected to this one, and this can be
 repeated with subsequent nodes that appear in order to explore the connections present in the database.