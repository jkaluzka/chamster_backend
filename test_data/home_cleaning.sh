#!/bin/bash
#set -x
set -e
set -u


if [ $# -ne 1 ] ; then
    >&2 echo "error! missing API_URL param!"
    >&2 echo "example usage:"
    >&2 echo "$0 \"http://127.0.0.1:8000/api\""
    exit 1
fi


#API_URL e.g.:
# "localhost:7000/api" or "http://192.168.1.16:9090/api"

readonly API_URL="${1}"


echo ""

echo "adding some project types, please wait..."
./add_projecttype.sh "${API_URL}/projecttypes/" "prod" "Official production project"


echo "adding some projects, please wait..."
# production projects
./add_project.sh "${API_URL}/projects/" "prod" "HOME_CLEANING" "branches/mrproper" "example url for HOME_CLEANING/branches/mrproper/" "some comments for HOME_CLEANING/branches/mrproper/"


echo "adding some flows, please wait..."
# HOME_CLEANING/branches/mrproper/ flows
./add_flow.sh "${API_URL}/flows/" 11 "HOME_CLEANING" "branches/mrproper" "2015-12-06 05:00:00.000000" 0 "HOME_CLEANING/branches/mrproper flow: 11 (created by add_flow.sh script for test purposes)"
./add_flow.sh "${API_URL}/flows/" 12 "HOME_CLEANING" "branches/mrproper" "2015-12-06 05:10:11.000000" 0 "HOME_CLEANING/branches/mrproper flow: 12 (created by add_flow.sh script for test purposes)"
./add_flow.sh "${API_URL}/flows/" 13 "HOME_CLEANING" "branches/mrproper" "2015-12-06 05:20:12.000000" 0 "HOME_CLEANING/branches/mrproper flow: 13 (created by add_flow.sh script for test purposes)"
./add_flow.sh "${API_URL}/flows/" 14 "HOME_CLEANING" "branches/mrproper" "2015-12-06 05:30:13.000000" 0 "HOME_CLEANING/branches/mrproper flow: 14 (created by add_flow.sh script for test purposes)"
./add_flow.sh "${API_URL}/flows/" 15 "HOME_CLEANING" "branches/mrproper" "2015-12-06 05:40:14.000000" 0 "HOME_CLEANING/branches/mrproper flow: 15 (created by add_flow.sh script for test purposes)"
./add_flow.sh "${API_URL}/flows/" 16 "HOME_CLEANING" "branches/mrproper" "2015-12-06 05:50:15.000000" 0 "HOME_CLEANING/branches/mrproper flow: 16 (created by add_flow.sh script for test purposes)"
./add_flow.sh "${API_URL}/flows/" 17 "HOME_CLEANING" "branches/mrproper" "2015-12-06 06:00:00.000000" 0 "HOME_CLEANING/branches/mrproper flow: 17 (created by add_flow.sh script for test purposes)"
./add_flow.sh "${API_URL}/flows/" 18 "HOME_CLEANING" "branches/mrproper" "2015-12-06 06:10:00.000000" 0 "HOME_CLEANING/branches/mrproper flow: 18 (created by add_flow.sh script for test purposes)"
./add_flow.sh "${API_URL}/flows/" 19 "HOME_CLEANING" "branches/mrproper" "2015-12-06 06:20:00.000000" 0 "HOME_CLEANING/branches/mrproper flow: 19 (created by add_flow.sh script for test purposes)"
./add_flow.sh "${API_URL}/flows/" 20 "HOME_CLEANING" "branches/mrproper" "2015-12-06 06:30:00.000000" 0 "HOME_CLEANING/branches/mrproper flow: 20 (created by add_flow.sh script for test purposes)"
./add_flow.sh "${API_URL}/flows/" 21 "HOME_CLEANING" "branches/mrproper" "2015-12-06 06:40:00.000000" 0 "HOME_CLEANING/branches/mrproper flow: 21 (created by add_flow.sh script for test purposes)"
./add_flow.sh "${API_URL}/flows/" 22 "HOME_CLEANING" "branches/mrproper" "2015-12-06 06:50:00.000000" 0 "HOME_CLEANING/branches/mrproper flow: 22 (created by add_flow.sh script for test purposes)"
./add_flow.sh "${API_URL}/flows/" 23 "HOME_CLEANING" "branches/mrproper" "2015-12-06 07:00:12.000000" 0 "HOME_CLEANING/branches/mrproper flow: 23 (created by add_flow.sh script for test purposes)"
./add_flow.sh "${API_URL}/flows/" 24 "HOME_CLEANING" "branches/mrproper" "2015-12-06 07:10:13.000000" 0 "HOME_CLEANING/branches/mrproper flow: 24 (created by add_flow.sh script for test purposes)"
./add_flow.sh "${API_URL}/flows/" 25 "HOME_CLEANING" "branches/mrproper" "2015-12-06 07:20:14.000000" 0 "HOME_CLEANING/branches/mrproper flow: 25 (created by add_flow.sh script for test purposes)"
./add_flow.sh "${API_URL}/flows/" 26 "HOME_CLEANING" "branches/mrproper" "2015-12-06 07:30:15.000000" 0 "HOME_CLEANING/branches/mrproper flow: 26 (created by add_flow.sh script for test purposes)"
./add_flow.sh "${API_URL}/flows/" 27 "HOME_CLEANING" "branches/mrproper" "2015-12-06 07:40:00.000000" 0 "HOME_CLEANING/branches/mrproper flow: 27 (created by add_flow.sh script for test purposes)"
./add_flow.sh "${API_URL}/flows/" 28 "HOME_CLEANING" "branches/mrproper" "2015-12-06 07:50:00.000000" 0 "HOME_CLEANING/branches/mrproper flow: 28 (created by add_flow.sh script for test purposes)"
./add_flow.sh "${API_URL}/flows/" 29 "HOME_CLEANING" "branches/mrproper" "2015-12-06 08:00:00.000000" 0 "HOME_CLEANING/branches/mrproper flow: 29 (created by add_flow.sh script for test purposes)"
./add_flow.sh "${API_URL}/flows/" 30 "HOME_CLEANING" "branches/mrproper" "2015-12-06 08:30:00.000000" 0 "HOME_CLEANING/branches/mrproper flow: 30 (created by add_flow.sh script for test purposes)"


echo "adding some event types, please wait..."
./add_eventtype.sh "${API_URL}/eventtypes/" "STARTED_washing" "some comments for STARTED_washing event"
./add_eventtype.sh "${API_URL}/eventtypes/" "DONE_washing" "some comments for DONE_washing event"
./add_eventtype.sh "${API_URL}/eventtypes/" "FAILED_washing" "some comments for FAILED_washing event"

./add_eventtype.sh "${API_URL}/eventtypes/" "STARTED_cooking" "some comments for STARTED_cooking event"
./add_eventtype.sh "${API_URL}/eventtypes/" "DONE_cooking" "some comments for DONE_cooking event"
./add_eventtype.sh "${API_URL}/eventtypes/" "FAILED_cooking" "some comments for FAILED_cooking event"

./add_eventtype.sh "${API_URL}/eventtypes/" "STARTED_cleaning" "some comments for STARTED_cleaning event"
./add_eventtype.sh "${API_URL}/eventtypes/" "DONE_cleaning" "some comments for DONE_cleaning event"
./add_eventtype.sh "${API_URL}/eventtypes/" "FAILED_cleaning" "some comments for FAILED_cleaning event"


echo "adding some events, please wait..."
# HOME_CLEANING/branches/mrproper events for flow 11
./add_event.sh "${API_URL}/events/" 11 "STARTED_washing" "HOME_CLEANING" "branches/mrproper" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" "useryolo" "base_project=HOME_CLEANING work_project=branches/mrproper flow_number=11"
./add_event.sh "${API_URL}/events/" 11 "STARTED_cleaning" "HOME_CLEANING" "branches/mrproper" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" "useryolo" "base_project=HOME_CLEANING work_project=branches/mrproper flow_number=11"
sleep 1s
./add_event.sh "${API_URL}/events/" 11 "DONE_washing" "HOME_CLEANING" "branches/mrproper" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" "useryolo" "base_project=HOME_CLEANING work_project=branches/mrproper flow_number=11"
./add_event.sh "${API_URL}/events/" 11 "DONE_cleaning" "HOME_CLEANING" "branches/mrproper" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" "useryolo" "base_project=HOME_CLEANING work_project=branches/mrproper flow_number=11"
./add_event.sh "${API_URL}/events/" 11 "STARTED_cooking" "HOME_CLEANING" "branches/mrproper" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" "useryolo" "base_project=HOME_CLEANING work_project=branches/mrproper flow_number=11"
./add_event.sh "${API_URL}/events/" 11 "DONE_cooking" "HOME_CLEANING" "branches/mrproper" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" "useryolo" "base_project=HOME_CLEANING work_project=branches/mrproper flow-number=11"

./add_event.sh "${API_URL}/events/" 51 "DONE_cooking" "HOME_CLEANING" "branches/mrproper" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" "useryolo" "base_project=HOME_CLEANING work_project=branches/mrproper flow-number=11"

echo "let's clean here!"

