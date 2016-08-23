#!/bin/bash

# Call this script with the parameter for the for example
# ./scriptname 1 2 3 4 5 6 7 8 9 10

if [ -n "$0" ]              # Tested variable is quoted.
then
 echo "Parameter #0 is $0"  # Need quotes to escape #
fi 

if [ -n "$1" ]              # Tested variable is quoted.
then
 echo "Parameter #1 is $1"  # Need quotes to escape #
fi 

exit 0