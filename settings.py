from datetime import datetime, timedelta
import subprocess
import os
#import downloadFiles as dF

edgelist = './hamnet100_renamed'
#edgelist = './hamnetgraph'
if edgelist == './hamnetgraphfull':
    seeder = ['db0zb']
    servers = ['db0zb','db0bi','db0hrf','db0hex','db0hr','db0zka','db0ab','db0ins','db0ko','db0lb']
elif edgelist == './hamnet100_renamed':
    seeder = ['db0zb']
    #servers = ['db0zb'] #1
    #servers = ['db0zb','db0hex'] #2
    servers = ['db0zb','db0hex','db0ins','db0taw','db0hbg'] #5
    #servers = ['db0zb','db0hex','db0ins','db0taw','db0hbg','db0vox','db0uc','db0eam','db0hhb','db0bio'] #10
    #servers = ['db0gth', 'db0wof', 'db0mw', 'db0mhb', 'db0vox', 'db0bul', 'db0wk', 'db0cgw', 'dl1flo1', 'db0son', 'db0rvb', 'db0ins', 'db0kvk', 'db0mio', 'db0cha', 'dm0avh', 'db0mak', 'db0hsr', 'db0mac', 'db0kt', 'dm0hr', 'df0ann', 'db0uhf', 'db0bl', 'db0zw', 'db0bwl', 'db0zm', 'db0bt', 'db0zb', 'db0slk', 'db0fue', 'db0eam', 'db0ein', 'db0hal', 'db0uc', 'dm0ea', 'db0ea', 'db0eb', 'db0hhb', 'db0ktb', 'db0ktn', 'db0nes', 'db0mpq', 'db0oha', 'dg7rz1', 'db0bbg', 'db0fhc', 'db0fha', 'db0fhn', 'db0ase', 'db0tan', 'db0for', 'db0war', 'db0bio', 'df0esa', 'dl9nbj1', 'db0nhm', 'db0hof', 'db0khh', 'db0hol', 'dl8new1', 'db0bam', 'db0hq', 'db0jgk', 'db0noe', 'db0bay', 'db0sbn', 'db0kat', 'db0sn', 'db0cj', 'db0hnk', 'db0hw', 'db0hbs', 'db0dri', 'db0hbg', 'db0gj', 'db0taw', 'db0adb', 'db0hrc', 'db0faa', 'db0hzs', 'db0eml', 'df0as', 'dl1nux', 'db0hex', 'db0shg', 'dm0et', 'db0nu', 'db0yq', 'db0feu', 'db0yz', 'db0rom', 'db0fc', 'dm0svx', 'db0abc', 'db0abb', 'db0ab', 'db0abz', 'db0cra', 'db0erf'] #100
else:
    seeder = ['db0uc']
    servers = ['db0uc','db0ktn']
name = []
ip = []
FNULL = open(os.devnull, 'w')

def useDownload():
    check = False
    while check == False:
        evaluate = raw_input("Evaluate download (y/n): ")
        if evaluate in ['y','Y','yes','Yes']:
            evaluate = 'y'
            check = True
        elif evaluate in ['n','N','no','No']:
            evaluate = 'n'
            check = True
        else:
            print 'Wrong input \n'
            check = False
    if evaluate == 'y':
        return True
    else:
        return False

def chooseBoolean():
    check = False
    while check == False:
        input = raw_input("Simulate server outage (y/n): ")
        if input in ['y','yes','Y','Yes','True','true']:
            check = True
            return True
        elif input in ['n','no','N','no','false','False']:
            check = True
            return False
        else:
            print 'Wrong input \n'
            check = False

def testIterations():
    check = False
    while check == False:
        input = raw_input('Please enter number of tests: ')
        if isinstance(input, (int, long)) == True:
            size = input
            check = True
        elif isinstance(int(input), (int, long)) == True:
            size = input
            check = True
        else:
            print 'Wrong input \n'
            check = False
    if check == True:
        return size
    else:
        return 'Merkwuerdiger Fehler'

