import numpy as np
import argparse
import httplib2
import os
import sys
import time
import socket
import threading

from apiclient import discovery
from oauth2client import file
from oauth2client import client
from oauth2client import tools

# Parser for command-line arguments.
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[tools.argparser])

parser.add_argument('input_file', help='Local path of csv input data (ex test.csv)')
parser.add_argument('output_file', help='Local path of csv output data (ex result.csv)')



CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')

# Set up a Flow object to be used for authentication.
FLOW = client.flow_from_clientsecrets(CLIENT_SECRETS,
  scope=[
      'https://www.googleapis.com/auth/devstorage.full_control',
      'https://www.googleapis.com/auth/devstorage.read_only',
      'https://www.googleapis.com/auth/devstorage.read_write',
      'https://www.googleapis.com/auth/prediction',
    ],
    message=tools.message_if_missing(CLIENT_SECRETS))

def print_header(line):
  '''Format and print header block sized to length of line'''
  header_str = '='
  header_line = header_str * len(line)
  print '\n' + header_line
  print line
  print header_line

class Printdot(threading.Thread): 
  def __init__(self, nom = ''): 
    threading.Thread.__init__(self) 
    self.nom = nom 
    self._stopevent = threading.Event()
  def run(self):
    while not self._stopevent.isSet():
      sys.stdout.flush()
      sys.stdout.write('.')
      time.sleep(1)
  def stop(self):
      self._stopevent.set()
  
def main(argv):
  # Parse the command-line flags.
  flags = parser.parse_args(argv[1:])

  # If the credentials don't exist or are invalid run through the native client
  # flow. The Storage object will ensure that if successful the good
  # credentials will get written back to the file.
  storage = file.Storage('sample.dat')
  credentials = storage.get()
  if credentials is None or credentials.invalid:
    credentials = tools.run_flow(FLOW, storage, flags)

  # Create an httplib2.Http object to handle our HTTP requests and authorize it
  # with our good Credentials.
  http = httplib2.Http()
  http = credentials.authorize(http)

  # Construct the service object for the interacting with the Prediction API.
  service = discovery.build('prediction', 'v1.6', http=http)

  try:
    prj = 'rproj-968'
    yourid='digit1'	
    papi = service.trainedmodels()
    print 'Google Prediction'
    print '\n' + "Building model"
    start_model = time.time()
    thrd = Printdot()
    thrd.start()
    	
    model_body = { 'id': yourid, 'storageDataLocation': 'digit/digit-train.csv','modelType':'classification' }
    model = papi.insert(project=prj,body=model_body).execute()

    model = papi.get(project=prj, id=yourid).execute()
    while (model['trainingStatus'] ==  'RUNNING'):
        time.sleep(1)
        model = papi.get(project=prj, id=yourid).execute()

    thrd.stop()
    end_model = time.time()
    print '\n' + "Completed in %.2f seconds" % (end_model - start_model) + '\n'


    # Make a prediction using the newly trained model.
    print 'Generating predictions'
    fin = open(flags.input_file, 'r')
    fout = open(flags.output_file, 'w')
    nbLines = 0
    start_predictions = time.time()
    thrd = Printdot()
    thrd.start()

    try:
        for line in fin:
      	    lineItems = line.split('\n')[0].replace('"','').split(',')
    	    body = {'input': {'csvInstance': lineItems[1:]}}
    	    result = papi.predict(project=prj, id=yourid, body=body).execute()
    	    yvalue = result['outputLabel']
      	    fout.write(yvalue+'\n')
    	nbLines+=1
    	if not nbLines%10:
          fout.flush()
    	  os.fsync(fout)
    except socket.error, v:
    	errorcode=v[0]
   	print 'error code '+errorcode+''
 
    thrd.stop()
    end_predictions = time.time()
    print '\n' + "Completed in %.2f seconds" % (end_predictions - start_predictions) + '\n'
    print "Google Prediction terminated in %.2f seconds" % (end_predictions - start_model) + '\n'
 
  except client.AccessTokenRefreshError:
    print ("The credentials have been revoked or expired, please re-run"
      "the application to re-authorize")
      
  #print prediction accuracy by comparing with labels of test data    
  y_predicted = np.genfromtxt('digit-results.csv', skip_header=0) 
  y_original = np.genfromtxt('Original.csv', skip_header=0)   
  accuracy = (y_predicted==y_original).sum()/float(y_predicted.size) 
  print 'Prediction accuracy is:', accuracy
   
if __name__ == '__main__':
  main(sys.argv)