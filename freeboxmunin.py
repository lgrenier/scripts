#!/usr/bin/python
# -*- coding: utf-8 -*-

#Import + variables globales
import requests
import json
import ConfigParser
import socket
import sys
import hmac
import hashlib


CONFFILE = '/home/lgrenier/scripts/freeboxmunin.conf'
URL = 'http://mafreebox.freebox.fr/api/v1/'
APP_ID = 'fr.freebox.munin'
APP_NAME = 'Freebox Munin Script'
DEVICE_NAME = socket.gethostname()
APP_VERSION = '0.0.1'
TRACK_ID = ''
APP_TOKEN = ''
HEADERS = ''


def installconf():
    """Fonction pour installer la conf"""
    print CONFFILE + ' does not exist, let me create it'
    try:
        myconffile = open(CONFFILE, 'w')
    except IOError:
        print 'ERROR : unable to open ' + CONFFILE + ' for writing !!!'
        exit(1)
    #payload = { 'APP_ID': APP_ID, 'APP_NAME': APP_NAME,
    #'APP_VERSION': APP_VERSION, 'DEVICE_NAME': DEVICE_NAME }
    print 'Autoriser l acces la demande sur la freebox'
    #Demande de Token
    #r = requests.post('http://mafreebox.freebox.fr/api/v1/login/authorize/',
    #data=payload)
    #print 'Reponse de la Freebox : ' + r.text
    #data = r.json()
    myconfig = ConfigParser.ConfigParser()
    myconfig.add_section('General')
    myconfig.set('General', 'APP_TOKEN', '9Q+RPkrhP9s5o31v4QWS1IutS5b8agBR6n77Ht3/LeXm52nGw9rW+DgyJ33xziUl')
    myconfig.set('General', 'TRACK_ID', 0)
    myconfig.write(myconffile)
    myconffile.close()
    exit(0)


def readconf():
    """Fonction sui lit et charge le fichier de conf"""
    global TRACK_ID
    global APP_TOKEN
    #On essaye d'ouvrir le fichier de conf
    try:
        myconffile = open(CONFFILE, 'r')
    except IOError:
        #(si pas de conf -> Installation)
        installconf()
    myconffile.close()

    #Chargement du fichier de conf
    myconfig = ConfigParser.ConfigParser()
    try:
        myconfig.read(CONFFILE)
    except ConfigParser.ParsingError, err:
        print 'Could not parse:', err
        exit(2)

    try:
        TRACK_ID = myconfig.get('General', 'TRACK_ID')
    except ConfigParser.NoOptionError, err:
        print 'Option TRACK_ID not found !!!'
        exit(3)

    try:
        APP_TOKEN = myconfig.get('General', 'APP_TOKEN')
    except ConfigParser.NoOptionError, err:
        print 'Option APP_TOKEN not found !!!'
        exit(4)


def authentification():
    """Fonction qui permet de s'authentifier"""
    global HEADERS
    #Verification du TrackID et recup du challenge
    payload = {'app_id': APP_ID, 'app_name': APP_NAME, 'app_version': APP_VERSION, 'device_name': DEVICE_NAME}
    r = requests.get(URL + 'login/authorize/' + TRACK_ID)
    if r.json()["result"]["status"] != "granted":
        print "Erreur : le TRACK_ID n'est pas au statut granted !!!"
        print "Recommencer l'installation !!!"
        print "Reponse de la Freebox : " + r.text
        exit(7)
    challenge = r.json()["result"]["challenge"]
    monhash = hmac.new(APP_TOKEN, challenge, hashlib.sha1).hexdigest()
    payload = {'app_id': APP_ID, 'password': monhash}
    r = requests.post(URL + 'login/session/', data=json.dumps(payload))
    if not r.json()["success"]:
        print "Erreur lors de l'authentification!!!"
        print "Reponse de la Freebox : " + r.text
        exit(8)
    HEADERS = {'X-Fbx-App-Auth': r.json()["result"]["session_token"]}


def disconnect():
    r = requests.post(URL + 'login/logout/', data='', headers=HEADERS)
    if not(r.json()["success"]):
        print "ERROR : no success to the disconnect request !!!"
        print "Answer from the Freebox is : " + r.text
        exit(13)


