# flask_api_demo
Simple python flask app using docker to demontrate use of google API and postgis to evaluate addresses

#Clone repository
git clone https://github.com/dceads4490/flask_api_demo.git

# YOU WILL NEED TO PERFORM THE FOLLOWING PRIOR TO DOCKER BUILD!!!!!
#You will need to provide your own Google API key to make this work!
#Edit .env file and place value for GOOGLE_API_KEY environment variable
#Dot in the .env file to set Google API KEY and postgress variables
. .ENV 

#Run the following command to build the app
docker-compose build

#Run the following command to start in foreground.  This is helpful to get logs directly on screen.
docker-compose up

#You can test the service using a web browser
http://localhost:5000/state_locator/?addr="7105 Avalon blvd, alpharetta"

#Testing using curl will require parsing the address to replace spaces.  You can use the following from the command prompt.
ADDR="7105 Avalon blvd, alpharetta, ga"
state=$(curl http://localhost:5000/state_locator/?addr=$(echo $ADDR|sed 's/ /%20/g'))
echo $state

If successful, this example should return Georgia



