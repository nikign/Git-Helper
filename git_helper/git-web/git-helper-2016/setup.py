#used for install necessary python modules to run the Google App Engine
#After install, need to copy all the packages into libs folder
import subprocess

bashCommand = "sudo pip install -t lib -r lib_requirements.txt"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output = process.communicate()[0]
print output
