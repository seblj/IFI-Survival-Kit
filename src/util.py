import argparse
import subprocess
from .errors import NoUsernameError, NoTokenError, NoPackageError
from pip._internal import main as pipmain

def parseArgs(textColor):
    ''' Parses arguments and handles all the user input at the initial part of the script
    Should return the final username and token for the script to use 
    '''

    desc = '''
    This is a small script helping with setting up a folder structure based on a configuration.

    The script will parse through the structure.json file within the same folder, and 
    create a folder structure, with a matching github structure
    '''

    parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-u', '--username', metavar="STR", type=str, help='Github username')
    parser.add_argument('-t','--token', metavar="NUM", type=int, help='Personal access token')
    parser.add_argument('-v', '--verbose', help="increase output verbosity", action="store_true")
    args = parser.parse_args()
    
    if not args.username or args.token:
        print("%sSome parameters was omitted.%s\nChecking global git config for defaults...%s" % (textColor.red, textColor.blue, textColor.blue))
        configUsername = subprocess.Popen("git config --global user.name", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip("\n")
        configToken = subprocess.Popen("git config --global user.token", shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').strip("\n")
    
    # Ask user for username
    if not (args.username):
        print("%sPlease enter your Github username:" % (textColor.purple), end='')
        # Check if there was a configUsername, if so supply it as arg
        if (configUsername != ""):
            print("%s (defaulting to: '%s')%s" % (textColor.green, configUsername, textColor.reset))
        else:
            print("%s (no default found)%s" % (textColor.blue, textColor.reset))
        inputUsername = input()
        if (inputUsername == ""):
            if (configUsername == ""):
                raise NoUsernameError
            else:
                username = configUsername
        else:
            username = inputUsername

    # Ask for user token
    if not (args.token):
        print("%sPlease enter your Github access token:" % (textColor.purple), end='')
        if (configToken != ""):
            print("%s(default '%s') %s" % (textColor.green, configToken, textColor.reset))
        else:
            print("%s (no default found)%s" % (textColor.blue, textColor.reset))
        inputToken = input()
        if (inputUsername == ""):
            if (configToken == ""):
                raise NoTokenError
            else:
                token = configToken
        else:
            token = inputToken

    return username, token

def import_or_install(package, textColor, emoji):
    try:
        __import__(package)
    except ImportError:
        print(("%s %sPackage %s%s %sis missing Do you want to install it through pip?") % (emoji.package, textColor.blue, textColor.purple, package, textColor.blue), end="")
        res = input(("%s (y/n) ") % (textColor.green))

        if (res == "y" or res == "Y"):
            pipmain(['install', package])
        else:
            raise NoPackageError(package)