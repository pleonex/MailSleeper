#!/bin/python3
# -*- coding: utf-8 -*-
###############################################################################
#  Delay your email notification some hours - V1.0                            #
#  Copyright 2015 Benito Palacios (aka pleonex)                               #
#                                                                             #
#  Licensed under the Apache License, Version 2.0 (the "License");            #
#  you may not use this file except in compliance with the License.           #
#  You may obtain a copy of the License at                                    #
#                                                                             #
#      http://www.apache.org/licenses/LICENSE-2.0                             #
#                                                                             #
#  Unless required by applicable law or agreed to in writing, software        #
#  distributed under the License is distributed on an "AS IS" BASIS,          #
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.   #
#  See the License for the specific language governing permissions and        #
#  limitations under the License.                                             #
###############################################################################

import imaplib
import getpass
import time

# Connect to the server
IMAP_SERVER = 'imap.google.com'
mail = imaplib.IMAP4_SSL('imap.gmail.com')

# Create a connection and login
email = input('E-mail: ')
pwd = getpass.getpass()
mail.login(email, pwd)

# Ask for the hours to delay
delay_start = time.strptime(input('Delay start (HH:MM): '), "%H:%M")
delay_start = delay_start.tm_hour * 60 + delay_start.tm_min
print("-> " + str(delay_start))
delay_end = time.strptime(input('Delay end (HH:MM): '), "%H:%M")
delay_end = delay_end.tm_hour * 60 + delay_end.tm_min
print("-> " + str(delay_end))

# Select main box
mail.select("inbox")

# List to store unseen msg.
unseen_uid = []

# Main loop
while True:
    print("Polling...")

    # Get current time
    current_time = time.localtime()
    current_time = current_time.tm_hour * 60 + current_time.tm_min
    print("\tCurrent time: " + str(current_time))

    # Check the mode we are
    if current_time >= delay_start and current_time < delay_end:
        # If we need to delay, mark all messages as seen
        print("\tDelaying messages...")
        result, data = mail.uid('search', None, 'UNSEEN')
        for uid in data[0].split():
            unseen_uid.append(uid)
            mail.uid('store', uid, '+FLAGS', '\\Seen')

    else:
        # After delay, mark again as unseen all fake seen messages
        print("\tUndoing things...")
        for uid in unseen_uid:
            mail.uid('store', uid, '-FLAGS', '\\Seen')
        del unseen_uid[:]

    # Sleep for the next minute
    print("\tSleeping...")
    time.sleep(60)
