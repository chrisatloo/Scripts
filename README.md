# Scripts
Scripts that will make life easier for submitting and compiling homework
mktest [filename1] [filename2]
cautomatically creat a suite[foldername abbrev].txt which contains the name of your tests filename.in and filename.out
it automatically checks against existing tests to make sure you don't overide. 

## Newrelic_API 
This script takes inspiration from newrelic forum. It uses newrelic api to communicate with newrelic app for batch change to your newrelic for server monitoring and application monitoring. It can list all your apps/servers, delete apps/servers, find inactive/expired apps/servers. 
This python script complement Newrelic GUI and makes operating in batch much faster than manual work, you can also use it with crontab to periodically clean your newrelic data and clear out expired server data. 
Feel free to use or modify. Glad if it helps!

##mkzip
zips up all your testfiles in a zip for testing or running with runSuite


