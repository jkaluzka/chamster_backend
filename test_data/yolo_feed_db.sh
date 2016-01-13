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
./add_projecttype.sh "${API_URL}/projecttypes/" "priv" "Private development project"
./add_projecttype.sh "${API_URL}/projecttypes/" "devops" "DEVOPS dedicated project"
./add_projecttype.sh "${API_URL}/projecttypes/" "x-files" "mysterious project type"


echo "adding some projects, please wait..."
# production projects
./add_project.sh "${API_URL}/projects/" "prod" "KISS" "trunk" "example url for KISS/trunk/" "some comments for KISS/trunk/"
# private projects
./add_project.sh "${API_URL}/projects/" "priv" "KISS" "branches/useryolo/branch2" "example url for KISS/branches/useryolo/branch2/" "some comments for KISS/branches/useryolo/branch2/"
./add_project.sh "${API_URL}/projects/" "priv" "YOLO-YOLO" "trunk" "example url for YOLO-YOLO/trunk/" "some comments for YOLO-YOLO/trunk/"
./add_project.sh "${API_URL}/projects/" "priv" "CHAMSTER" "trunk" "example url for CHAMSTER/trunk/" "some comments for CHAMSTER/trunk/"
./add_project.sh "${API_URL}/projects/" "priv" "FUNNY" "trunk" "example url for FUNNY/trunk/" "some comments for FUNNY/trunk/"
./add_project.sh "${API_URL}/projects/" "priv" "L.DA.VINCI" "trunk" "example url for L.DA.VINCI/trunk/" "some comments for L.DA.VINCI/trunk/"
# other projects
./add_project.sh "${API_URL}/projects/" "x-files" "X-FILES" "mulder/scully" "example url for X-FILES/mulder/scully/" "some comments for X-FILES/mulder/scully/"


#echo "adding some flows, please wait..."
# KISS/trunk/ flows
#./add_flow.sh "${API_URL}/flows/" 2 "KISS" "trunk" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" 0 "KISS/trunk flow: 2"
# KISS/branches/useryolo/branch2/ flows
#./add_flow.sh "${API_URL}/flows/" 9 "KISS" "branches/useryolo/branch2" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" 0 "KISS/trunk flow: 9"
# YOLO-YOLO/trunk/ flows
#./add_flow.sh "${API_URL}/flows/" 1 "YOLO-YOLO" "trunk" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" 0 "YOLO-YOLO/trunk flow: 1"
# CHAMSTER/trunk/ flows
#./add_flow.sh "${API_URL}/flows/" 3 "CHAMSTER" "trunk" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" 0 "CHAMSTER/trunk flow: 3"
# FUNNY/trunk/ flows
#./add_flow.sh "${API_URL}/flows/" 4 "FUNNY" "trunk" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" 0 "FUNNY/trunk flow: 4"
# L.DA.VINCI/trunk/ flows
#./add_flow.sh "${API_URL}/flows/" 1 "L.DA.VINCI" "trunk" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" 0 "L.DA.VINCI/trunk flow: 1"
#./add_flow.sh "${API_URL}/flows/" 2 "L.DA.VINCI" "trunk" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" 0 "L.DA.VINCI/trunk flow: 2"
#./add_flow.sh "${API_URL}/flows/" 3 "L.DA.VINCI" "trunk" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" 0 "L.DA.VINCI/trunk flow: 3"


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
# KISS/trunk events for flow 2
./add_event.sh "${API_URL}/events/" 2 "STARTED_washing" "KISS" "trunk" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" "useryolo" "url" 4 3 2 1 100 "uri" "base_project=KISS work_project=trunk flow_number=2"
./add_event.sh "${API_URL}/events/" 2 "STARTED_cleaning" "KISS" "trunk" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" "useryolo" "url" 4 3 2 1 100 "uri" "base_project=KISS work_project=trunk flow_number=2"
sleep 1s
./add_event.sh "${API_URL}/events/" 2 "DONE_washing" "KISS" "trunk" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" "useryolo" "url" 4 3 2 1 100 "uri" "base_project=KISS work_project=trunk flow_number=2"
./add_event.sh "${API_URL}/events/" 2 "DONE_cleaning" "KISS" "trunk" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" "useryolo" "url" 4 3 2 1 100 "uri" "base_project=KISS work_project=trunk flow_number=2"
# KISS/branches/useryolo/branch2 events for flow 9
./add_event.sh "${API_URL}/events/" 9 "STARTED_cooking" "KISS" "branches/useryolo/branch2" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" "useryolo" "url" 4 3 2 1 100 "uri" "base_project=KISS work_project=branches/useryolo/branch2 flow_number=9"
./add_event.sh "${API_URL}/events/" 9 "DONE_cooking" "KISS" "branches/useryolo/branch2" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" "useryolo" "url" 4 3 2 1 100 "uri" "base_project=KISS work_project=branches/useryolo/branch2 flow-number=9"