def get_traffic():
    r = requests.get(URL + 'connection/', data='', headers=HEADERS)
    if not(r.json()["success"]):
        print "ERROR : no success to the connection request !!!"
        print "Answer from the Freebox is : " + r.text
        exit(12)
    print 'traffic_down.value ' + str(r.json()["result"]["rate_down"])
    print 'traffic_up.value ' + str(r.json()["result"]["rate_up"])


def get_trafficup():
    r = requests.get(URL + 'connection/', data='', headers=HEADERS)
    if not(r.json()["success"]):
        print "ERROR : no success to the connection request !!!"
        print "Answer from the Freebox is : " + r.text
        exit(12)
    print 'traffic_up.value ' + str(r.json()["result"]["rate_up"])


def get_trafficdown():
    r = requests.get(URL + 'connection/', data='', headers=HEADERS)
    if not(r.json()["success"]):
        print "ERROR : no success to the connection request !!!"
        print "Answer from the Freebox is : " + r.text
        exit(12)
    print 'traffic_down.value ' + str(r.json()["result"]["rate_down"])


def get_temperature():
    r = requests.get(URL + 'system/', data='', headers=HEADERS)
    if not(r.json()["success"]):
        print "ERROR : no success to the connection request !!!"
        print "Answer from the Freebox is : " + r.text
        exit(13)
    print 'temp_cpum.value ' + str(r.json()["result"]["temp_cpum"])
    print 'temp_cpub.value ' + str(r.json()["result"]["temp_cpub"])
    print 'temp_sw.value ' + str(r.json()["result"]["temp_sw"])


def get_uptime():
    r = requests.get(URL + 'system/', data='', headers=HEADERS)
    if not(r.json()["success"]):
        print "ERROR : no success to the connection request !!!"
        print "Answer from the Freebox is : " + r.text
        exit(14)
    uptimestr = r.json()["result"]["uptime"]
    monuptime = float(0)
    i = uptimestr.find('seconde')
    if (i != -1):
        if (i >= 3):
            monuptime += (float(uptimestr[i - 3:i]) / (60 * 60 * 24))
        else:
            monuptime += (float(uptimestr[i - 2:i]) / (60 * 60 * 24))
    i = uptimestr.find('minute')
    if (i != -1):
        if (i >= 3):
            monuptime += (float(uptimestr[i - 3:i]) / (60 * 24))
        else:
            monuptime += (float(uptimestr[i - 2:i]) / (60 * 24))
    i = uptimestr.find('heure')
    if (i != -1):
        if (i >= 3):
            monuptime += (float(uptimestr[i - 3:i]) / (24))
        else:
            monuptime += (float(uptimestr[i - 2:i]) / (24))
    i = uptimestr.find('jour')
    if (i != -1):
        if (i >= 3):
            monuptime += (float(uptimestr[i - 3:i]))
        else:
            monuptime += (float(uptimestr[i - 2:i]))
    #print uptimestr
    print 'uptime.value ' + str(monuptime)


def get_fan():
    r = requests.get(URL + 'system/', data='', headers=HEADERS)
    if not(r.json()["success"]):
        print "ERROR : no success to the connection request !!!"
        print "Answer from the Freebox is : " + r.text
        exit(15)
    print 'fan_rpm.value ' + str(r.json()["result"]["fan_rpm"])


def get_switch(num_switch):
    if num_switch < 1 or num_switch > 4:
        print 'ERROR : port number must be between 1 and 4'
        exit(16)
    r = requests.get(URL + 'switch/port/' + str(num_switch) +
    '/stats', data='', headers=HEADERS)
    if not(r.json()["success"]):
        print "ERROR : no success to the connection request !!!"
        print "Answer from the Freebox is : " + r.text
        exit(16)
    print 'tx_bytes_rate.value ' + str(r.json()["result"]["tx_bytes_rate"])
    print 'rx_bytes_rate.value ' + str(r.json()["result"]["rx_bytes_rate"])


def get_switch1():
    get_switch(1)


def get_switch2():
    get_switch(2)


def get_switch3():
    get_switch(3)


def get_switch4():
    get_switch(4)


def get_wifi():
    r = requests.get(URL + 'wifi/stations/', data='', headers=HEADERS)
    if not(r.json()["success"]):
        print "ERROR : no success to the connection request !!!"
        print "Answer from the Freebox is : " + r.text
        exit(17)
    print r.text


