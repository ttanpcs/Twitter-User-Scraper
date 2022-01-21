#!/usr/bin/env python

import argparse

def main(args):
    """Scrape twitter for information on specified arguments"""
    return 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Functional Twitter user information scraper.")
    parser.add_argument("names", nargs = "*", help = "Twitter usernames to scrape information from")
    parser.add_argument("--input", "--i", help = "input file path")
    parser.add_argument( "--output", "--o", help = "output file path (default: user_information.csv)", default = "user_information.csv")
    args = parser.parse_args()

    main(args)
