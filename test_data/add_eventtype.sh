#!/bin/bash
#set -x
set -e
set -u


API_URL=${1}
NAME=${2}
COMMENTS=${3}

OUT_DIR=data/add_eventtype
OUT_FILE=${OUT_DIR}/payload.json

mkdir -pv ${OUT_DIR}

echo "
{
\"name\": \"${NAME}\",
\"comments\": \"${COMMENTS}\"
}
" > ${OUT_FILE}

cat ${OUT_FILE}

curl -X POST ${API_URL} -H "Content-Type: application/json" --data "@${OUT_FILE}"