def get_uptime_sync():
    r = requests.get(URL + 'connection/xdsl/', data='', headers=HEADERS)
    if not(r.json()["success"]):
        print "ERROR : no success to the connection request !!!"
        print "Answer from the Freebox is : " + r.text
        exit(18)
    print 'uptime_sync.value ' + str(float(r.json()["result"]["status"]["uptime"]) / 86400)


def get_snr():
    r = requests.get(URL + 'connection/xdsl/', data='', headers=HEADERS)
    if not(r.json()["success"]):
        print "ERROR : no success to the connection request !!!"
        print "Answer from the Freebox is : " + r.text
        exit(19)
    print 'snr_up.value ' + str(r.json()["result"]["up"]["snr"])
    print 'snr_down.value ' + str(r.json()["result"]["down"]["snr"])


def get_attenuation():
    r = requests.get(URL + 'connection/xdsl/', data='', headers=HEADERS)
    if not(r.json()["success"]):
        print "ERROR : no success to the connection request !!!"
        print "Answer from the Freebox is : " + r.text
        exit(19)
    print 'attenuation_up.value ' + str(r.json()["result"]["up"]["attn"])
    print 'attenuation_down.value ' + str(r.json()["result"]["down"]["attn"])


def get_atm():
    r = requests.get(URL + 'connection/xdsl/', data='', headers=HEADERS)
    if not(r.json()["success"]):
        print "ERROR : no success to the connection request !!!"
        print "Answer from the Freebox is : " + r.text
        exit(20)
    print 'atm_up.value ' + str(r.json()["result"]["up"]["rate"])
    print 'atm_down.value ' + str(r.json()["result"]["down"]["rate"])


