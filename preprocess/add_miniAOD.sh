#!/bin/bash
#=========================================================================================
# add_miniAOD.sh -------------------------------------------------------------------------
#=========================================================================================

echo "Welcome to a simple file listing script"

FileNumber=$(eos root://cmseos.fnal.gov/ ls /store/user/bregnery/MinBias/NLO_step6_VLQ_MiniAOD/211011_204431/0000/ | wc -l )

rm NLO_files.txt
touch NLO_files.txt

for File in {1..151}
    do 
        echo "root://cmseos.fnal.gov//store/user/bregnery/MinBias/NLO_step6_VLQ_MiniAOD/211011_204431/0000/NLO_VLQ_custom_MiniAOD_${File}.root" >> NLO_files.txt
done    

#echo "Merging files: "

#edmCopyPickMerge inputFiles_load=NLO_files.txt outputFile=NLO_VLQ_custom_MiniAOD.root     maxSize=1000000

#hadd -f NLO_VLQ_custom_MiniAOD.root $FileNames

#eos root://cmseos.fnal.gov/ ls /store/user/bregnery/MinBias/NLO_step6_VLQ_MiniAOD/211011_204431/0000/ | grep `NLO_VLQ_custom_MiniAOD.root`



#hadd NLO_VLQ_custom_MiniAOD.root $(eos root://cmseos.fnal.gov/ ls /store/user/bregnery/MinBias/NLO_step6_VLQ_MiniAOD/211011_204431/0000/ | grep `NLO_VLQ_custom_MiniAOD.root`)




