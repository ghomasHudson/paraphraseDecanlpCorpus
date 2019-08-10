# Randomly merge multiple files
# e.g. for each line randomly pick a version of that line from one of the files
# Files must be of equal length

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 [FILES]"
    exit 1
fi

inputFiles=("$@")
numLines=$(wc -l "${inputFiles[0]}" | awk "{print \$1}")
numFiles=${#inputFiles[@]}

get_fair_partition()
{
    # Divide len(shuffledLines) as evenly as possible across $numFiles
    idx=$1
    var=${#lineIdxs[@]}
    slots=$numFiles
    result=$((var / slots))
    k=$((var % slots ))

    for ((i=0; i<k; i++)); do
        partitionLen[i]=$(( result + 1 ))
    done
    for ((i=k; i < slots; i++)); do
        partitionLen[i]=$result
    done

    #Get cumulative sum
    sum=0
    for ((i=0; i < idx; i++)); do
        sum=$(($sum+${partitionLen[$i]}))
    done
    echo $sum

}

get_split()
{
    index=$1
    startPoint=$(get_fair_partition $index)
    endPoint=`get_fair_partition $(($index+1))`
    #echo "$startPoint to $endPoint"
    outputStr=""

    for ((i=$startPoint; i < $endPoint; i++)); do
        l=${lineIdxs[$i]}
        outputStr+="-e ${l}p "
    done
    echo "$outputStr"

}

get_seeded_random()
{
  seed="$1"
  openssl enc -aes-256-ctr -pass pass:"$seed" -nosalt \
    </dev/zero 2>/dev/null
}

# Get a randomly shuffled array from 1 - numlines
readarray -t lineIdxs < <(shuf -i1-$numLines --random-source=<(get_seeded_random 42))

j=0
for f in "${inputFiles[@]}"
do
    cat -n $f | sed -n `get_split $j`
    j=$((j+1))
done | sort -n -k 1 | cut -f 2- #Sort back into order at the end
