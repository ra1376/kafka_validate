echo "Running the validate script"
source /root/build.sh
cd /root
#running the setup to first create 
python3 message_setup.py

# running the validate script
python3 consumer_client.py