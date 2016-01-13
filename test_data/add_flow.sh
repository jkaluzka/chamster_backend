#!/bin/bash
#set -x
set -e
set -u


API_URL=${1}
NUMBER=${2}
BASE_PROJECT=${3}
WORK_PROJECT=${4}
TIMESTAMP=${5}
STATUS=${6}
COMMENTS=${7}

OUT_DIR=data/add_flow
OUT_FILE=${OUT_DIR}/payload.json

mkdir -pv ${OUT_DIR}

echo "
{
\"number\": ${NUMBER},
\"base_project\": \"${BASE_PROJECT}\",
\"work_project\": \"${WORK_PROJECT}\",
\"timestamp\": \"${TIMESTAMP}\",
\"status\": \"${STATUS}\",
\"comments\": \"${COMMENTS}\"
}
" > ${OUT_FILE}

cat ${OUT_FILE}

curl -X POST ${API_URL} -H "Content-Type: application/json" --data "@${OUT_FILE}"

