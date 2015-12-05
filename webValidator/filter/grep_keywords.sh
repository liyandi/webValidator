#!/bin/bash
##################################
# AUTHOR : Yandi LI
# CREATED_AT : 2015-09-01
# RUN : 
# TASK : grep charactors
##################################
if [ -f /etc/bashrc ]; then
  . /etc/bashrc
  . /data0/yandi/.bashrc
fi
wrkdir=/data0/yandi/project/toutiao/webpage_validator/validator/data/
outdir=/data0/yandi/project/toutiao/feed/data/output/
                      
<< COMMENT
for i in $(seq 1 20)
do
  dt=$(date -d "$i days ago" +%Y%m%d)
  echo $dt

  echo "=============================="
  echo "      COLLECTING DATA         "
  echo "=============================="
  cat ${outdir}/${dt}/*out|gawk -F '\t' '{print $2$3}'|grep -o .|sort|uniq -c|sort -k1,1 -nr -o  ${wrkdir}/coding/sdata/${dt}
  echo -e "\n==============DONE================"
done;
COMMENT

gawk '{arr[$2]+=$1;} END {for (i in arr) print i, arr[i]}' ${wrkdir}/coding/sdata/*|sort -k2,2 -nr -o ${wrkdir}/../conf/common_chars.conf
