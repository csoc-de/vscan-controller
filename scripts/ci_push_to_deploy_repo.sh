#!/bin/bash

DEPLOY_REPO="csoc/dev/sensor/sensor-deployment"
DEPLOY_DIR="sensor-deployment"
STAGE_FILE="./inventories/stage/group_vars/sensors.yml"
PROD_FILE="./inventories/prod/group_vars/sensors.yml"

function apply_changes() {
  echo -n "Applying changes..."
  EXIT_CODE=0
  if [[ $CI_COMMIT_TAG =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    sed -i "s|VERSION_VSCAN_CONTROLLER: .*|VERSION_VSCAN_CONTROLLER: '${CI_COMMIT_TAG}'|g" ${STAGE_FILE}
    sed -i "s|VERSION_VSCAN_CONTROLLER: .*|VERSION_VSCAN_CONTROLLER: '${CI_COMMIT_TAG}'|g" ${PROD_FILE}
    EXIT_CODE=$?
  elif [[ $CI_COMMIT_TAG =~ ^[0-9]+\.[0-9]+\.[0-9]+-dev[0-9]*$ ]]; then
    sed -i "s|VERSION_VSCAN_CONTROLLER: .*|VERSION_VSCAN_CONTROLLER: '${CI_COMMIT_TAG}'|g" ${STAGE_FILE}
    EXIT_CODE=$?
  else
    echo -e "\nUnsupported tag trailer: ${CI_COMMIT_TAG}"
    return 1
  fi

  if [[ "$EXIT_CODE" -ne "0" ]]; then
    echo "FAILED"
    return 1
  fi

  git commit -a -m "chore(deps): Updated vscan-controller to version ${CI_COMMIT_TAG}"
  if [[ "$?" -ne "0" ]]; then
    echo "FAILED"
    return 1
  fi
  echo "OK"
}

function create_new_mr() {
  echo -n "Creating new branch..."
  git checkout -b "update"
  if [[ "$?" -ne "0" ]]; then
    echo "FAILED"
    return 1
  fi
  echo "OK"

  if ! apply_changes; then
    return 2
  fi

  echo -n "Creating new merge request..."
  git push origin HEAD:update -o merge_request.create -o merge_request.target=master -o merge_request.title="VScanner Update"
  if [[ "$?" -ne "0" ]]; then
    echo "FAILED"
    return 3
  fi
  echo "OK"
}

function update_mr() {
  BRANCH=$(echo -n "$1")

  echo -n "Switching to branch \"${BRANCH}\"..."
  git checkout "${BRANCH}"
  if [[ "$?" -ne "0" ]]; then
    echo "FAILED"
    return 1
  fi
  echo "OK"

  if ! apply_changes; then
    return 2
  fi

  echo -n "Pushing changed..."
  git push origin "${BRANCH}"
  if [[ "$?" -ne "0" ]]; then
    echo "FAILED"
    return 3
  fi
  echo "OK"
}

glab auth login --token ${SETUP_REPO_KEY} --hostname git.dev.csoc.host || exit 1
glab config set -h git.dev.csoc.host user gitlab-ci-token || exit 2
glab config set -h git.dev.csoc.host git_protocol https || exit 3
glab config set -h git.dev.csoc.host api_protocol https || exit 4
git config --global user.name "AutoMR Bot 🤖"
git config --global user.email "auto.mr.bot@dev.csoc.host"
git config --global credential.helper '!/usr/bin/glab auth git-credential' || exit 5

glab repo clone ${DEPLOY_REPO} || exit 6
cd ${DEPLOY_DIR} || exit 7
git fetch || exit 8

MERGE_REQUESTS=$(glab mr list --search "Sensor Update" --output=json | jq -r .)
MR_COUNT=$(echo -n "${MERGE_REQUESTS}" | jq length)

if [[ "${MR_COUNT}" -eq "0" ]]; then
  # Create new MR
  create_new_mr || exit 9
elif [[ "${MR_COUNT}" -eq "1" ]]; then
  SOURCE_BRANCH=$(echo -n ${MERGE_REQUESTS} | jq -r .[0].source_branch)
  # Update MR
  update_mr $SOURCE_BRANCH || exit 10
else
  echo "ERROR: Cannot choose between multiple MRs!"
  exit 11
fi