# YOLO-YOLO/trunk events for flow 1
./add_event.sh "${API_URL}/events/" 1 "STARTED_washing" "YOLO-YOLO" "trunk" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" "useryolo" "url" 4 3 2 1 100 "uri" "base_project=YOLO-YOLO work_project=trunk flow_number=1"
./add_event.sh "${API_URL}/events/" 1 "STARTED_cooking" "YOLO-YOLO" "trunk" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" "useryolo" "url" 4 3 2 1 100 "uri" "base_project=YOLO-YOLO work_project=trunk flow_number=1"
./add_event.sh "${API_URL}/events/" 1 "STARTED_cleaning" "YOLO-YOLO" "trunk" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" "useryolo" "url" 4 3 2 1 100 "uri" "base_project=YOLO-YOLO work_project=trunk flow_number=1"
sleep 1s
./add_event.sh "${API_URL}/events/" 1 "DONE_cooking" "YOLO-YOLO" "trunk" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" "useryolo" "url" 4 3 2 1 100 "uri" "base_project=YOLO-YOLO work_project=trunk flow_number=1"
./add_event.sh "${API_URL}/events/" 1 "DONE_cleaning" "YOLO-YOLO" "trunk" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" "useryolo" "url" 4 3 2 1 100 "uri" "base_project=YOLO-YOLO work_project=trunk flow_number=1"
./add_event.sh "${API_URL}/events/" 1 "FAILED_washing" "YOLO-YOLO" "trunk" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" "useryolo" "url" 4 3 2 1 100 "uri" "base_project=YOLO-YOLO work_project=trunk flow_number=1"


# CHAMSTER/trunk events for flow 3
./add_event.sh "${API_URL}/events/" 3 "STARTED_cleaning" "CHAMSTER" "trunk" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" "useryolo" "url" 4 3 2 1 100 "uri" "base_project=CHAMSTER work_project=trunk flow_number=3"
./add_event.sh "${API_URL}/events/" 3 "FAILED_cleaning" "CHAMSTER" "trunk" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" "useryolo" "url" 4 3 2 1 100 "uri" "base_project=CHAMSTER work_project=trunk flow_number=3"


# FUNNY/reunk events for flow 4
./add_event.sh "${API_URL}/events/" 4 "STARTED_washing" "FUNNY" "trunk" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" "useryolo" "url" 4 3 2 1 100 "uri" "base_project=FUNNY work_project=trunk flow_number=4"
./add_event.sh "${API_URL}/events/" 4 "STARTED_cooking" "FUNNY" "trunk" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" "useryolo" "url" 4 3 2 1 100 "uri" "base_project=FUNNY work_project=trunk flow_number=4"
./add_event.sh "${API_URL}/events/" 4 "STARTED_cleaning" "FUNNY" "trunk" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" "useryolo" "url" 4 3 2 1 100 "uri" "base_project=FUNNY work_project=trunk flow_number=4"
sleep 1s
./add_event.sh "${API_URL}/events/" 4 "FAILED_washing" "FUNNY" "trunk" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" "useryolo" "url" 4 3 2 1 100 "uri" "base_project=FUNNY work_project=trunk flow_number=4"
./add_event.sh "${API_URL}/events/" 4 "FAILED_cooking" "FUNNY" "trunk" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" "useryolo" "url" 4 3 2 1 100 "uri" "base_project=FUNNY work_project=trunk flow_number=4"
./add_event.sh "${API_URL}/events/" 4 "FAILED_cleaning" "FUNNY" "trunk" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" "useryolo" "url" 4 3 2 1 100 "uri" "base_project=FUNNY work_project=trunk flow_number=4"


# L.DA.VINCI/trunk events for flow 1
./add_event.sh "${API_URL}/events/" 1 "STARTED_cooking" "L.DA.VINCI" "trunk" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" "useryolo" "url" 4 3 2 1 100 "uri" "base_project=L.DA.VINCI work_project=trunk flow_number=1"
./add_event.sh "${API_URL}/events/" 1 "FAILED_cooking" "L.DA.VINCI" "trunk" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" "useryolo" "url" 4 3 2 1 100 "uri" "base_project=L.DA.VINCI work_project=trunk flow_number=1"
sleep 1s
# L.DA.VINCI/trunk events for flow 2
./add_event.sh "${API_URL}/events/" 2 "STARTED_cooking" "L.DA.VINCI" "trunk" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" "useryolo" "url" 4 3 2 1 100 "uri" "base_project=L.DA.VINCI work_project=trunk flow_number=2"
./add_event.sh "${API_URL}/events/" 2 "FAILED_cooking" "L.DA.VINCI" "trunk" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" "useryolo" "url" 4 3 2 1 100 "uri" "base_project=L.DA.VINCI work_project=trunk flow_number=2"
sleep 1s
# L.DA.VINCI/trunk events for flow 3
./add_event.sh "${API_URL}/events/" 3 "STARTED_cooking" "L.DA.VINCI" "trunk" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" "useryolo" "url" 4 3 2 1 100 "uri" "base_project=L.DA.VINCI work_project=trunk flow_number=3"
./add_event.sh "${API_URL}/events/" 3 "FAILED_cooking" "L.DA.VINCI" "trunk" "$(date +'%Y-%m-%d %H:%M:%S.%6N')" "useryolo" "url" 4 3 2 1 100 "uri" "base_project=L.DA.VINCI work_project=trunk flow_number=3"

echo "yolo!"

