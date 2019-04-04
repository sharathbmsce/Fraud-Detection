import sys
import os
import logging
import argparse
import traceback
from anotherclient.py import EducationClient

KEY_NAME="education"

DEFAULT_URL="http://rest-api:8008"

def _get_private_keyfile(key_name):
    '''Get the private key for key_name.'''
    home = os.path.expanduser("~")
    key_dir = os.path.join(home, ".sawtooth", "keys")
    return '{}/{}.priv'.format(key_dir, key_name)

def add(usn,name,marks):
	privkeyfile = _get_private_keyfile(KEY_NAME)
	client=EducationClient(base_url=DEFAULT_URL,key_file=privkeyfile)
	client.add(usn,name,marks)

def run():
	args=sys.argv
	if  len(args)<2:
		print("Enter arguements")
		return
	elif args[1]=="add":
		if args[2] or  args[3] or args[4]==0:
			print("Invalid No, of Arguments")
			return
		try:add(args[2],args[3],args[4])
		except:print("Cannot add")
if __name__=="__main__":
	run()

