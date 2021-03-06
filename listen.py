#!/usr/bin/python

# Practice English listening to numbers

import random

voices = ['default', 'en-scottish', 'english', 'lancashire', 'english_rp',
 'english_wmids', 'english-us', 'en-westindies']

rnd = random.Random()

def random_numeric(digitlength):
    return rnd.randint(0, 10 ** digitlength - 1)

import datetime, time

import sys, getopt, os, subprocess
usage = 'listen.py [-s <speed_def_160>] [-n]\r\n   -s: talking speed, default 160\r\n   -n: no repeat'
nullfile = open('/dev/null','w')

def summary(loop,corr_count,speed):
    print
    print "Summary of your performance:"
    print "Talking speed: "+speed
    print "Digit | Loop | Accuracy"
    print "============================"
    for i in range(1,11):
        if loop[i] > 0:
            print ("%5d" % i)+" | "+("%4d" % loop[i])+" | "+ \
                ("%6.2f"% (round(corr_count[i]*1.0/loop[i],3)*100))
        else:
            print ("%5d" % i)+" |    0 |    N/A"
    print "============================"
    print

# double triple
def dbtp(input):
    x = input.split(' ')
    for i in range(len(x)):
        if i < (len(x)-2) and x[i] == x[i+1] and x[i] == x[i+2]:
            x[i] = 'triple'
            x[i+2] = ''
        elif i < (len(x)-1) and x[i] == x[i+1]:
            x[i] = 'double'
    return ' '.join(x)

def main(argv):
    speed = '160'
    repeat = True
    try:
        opts, args = getopt.getopt(argv,"hs:n",["speed="])
    except getopt.GetoptError:
        print usage
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print usage
            sys.exit()
        if opt == '-n':
            repeat = False
        elif opt in ("-s", "--speed"):
            speed = arg
    totalloop = 0
    loop = [0] * 21
    sumtime = [0] * 21
    maxtime = [0] * 21
    mintime = [20000] * 21
    corr_count = [0] * 21
    os.system('clear')
    print "Welcome to English Digit Listening training...\r\n"
    while True:
        # generate number, read out, and wait for input
        totalloop = totalloop + 1
        time.sleep(0.5)
        if random.random() >= 0.5:
            digitlength = rnd.randint(1,10)
            d = random_numeric(digitlength)
            readout = str(d)
            answerd = readout
        else:
            readout = ""
            answerd = ""
            digitlength = 16
            for i in range(4):
                for j in range(4):
                    dig = random_numeric(1)
                    answerd = answerd + str(dig)
                    readout = readout + " " + str(dig)
                readout = readout + ","
            if random.random() >= 0.5:
                readout = readout.replace('0','o')
            if random.random() >= 0.5:
                readout = dbtp(readout)
        v = voices[rnd.randint(0,len(voices)-1)]
        p = rnd.randint(5,95)
        print
        print
        print "Inpur what you've heard: ",
        sys.stdout.flush()
        subprocess.call(['espeak', '-v', v, '-p', str(p), '-s', speed, readout], stderr=nullfile)
        tstart = datetime.datetime.now()
        answer = raw_input()
        tdur = (datetime.datetime.now() - tstart).total_seconds()
        
        loop[digitlength] = loop[digitlength] + 1
        sumtime[digitlength] = sumtime[digitlength] + tdur
        maxtime[digitlength] = max(maxtime[digitlength], tdur)
        mintime[digitlength] = min(mintime[digitlength], tdur)
        correct = answer.strip() == answerd
        if correct:
            corr_count[digitlength] = corr_count[digitlength] + 1
        print "Total Loop:   "+str(totalloop)
        print "N of Digits:  "+str(digitlength)
        print "You heard:    "+readout
        print "Your answer:  "+answer        
        print "Loop(N):      "+str(loop[digitlength])
        print "Talk Speed:   "+speed
        print "Time:         "+str(round(tdur,1))+" sec."
        

        if correct:
            print "Correct:   YES :) YES :) YES :)"
            subprocess.call(['espeak', '-p', "60", '-s', "160","correct"], stderr=nullfile)
        else:
            print "Correct:   NO  :< NO  :< NO  :<"
            subprocess.call(['espeak', '-p', "40", '-s', "130", "oh,no"], stderr=nullfile)
        print "Correct Rate: "+str(round(corr_count[digitlength]*1.0/loop[digitlength],3)*100)+"%"
        pkey = ""
        while repeat & (answer.strip() != answerd):
            print "Listen again and inpur your answer: ",
            sys.stdout.flush()
            time.sleep(0.5)
            subprocess.call(['espeak', '-p', "60", '-s', "160","repeat"], stderr=nullfile)
            time.sleep(0.5)
            subprocess.call(['espeak', '-v', v, '-p', str(p), '-s', speed, readout], stderr=nullfile)
            answer = raw_input()
            if answer.strip() == answerd:
                subprocess.call(['espeak', '-p', "60", '-s', "160","correct"], stderr=nullfile)
            else:
                subprocess.call(['espeak', '-p', "40", '-s', "200", "no"], stderr=nullfile)
        
        while True:
            pkey = raw_input("Enter to continue, 'end' to quit, 'rp' to replay, 'sum' to see score:")
            if pkey.strip() == "rp":
                subprocess.call(['espeak', '-v', v, '-p', str(p), '-s', speed, readout], stderr=nullfile)
            elif pkey.strip() == "sum":
                summary(loop, corr_count,speed)
            else:
                break
        if pkey.strip() == "end":
            break

    print
    print
    print
    summary(loop, corr_count,speed)
    print "Thanks for using and good luck!\r\n"

if __name__ == "__main__":
   main(sys.argv[1:])

