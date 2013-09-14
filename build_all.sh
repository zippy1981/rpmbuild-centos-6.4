#!/bin/sh

mkdir LOGS 2>> /dev/null

SRPMS=SPECS/*.spec
for SRPM in $SRPMS
do
  echo -n "Building source rpm $(basename $SRPM)" . . .
  rpmbuild -ba  $SRPM &> "LOGS/$(basename $SRPM .spec).$(date +%Y-%m-%d-%H.%M.%S).log" && echo "SUCCESS!" || echo "ERROR!" 
done