def measureTime(bo, Instance, Test, iteration):
    timeDelta = [[] for i in range(int(iteration))]
    doc = open('./measurements/%s/%s/results/time.txt' % (Instance,Test), 'w+')

    for node in name:
        if not node in seeder:
            for i in range(int(iteration)):
                with open('./measurements/%s/%s/%s/time/%s_start.txt' % (Instance, Test, i, node)) as start:
                    with open('./measurements/%s/%s/%s/time/%s_end.txt' % (Instance, Test, i, node)) as end:
                        lines1 = start.readlines()
                        lines2 = end.readlines()
                        time1 = lines1[0]
                        time2 = lines2[0]
                        time1 = datetime.strptime(time1[:23], '%Y-%m-%dT%H:%M:%S.%f') #2019-09-30 14:19:25.000
                        time2 = datetime.strptime(time2[:23], '%Y-%m-%dT%H:%M:%S.%f')
                        tmp = time2 - time1
                        tmp = tmp.total_seconds()
                timeDelta[i].append(str(tmp))
            if bo == True:
                print node
                print tmp
        else:
            for i in range(int(iteration)):
                timeDelta[i].append('0')

    for m in range(int(iteration)):
        timeDelta[m].sort(key=float)
    for l in range(len(name)):
        for o in range(int(iteration)):
            doc.write('%s ' % str(timeDelta[o][l]))
        doc.write('\n')
    doc.close()
    if bo == True:
        print (timeDelta)

def measureTraffic(bo, Instance, Test, iteration):
    bytesIN = [[] for i in range(int(iteration))]
    bytesOUT = [[] for i in range(int(iteration))]
    docIN = open('./measurements/%s/%s/results/traffic_IN.txt' % (Instance,Test), 'w+')
    docOUT = open('./measurements/%s/%s/results/traffic_OUT.txt' % (Instance,Test), 'w+')

    for i in range(int(iteration)):
        for node in name:
            bytesIN[i].append(0)
            bytesOUT[i].append(0)
            with open('measurements/%s/%s/%s/traffic/%s_IN.txt' % (Instance, Test, i, node)) as inputIN:
                with open('measurements/%s/%s/%s/traffic/%s_OUT.txt' % (Instance, Test, i, node)) as inputOUT:
                    linesIN = inputIN.readlines()
                    linesOUT = inputOUT.readlines()
                    if len(linesIN) > 2:
                        for j in range(2,len(linesIN)): # first two lines are headers
                            tmp = linesIN[j].split() # tmp[1] = bytes
                            bytesIN[i][name.index(node)] = bytesIN[i][name.index(node)] + int(tmp[1])
                            #print bytesIN[i-1][name.index(node)]
                    if len(linesOUT) > 2:
                        for k in range(2,len(linesOUT)):
                            tmp = linesOUT[k].split() # tmp[1] = bytes
                            bytesOUT[i][name.index(node)] = bytesOUT[i][name.index(node)] + int(tmp[1])

    for m in range(int(iteration)):
        bytesIN[m].sort(key=float)
        bytesOUT[m].sort(key=float)

    for l in range(len(name)):
        for o in range(int(iteration)):
            docIN.write('%s ' % str(bytesIN[o][l]))
            docOUT.write('%s ' % str(bytesOUT[o][l]))
        docIN.write('\n')
        docOUT.write('\n')
    docIN.close()
    docOUT.close()
    if bo == True:
        print (bytesIN)
        print (bytesOUT)

def findInterfaces():
    for node in name:
        interfaces = []
        doc = open('./interfaces/%s.txt' % (node), 'w+')
        with open(edgelist) as input:
            lines = input.readlines()
            for line in lines:
                if '%s ' % node in line:
                    tmp = line[:line.find(' {')]
                    nodes = tmp.split()
                    if tmp.startswith('%s ' % node) == True:
                        interfaces.append('%s-%s' % (node, nodes[1]))
                    else:
                        interfaces.append('%s-%s' % (node, nodes[0]))

        for i in range(len(interfaces)):
            if not i == len(interfaces) - 1:
                doc.write('%s\n' % interfaces[i])
            else:
                doc.write(interfaces[i])
        doc.close

