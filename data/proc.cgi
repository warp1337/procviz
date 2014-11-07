#!/usr/bin/python

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
        self.conf = self.load_conf_file()

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
watch_list = s.conf
render = []

h = 0
for item in watch_list['procs']:
    res = s.check_process(item['host'], item['cmd'])
    if len(res) > 0:
        c = dict()
        c[h] = { "id":h, "h":item['host'], "PID":str(res[0]).replace('\n', ' ').replace('\r', ''), "name":item['name'].replace('\n', ' ').replace('\r', '') }
        render.append(c)
    else:
        c = dict()
        c[h] = { "id":h, "h":item['host'], "PID":"DEAD", "name":item['name'].replace('\n', ' ').replace('\r', '') }
        render.append(c)
    h = h + 1

def print_response(start, data):

    # Print the HTML header
    print '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
    <html>
        <head>
            <title>LSP PROC VIZ</title>
            <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
            <meta http-equiv="Refresh" content="60">
            <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
            <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css">
            <link href="vis/dist/vis.css" rel="stylesheet" type="text/css" />
            <script src="vis/dist/vis.js"></script>
            <style type="text/css">
                #mynetwork {
                    width: 400px;
                    height: 400px;
                    border: 0px solid lightgray;
                }
            </style>
        </head>'''

    # Print header message for result
    print_html_message_h1("LSP-CSRA PROCESS WATCHDOG")

    # Print plot type
    for i in data:
        print_html_message_h3(i)

    print '''<div id="mynetwork"></div>
    <script type="text/javascript">'''

    print "var nodes = ["
    count = 0
    for k in data:
        print "{id: %s, label: '%s'}," % (k[count]['id'], k[count]['h'])
        print "{id: %s, label: '%s'}," % (k[count]['id']+2, k[count]['name'])
        count = count + 1
    print "{id:%s, label:'None'}" % 666
    print "];"

    print "var edges = ["
    count = 0
    for k in data:
        # print "{from: %s, to: '%s'}," % (k[count]['id'],k[count]['id']+1)
        print "{from: %s, to: '%s'}," % (k[count]['id'],k[count]['id'])
        count = count + 1
    print "{from:0, to: 'pycharm_3'}"
    print "];"

    print''' var container = document.getElementById('mynetwork');
        var data = {
                nodes: nodes,
                edges: edges
            };
        var options = {};
        var network = new vis.Network(container, data, options);
    </script> '''

    # Stop the timer and print the time
    stop = timeit.default_timer()
    print_html_message("Calculation and Rendering took "+str(stop-start)[:4]+" Seconds")

    # Close the HTML tree
    print '''</body></html>'''

# Now print the HTML response
print_response(start, render)


