#!C:\Python27\python.exe

#This shebang reflects the location of the python.exe file. Change it appropriately if the corresponding location is different in your computer

print "Content-type: text/html"
print
print "<html><head>"
print '<meta http-equiv="refresh" content="30"/>'		#this is where the refresh happens

#These are the stylesheet and the JS scripts
#I used JQuery and JQuery UI to produce a responsive design
#Even if you ommit the CSS and JS altogether, this code would still produce the essential detials and the refresh also would still function
#So if you want to check the functionality without them, simply comment out the following four imports

print '<link rel="stylesheet" type="text/css" href="css/styles.css">'	
print '<script src="js/jquery-3.2.0.min.js"></script>'
print '<script src="js/jquery-ui.min.js"></script>'
print '<script src="js/app.js"></script>'


print "</head><body>"

#I'm using the inbuilt subprocess module to run the system command

import subprocess

#run the command and read the entire output in stdout to variable "output" 

output = subprocess.Popen('netsh wlan show all', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read()

#I am using the inbuilt regex module to extract the required data from the raw output

#this regex simply matches the format in which the details of the available WLANs are presented in the given command
#I have made a few assumptions here
# 1. Even though the SSID don't really have any character restrictions (in that it is not defined as a sequence of ASCII or Unicode characters),
#    I have assumed that it will not contain any newline charcters. Also in a subsequent operation I have assumed that there are no trailing or leading whitespace
# 2. The BSSID is assumed to be in the format of a MAC address (this is true in the majority of cases)

regex = r"^SSID \d+\s+: .+\s+Network type\s+: .+\s+Authentication\s+: .+\s+Encryption\s+: .+\s+BSSID 1\s+: [a-fA-F\d:]+\s+Signal\s+: \d+%"

import re

#findAll() is used since there can be multiple WLANS and hence mutiple matches for the above regex
#Also, the multiline flag is enabled to identify beginning of lines
matches = re.findall(regex, output, flags=re.MULTILINE)

#this list will hold the data for each WLAN
wlans = []

#iterating over the matches found
for match in matches:

	#this dictionary will hold the details of the current WLAN
	wlan = dict()

	#this regex exracts the SSID. Improvisations have been made to counter the restriction on variable length lookbehind in the Python regex engine
	ssid = re.search(r"(?<=\bSSID )\d+\s+: .+",match).group().strip().split(':')[1].strip()
	
	wlan["ssid"] = ssid;
	
	
	#this regex exracts the BSSID
	pre_bssid = re.search(r"(?<=\bBSSID 1)\s+: .+",match).group().strip()
	bssid = re.search(r"(?<=: ).+",pre_bssid).group()
	wlan["bssid"] = bssid;
	
	
	#this regex exracts the Signal
	pre_signal = re.search(r"(?<=\bSignal)\s+: .+",match).group().strip()
	signal = re.search(r"(?<=: ).+",pre_signal).group()
	wlan["signal"] = signal;
	
	wlans.append(wlan);


#this wrapper dictionary is to simply produce a JSON with the standard format, so that the details of the WLANS are available under the "wlans" property
wlan_wrapper = {"wlans":wlans};
	

import json

#create the JSON. This object can be passed into the client-side JS as a JSON
wlans_json = json.dumps(wlan_wrapper)


#loading the formed JSON so that it can be parsed
parsed_json = json.loads(wlans_json)


#the following simply iterates over the parsed JSON and writes the HTML. I have simply used a nested Ordered List(<ol>) and two buttons together with some headings.

print '<div id="heading"><h1>Availabe WLANs</h1><h2 id="countdown">Time until next refresh: <span id="timer">30</span></h2></div>'

print '<div id="canvas">'

print '<ol id="accordion">'
	
for wlan in parsed_json["wlans"]:
	print '<li class="main selected"> <span class="pill-main">'+wlan["ssid"]+'</span>'
	print '<ol>'
	print '<li> <span class="pill-key">SSID&nbsp;</span><span class="pill-value">'+wlan["ssid"]+'</span></li>'
	print '<li> <span class="pill-key">BSSID&nbsp;</span><span class="pill-value">'+wlan["bssid"]+'</span> </li>'
	print '<li> <span class="pill-key">Signal&nbsp;</span><span class="pill-value">'+wlan["signal"]+'</span><span class="progress"><span class="progress-bar" progress="'+wlan["signal"]+'" style="width:0%;"></span></span></li>'
	print '</ol>'
	print '</li>'

print '</ol>'

print '<div style="text-align:center; margin-bottom: 50px;"><div style="display: inline-block;">'
print '<button id="expand">Expand all</button>'
print '<button id="collapse">Collapse all</button>'
print '</div></div>'

print '</div>'
	
print "</body></html>"