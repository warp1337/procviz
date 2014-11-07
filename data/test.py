import cgi
import os
import sys
import time
import cgitb
import timeit
import json

from paramiko import SSHClient
from paramiko import AutoAddPolicy

from tools import print_html_message
from tools import print_html_message_h1
from tools import print_html_message_h3
from tools import cut_string_after_char

# Measure some performance
start = timeit.default_timer()

# Enable cgitb
cgitb.enable()

# Set the HTML content type to HTML
print "Content-Type:text/html \n"

# Read the form field storage
params = cgi.FieldStorage()


class Server:

    def __init__(self):
        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.client.load_system_host_keys()

    def load_conf_file(self):
        with open("processes.json") as json_file:
            json_data = json.load(json_file)
        return json_data

    def check_process(self, host, proc_name):
        self.client.connect(host)
        stdin, stdout, stderr = self.client.exec_command('pidof %s' % proc_name)
        data = stdout.readlines()
        self.client.close()
        return data

s = Server()
data = s.check_process("m0thership", "/bin/sh /home/flier/pycharm-2.7.3/bin/pycharm.sh")[0]


def print_response(start, data):

    # Print the HTML header
    print '''<html> <head> <title>WebServer Log Visualisation</title></head>'''

    # Print header message for result
    print_html_message_h1("LogFile Visualisation Result")

    # Print plot type
    print_html_message_h3(data)

    # Stop the timer and print the time
    stop = timeit.default_timer()
    print_html_message("Calculation and Rendering took "+str(stop-start)[:4]+" Seconds")

    # Close the HTML tree
    print '''</body></html>'''

# Now print the HTML response
print_response(start, data)
