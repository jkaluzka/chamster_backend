#!/bin/bash
#set -x
set -e
set -u


API_URL=${1}
PROJECT_TYPE=${2}
BASE_PROJECT=${3}
WORK_PROJECT=${4}
PROJECT_URL=${5}
COMMENTS=${6}

OUT_DIR=data/add_project
OUT_FILE=${OUT_DIR}/payload.json

mkdir -pv ${OUT_DIR}

echo "
{
\"project_type\": \"${PROJECT_TYPE}\",
\"base_project\": \"${BASE_PROJECT}\",
\"work_project\": \"${WORK_PROJECT}\",
\"project_url\": \"${PROJECT_URL}\",
\"comments\": \"${COMMENTS}\"
}
" > ${OUT_FILE}

cat ${OUT_FILE}

curl -X POST ${API_URL} -H "Content-Type: application/json" --data "@${OUT_FILE}"

