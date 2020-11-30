#!/bin/bash

DATASET_NAME="luslab"
URL="http://40.120.39.12:5984/"
USR="admin"
PW="dnMNDkDFS2Pj"
DB="luscan"
SCAN_DIR='/Users/cheshic/dev/repos/arshamg-scrnaseq-wgan'
OUT_DIR="/Users/cheshic/dev/test-data/space_util/"

TEST_SET_NAME="scan.csv"
SCAN_HIST_NAME="scan_hist.csv"
SUMMARY_NAME="size_summary.csv"

TEST_SET_PATH="$OUT_DIR$TEST_SET_NAME"

echo "running luscan test script"

# Delete and rebuild the database
python main.py testdb --url $URL --usr $USR --pw $PW --db $DB && \
python main.py rebuild --url $URL --usr $USR --pw $PW --db $DB && \
python main.py testdb --url $URL --usr $USR --pw $PW --db $DB && \

# Scan some data
python main.py scan --path $SCAN_DIR --output $TEST_SET_PATH --ignore_hidden True --set_name $DATASET_NAME && \

# Upload to db
python main.py upload --url $URL --usr $USR --pw $PW --db $DB --path $TEST_SET_PATH && \

Call all test views and output data to file
python main.py view --url $URL --usr $USR --pw $PW --db $DB --view_name "scan_hist" --output "$OUT_DIR$SCAN_HIST_NAME" && \
python main.py view --url $URL --usr $USR --pw $PW --db $DB --view_name "size_summary" --output "$OUT_DIR$SUMMARY_NAME"