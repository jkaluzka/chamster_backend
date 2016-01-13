#!/bin/bash
#set -x
set -e
set -u


API_URL=${1}
FLOW=${2}
EVENT_TYPE=${3}
BASE_PROJECT=${4}
WORK_PROJECT=${5}
TIMESTAMP=${6}
USER=${7}
COMMENTS=${8}


OUT_DIR=data/add_event
OUT_FILE=${OUT_DIR}/payload.json

mkdir -p ${OUT_DIR}

echo "
{
\"flow\": ${FLOW},
\"event_type\": \"${EVENT_TYPE}\",
\"base_project\": \"${BASE_PROJECT}\",
\"work_project\": \"${WORK_PROJECT}\",
\"timestamp\": \"${TIMESTAMP}\",
\"user\": \"${USER}\",
\"comments\": \"${COMMENTS}\"
}
" > ${OUT_FILE}

cat ${OUT_FILE}

curl -X POST ${API_URL} -H "Content-Type: application/json" --data "@${OUT_FILE}"

