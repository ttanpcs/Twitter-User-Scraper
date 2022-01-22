#!/usr/bin/env python
"""Twitter User Scraper Tool

This script allows the user to find various statistics for the users
specified in the command line arguments.

This tool either accepts all non flagged parameters as string usernames
or accepts an input file location with the flag --input.
The --output flag allows the user to change the output location from
'user_information.csv'
"""

import argparse
import os

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

    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Functional Twitter user information scraper.")
    parser.add_argument("names", nargs = "*", help = "Twitter usernames to scrape information from")
    parser.add_argument("--input", "--i", help = "input file path")
    parser.add_argument( "--output", "--o", help = "output file path (default: user_information.csv)", default = "user_information.csv")
    args = parser.parse_args()

    main(args)