def interfaceIp(host_ip):
    subprocess.call(["docker exec mn.%s sh -c 'ifconfig > interfaces.txt'" % host_ip ],stdout=FNULL, stderr=subprocess.STDOUT,shell=True)
    subprocess.call(["docker cp mn.%s:interfaces.txt ./tmp.txt'" % (host_ip) ],stdout=FNULL, stderr=subprocess.STDOUT,shell=True)
    interfaceIps = []
    doc = open('./interfaces/%s_ip.txt' % (host_ip), 'w+')
    with open('./interfaces/%s.txt' % (host_ip)) as inputName:
        with open('tmp.txt') as inputIp:
            linesName = inputName.readlines()
            linesIp = inputIp.readlines()
            for lineName in linesName:
                for lineIp in linesIp:
                    if lineName in lineIp:
                        tmp = linesIp[linesIp.index(lineIp) + 1]
                        interfaceIps.append(tmp[lineIp.find('inet addr:'):lineIp.find('  Bcast')])
                        doc.write(tmp[lineIp.find('inet addr:'):lineIp.find('  Bcast')] + '\n')
    doc.close()

def readNodes():
    global name
    name = []
    global ip
    ip = []
    with open('./infoName.txt') as infoName:
        for line in infoName.readlines():
            if not line == "":
                tmp = line
                tmp = tmp.strip("\n")
                name.append(tmp)
    with open('./infoIP.txt') as infoIP:
        for line in infoIP.readlines():
            if not line == "":
                tmp = line
                tmp = tmp.strip("\n")
                ip.append(tmp)
    print name
    print ip

def checkNetwork():
    sum = 0
    for node in set.name:
        if 'mn.'+ set.name in subprocess.check_output(['docker ps'],shell=True):
            sum = sum + 1
        else:
            print (node + ' is missing in network')
    if sum < len(set.name):
        print ('Network is not running correctly')
        exit()
    else:
        print 'Network up and running'


def setupIptables():
    for node in name:
        #print node
        subprocess.call(["docker exec mn.%s sh -c 'iptables -N IN'" % node ],stdout=FNULL, stderr=subprocess.STDOUT,shell=True)
        subprocess.call(["docker exec mn.%s sh -c 'iptables -N OUT'" % node ],stdout=FNULL, stderr=subprocess.STDOUT,shell=True)
        subprocess.call(["docker exec mn.%s sh -c 'iptables -N FOR'" % node ],stdout=FNULL, stderr=subprocess.STDOUT,shell=True)
        with open('interfaces/%s.txt' % (node)) as input:
            for line in input.readlines():
                if not line == '':
                    #print line
                    subprocess.call(["docker exec mn.%s sh -c 'iptables -I INPUT -i %s -j IN'" % (node, line)],stdout=FNULL, stderr=subprocess.STDOUT,shell=True)
                    subprocess.call(["docker exec mn.%s sh -c 'iptables -I OUTPUT -o %s -j OUT'" % (node, line)],stdout=FNULL, stderr=subprocess.STDOUT,shell=True)
                    subprocess.call(["docker exec mn.%s sh -c 'iptables -I FORWARD -i %s -j FOR'" % (node, line)],stdout=FNULL, stderr=subprocess.STDOUT,shell=True)
                    subprocess.call(["docker exec mn.%s sh -c 'iptables -I FORWARD -o %s -j FOR'" % (node, line)],stdout=FNULL, stderr=subprocess.STDOUT,shell=True)

def restartExited(): #restart stopped container
    subprocess.call(["docker ps -a | grep Exited > exited.txt"],stdout=FNULL, stderr=subprocess.STDOUT,shell=True)
    with open('./exited.txt') as doc:
        for line in doc.readlines():
            tmp = line.split()
            subprocess.call(["docker restart %s" % tmp[-1] ],stdout=FNULL, stderr=subprocess.STDOUT,shell=True)
            print ('%s was restarted' % tmp[-1])

def __init__():
    checkNetwork()
    currentInstance = datetime.strftime(datetime.now(),'%Y%m%d%H%M')
