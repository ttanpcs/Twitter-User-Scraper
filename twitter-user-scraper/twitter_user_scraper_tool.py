#!/usr/bin/env python
"""Twitter User Scraper Tool

This script allows the user to find various statistics for the users
specified in the command line arguments.

This tool either accepts all non flagged parameters as string usernames
or accepts an input file location with the flag --input.
The --output flag allows the user to change the output location from
'user_information.json'
"""

import argparse
import os
import twitter_user_scraper as tus
import user_data_handler as udh

bearer_token = os.environ.get("BEARER_TOKEN")

def main(args):
    """Scrape twitter for information on specified arguments
    
    If either 'names' or '--input' are not passed, the program will stop. 
    The program prioritizes 'names' before 'input'

    Parameters
    ----------
    args : argument namespace
        All command line arguments as parsed by argparse
    """

    username_list = []
    if (len(args.names) == 0 and (args.input is None)):
        print("Please input either a list of usernames or an input file path\n")
        return 0

    if (len(args.names) != 0):
        username_list = [user.strip() for user in args.names]
    elif (args.input is not None):
        with open(args.input) as infile:
            username_list = [user.strip() for user in infile.readlines()]
    scraper = tus.TwitterUserScraper(bearer_token, username_list, args.followers, args.timeline)
    user_data_list = scraper.parse()
    handler = udh.UserDataHandler()
    handler.write_users_to_file(user_data_list, args.output)

    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Functional Twitter user information scraper.")
    parser.add_argument("names", nargs = "*", help = "Twitter usernames to scrape information from")
    parser.add_argument("--input", "-i", help = "input file path")
    parser.add_argument( "--output", "-o", help = "output file path (default: user_information.json)", default = "user_information.json")
    parser.add_argument("--followers", "-f", help = "Adds followers statistics to dataset", action = "store_true")
    parser.add_argument("--timeline", "-t", help = "Adds timeline statistics to dataset", action = "store_true")

    args = parser.parse_args()
    main(args)
