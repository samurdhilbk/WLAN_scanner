# WLAN_scanner
A Python backed web page that gives details about the currently available WLANs of the host server

The configuration of the Apache server to run Python as CGI was done by editing the httpd.conf file. I have included the entire httpd.conf file for completeness. The essential lines are 
  1. Options Indexes FollowSymLinks Includes ExecCGI
  2. AddHandler cgi-script .cgi .pl .asp .py
  
The 30-second refresh is handled by a meta tag in the HTML