def config(hostname, monitor):
    print 'host_name ' + hostname
    print 'graph_category freebox'
    print 'graph_args --base 1000 -l 0'
    if monitor == 'traffic':
        print 'graph_category adsl'
        print 'graph_title Freebox Traffic (Up and Down)'
        print 'graph_info This graph shows the Traffic of the adsl line'
        + ' of the freebox server.'
        print 'traffic_down.label Download traffic'
        print 'traffic_up.label Upload traffic'
        print 'graph_vlabel Traffic (o/s)'
    elif monitor == 'trafficup':
        print 'graph_category adsl'
        print 'graph_title Freebox Traffic (Up)'
        print 'graph_info This graph shows the Traffic (Up) of the adsl'
        + ' line of the freebox server.'
        print 'traffic_up.label Upload traffic'
        print 'graph_vlabel Traffic (Up) (o/s)'
    elif monitor == 'trafficdown':
        print 'graph_category adsl'
        print 'graph_title Freebox Traffic (Down)'
        print 'graph_info This graph shows the Traffic (Down) of the'
        + ' adsl line of the freebox server.'
        print 'traffic_down.label Download traffic'
        print 'graph_vlabel Traffic (Down) (o/s)'
    elif monitor == 'temperature':
        print 'graph_category sensors'
        print 'graph_title Freebox temperatures'
        print 'graph_info This graph shows the temperatures of the'
        + ' freebox server.'
        print 'graph_vlabel Temp in °C'
        print 'temp_cpum.label Temp CPUm'
        print 'temp_cpub.label Temp CPUb'
        print 'temp_sw.label Temp SW'
    elif monitor == 'uptime':
        print 'graph_category system'
        print 'graph_title Freebox Uptime in days'
        print 'uptime.label uptime'
        print 'graph_vlabel uptime'
        print 'graph_info This graph shows the uptime of the freebox'
        + ' server.'
        print 'uptime.draw AREA'
    elif monitor == 'fan':
        print 'graph_category sensors'
        print 'graph_title Freebox fan speed'
        print 'graph_info This graph shows the fan rotationnal speed of'
        + ' the freebox server.'
        print 'fan_rpm.label fan speed'
        print 'graph_vlabel fan speed (RPM)'
    elif monitor == 'switch1':
        print 'graph_category ethernet'
        print 'graph_title Switch port 1 Traffic (Up and Down)'
        print 'graph_info This graph shows the Traffic of port 1 of the'
        + ' freebox server.'
        print 'tx_bytes_rate.label TX traffic'
        print 'rx_bytes_rate.label RX traffic'
        print 'graph_vlabel Traffic (o/s)'
    elif monitor == 'switch2':
        print 'graph_category ethernet'
        print 'graph_title Switch port 2 Traffic (Up and Down)'
        print 'graph_info This graph shows the Traffic of port 2 of the'
        + ' freebox server.'
        print 'tx_bytes_rate.label TX traffic'
        print 'rx_bytes_rate.label RX traffic'
        print 'graph_vlabel Traffic (o/s)'
    elif monitor == 'switch3':
        print 'graph_category ethernet'
        print 'graph_title Switch port 3 Traffic (Up and Down)'
        print 'graph_info This graph shows the Traffic of port 3 of the'
        + ' freebox server.'
        print 'tx_bytes_rate.label TX traffic'
        print 'rx_bytes_rate.label RX traffic'
        print 'graph_vlabel Traffic (o/s)'
    elif monitor == 'switch4':
        print 'graph_category ethernet'
        print 'graph_title Switch port 4 Traffic (Up and Down)'
        print 'graph_info This graph shows the Traffic of port 4 of the'
        + ' freebox server.'
        print 'tx_bytes_rate.label TX traffic'
        print 'rx_bytes_rate.label RX traffic'
        print 'graph_vlabel Traffic (o/s)'
    elif monitor == 'uptimesync':
        print 'graph_category adsl'
        print 'graph_title Freebox adsl sync uptime in days'
        print 'uptime_sync.label uptime_sync'
        print 'graph_vlabel uptime_sync'
        print 'graph_info This graph shows the synchro uptime of the'
        + ' freebox server.'
        print 'uptime_sync.draw AREA'
    elif monitor == 'atm':
        print 'graph_category adsl'
        print 'graph_title Freebox ATM Bandwidth (Up and Down)'
        print 'graph_info This graph shows the ATM bandwith of the'
        + ' freebox server.'
        print 'atm_down.label ATM down'
        print 'atm_up.label ATM up'
        print 'graph_vlabel ATM Bandwidth (kbit/s)'
    elif monitor == 'attenuation':
        print 'graph_category adsl'
        print 'graph_title Freebox Attenuation (Up and Down)'
        print 'graph_info This graph shows the Attenuation of the ADSL'
        + ' line of the freebox server.'
        print 'attenuation_down.label Attenuation down'
        print 'attenuation_up.label Attenuation up'
        print 'graph_vlabel Line attenuation (dB)'
    elif monitor == 'snr':
        print 'graph_category adsl'
        print 'graph_title Freebox SNR margin (Up and Down)'
        print 'graph_info This graph shows the SNR margin of the adsl'
        + ' line of the freebox server.'
        print 'snr_down.label SNR margin down'
        print 'snr_up.label SNR margin up'
        print 'graph_vlabel SNR margin (dB)'
    else:
        print 'ERROR : monitor can only be : traffic, temperature, fan,'
        + ' switch(n), uptimesync'
        return(99)

    return(0)


def main():
    scriptname = sys.argv[0].split('_')
    if len(scriptname) != 3:
        print 'Error  script name must be scriptname_hostname_monitor'
        return(9)
    hostname = scriptname[1]
    monitor = scriptname[2]

    if len(sys.argv) > 1:
        if sys.argv[1] == 'config':
            return(config(hostname, monitor))
        else:
            print sys.argv[1] + ' : unknown argument !!!'
            return(10)
    readconf()
    authentification()

    if monitor == 'traffic':
        get_traffic()
    elif monitor == 'trafficup':
        get_trafficup()
    elif monitor == 'trafficdown':
        get_trafficdown()
    elif monitor == 'temperature':
        get_temperature()
    elif monitor == 'uptime':
        get_uptime()
    elif monitor == 'fan':
        get_fan()
    elif monitor == 'switch1':
        get_switch1()
    elif monitor == 'switch2':
        get_switch2()
    elif monitor == 'switch3':
        get_switch3()
    elif monitor == 'switch4':
        get_switch4()
    elif monitor == 'uptimesync':
        get_uptime_sync()
    elif monitor == 'atm':
        get_atm()
    elif monitor == 'attenuation':
        get_attenuation()
    elif monitor == 'snr':
        get_snr()
    #elif monitor == 'wifi':
    #    get_wifi()
    else:
        print 'ERROR : monitor can only be : traffic,'
        return(11)
    disconnect()
    return(0)


if __name__ == "__main__":
    sys.exit(main())
