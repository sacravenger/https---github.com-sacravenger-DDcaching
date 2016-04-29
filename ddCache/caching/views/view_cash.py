from django.shortcuts import render
from selenium import webdriver
from selenium.common.exceptions import NoSuchAttributeException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import staleness_of
import timeit

import socket
# Use log
import logging
# Import date time
from datetime import datetime
import time
import uuid

from xml.dom import minidom
import urllib

# using os lib
import os
import websocket

def catche_DD(request):
    SocketUrl = "ws://localhost:9000/"+str(uuid.uuid1())+"/"
    ws = websocket.WebSocket()


    #outputFileName = "loadingTimeat_" + str(time.strftime('%X')).replace(":","_")+".txt"
    #text_file = open(outputFileName, "w")
    
    if(request.GET.get('mybtn')):
        logging.basicConfig(filename='LogFile.log',level=logging.DEBUG)
        logging.info('Page cashing time log, testing date:')
        logging.info(str(datetime.now()))

        try:
            ws.connect(SocketUrl)
        except:
            ws.close()




        def wait_for_page_load(self, timeout=1):
            old_page = self.find_element_by_tag_name('html')
            yield
            WebDriverWait(self, timeout).until(staleness_of(old_page))
        # create a list of page loading time
        timeList = []
        url = request.GET.get('mytextbox')
        xml_str = urllib.urlopen(url).read()
        xmldoc = minidom.parseString(xml_str)

        itemList = xmldoc.getElementsByTagName('loc')
        print "Len : ", len(itemList)

        for s in itemList[-100:]:

            targetUrl = s.firstChild.nodeValue
            printtoweb(request,targetUrl )
            print "caching:" + targetUrl
            ws.send("caching:" + targetUrl +"     ")
            try:

                browser = webdriver.Firefox()
                # start the timer
                start_time = timeit.default_timer()
                browser.get(targetUrl)
                try:
                    wait_for_page_load(browser)
                    print "Page is ready!"
                    ws.send("Page is ready!" +"\n")
                    timeList.append(timeit.default_timer() - start_time)
                    browser.quit()
                except TimeoutException:
                    print "Loading took too much time!"
                    ws.send("Loading took too much time! \n")
                    timeList.append(timeit.default_timer() - start_time)
            except:
                logging.error(s)
                logging.error("cannot be load or open")


        #text_file.write('Page catching time log, testing date: '+ str(datetime.now()))
        #text_file.write(('\n' +'Index' + "   " + "Page loading time"))
        #totalTime = 0
        #for idx, val in enumerate(timeList):
        #    totalTime = totalTime + val
        #    timeinfo = '\n' +str(idx) + "         " + str(val)+" s"
        #    text_file.write(timeinfo)
        #text_file.write('\n'+'\n'+'Total time: ' + str(totalTime) +" s")
        #text_file.close()


    ws.close()

    return render(request,'Get_url.html', {'SocketUrl':SocketUrl})

def printtoweb(request, printinfo):
    outputweb = printinfo + ": successful"
    return render(request, 'outputweb.html', {'outputweb':outputweb})
