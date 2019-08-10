# Shell version of makeTraining.py


if [ "$#" -ne 2 ]; then
    echo "Usage: $0 INTPUT_DIR OUTPUT_DIR"
    echo
    echo "  Arguments:"
    echo "      INTPUT_DIR: directory containing full corpus from makeCorpus.py"
    echo "      OUTPUT_DIR: directory to output training corput"
    echo
    exit 1
fi

inputDir=$1
outputDir=$2

mkdir -p $outputDir
shopt -s nullglob
arr=($inputDir/*[!0-9]0)
for task in ${arr[@]};
do
    taskRoot=$(basename $task)
    taskRoot=${taskRoot%?};
    echo "Merging $taskRoot"
    mkdir -p "$outputDir/$taskRoot"

    # Find ids not in test set
    allIds=($inputDir/$taskRoot*/train.jsonl)

    goodIds=""
    for id in ${allIds[@]};
    do
        idFormat=`dirname $id`
        idFormat=`basename $idFormat`
        # if [[ ! "${testIds[@]}" =~ ${idFormat} ]]; then
            goodIds+="$id "
        # fi
    done

    #Do the merge
    ./randomMerge.sh $goodIds > "$outputDir/$taskRoot/train.jsonl"
done
