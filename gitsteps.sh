#!/bin/bash -eu
push=${1}
commitnote=${2}

git add .
git commit -m "$commitnote"

echo "added and commmitted"

if [[ $push -eq 1 ]]
then
	git commit; echo "and pushed"
fi
