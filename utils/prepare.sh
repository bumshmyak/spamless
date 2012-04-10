#!/bin/bash

BASEDIR=`dirname "$0"`/..

LABELS_FILE="data/labels.txt"
shuf ${BASEDIR}/${LABELS_FILE} > tmp
mv tmp ${BASEDIR}/${LABELS_FILE}

# split data into training and testing set
head -10000 ${BASEDIR}/${LABELS_FILE} > ${BASEDIR}/data/train_labels.txt
tail -3491 ${BASEDIR}/${LABELS_FILE} > ${BASEDIR}/data/test_labels.txt

# prepare features
OBVIOUS_FEATURES_FILE=${BASEDIR}/data/uk-2007-05.obvious_features.csv
LINK_FEATURES_FILE=${BASEDIR}/data/uk-2007-05.link_based_features.csv
PAGERANK=${BASEDIR}/data/pagerank.txt
FEATURES_FILE=${BASEDIR}/data/features.csv

cut -f 3,4 -d ',' ${OBVIOUS_FEATURES_FILE} > tmp
paste -d ',' ${LINK_FEATURES_FILE} ${PAGERANK} tmp > ${FEATURES_FILE}
rm tmp

${BASEDIR}/utils/prepare_train_control.py ${FEATURES_FILE} ${BASEDIR}/data/train_labels.txt > ${BASEDIR}/data/prepared_train.txt
${BASEDIR}/utils/prepare_train_control.py ${FEATURES_FILE} > ${BASEDIR}/data/prepared_control.txt

<<EOF
FEATURE_NAMES_FILE=${BASEDIR}/data/uk-2007-05.link_based_features_header.csv
cat ${BASEDIR}/data/prepared_train.txt | \
    ${BASEDIR}/utils/convert_prepared_set_to_arff.py -n ${FEATURE_NAMES_FILE} -l >\
    ${BASEDIR}/data/prepared_train.arff

cat ${BASEDIR}/data/prepared_control.txt | \
    ${BASEDIR}/utils/convert_prepared_set_to_arff.py -n ${FEATURE_NAMES_FILE} >\
    ${BASEDIR}/data/prepared_control.arff
EOF