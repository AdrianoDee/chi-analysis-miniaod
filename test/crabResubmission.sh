#!/bin/bash

arg=$1

find ${arg}/*/ -name "crab_*" >& taskName.txt

echo "CRAB Task List have been created"

crabRS=crabResubmit

cat>> ${crabRS}.sh <<rSfile
#!/bin/bash

counter=0

while IFS='' read -r line || [[ -n "\$line" ]]; do

counter=\$((counter+1))
echo "\$counter"
echo " \$line "
echo " "
crab resubmit \$line
echo " "

done < "\$1"
rSfile

echo " "
echo "${crabRS}.sh have been created"
chmod a+x ${crabRS}.sh
echo " "
echo "${crabRS}.sh is executable now"
echo " "

./${crabRS}.sh taskName.txt

mv ${crabRS}.sh ${crabRS}_Old.sh
mv taskName.txt taskName_Old.txt

echo " "
echo "SL************************************************SL"
echo "SL************************************************SL"
echo "SL************* MISSION COMPLETED ****************SL"
echo "SL************************************************SL"
echo "SL************************************************SL"
echo "SL********** You can drink a coffee **************SL"
echo "SL************************************************SL"
echo "SL************************************************SL"
echo " "

