#!/bin/bash

BASEDIR=`dirname "$0"`/..

SET1_LABELS_FILE="data/webspam-uk2007-set1-1.0/WEBSPAM-UK2007-SET1-labels.txt"

# split data into training and testing set
head -3000 ${BASEDIR}/${SET1_LABELS_FILE} | grep -v " - " > ${BASEDIR}/data/train.txt
tail -1275 ${BASEDIR}/${SET1_LABELS_FILE} | grep -v " - " > ${BASEDIR}/data/test.txt

# prepare features
FEATURES_FILE=${BASEDIR}/data/uk-2007-05.link_based_features.csv
${BASEDIR}/utils/make_training_set.py ${BASEDIR}/data/train.txt ${FEATURES_FILE} > ${BASEDIR}/data/prepared_train.txt
${BASEDIR}/utils/make_control_set.py ${FEATURES_FILE} > ${BASEDIR}/data/prepared_control.txt
