#!/bin/bash
BASEDIR=`dirname "$0"`/..

${BASEDIR}/utils/extract_test_predictions.py ${BASEDIR}/data/test.txt ${BASEDIR}/data/results/res2.txt | ${BASEDIR}/perf.src/perf -ROC