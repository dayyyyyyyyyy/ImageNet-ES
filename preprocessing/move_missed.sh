# SESSION_NUM=3
# TARGET=102
# l102_1=($(seq 6242 7003))
# l102=("${l102_1[@]}")
# for i in ${l102[@]}
# do  
#     b=`printf "%.4d" $i` 
#     cp "/Volumes/ss${SESSION_NUM}backup/loaded/${TARGET}CANON/IMG_$b.JPG" "./datasets/231117/ss${SESSION_NUM}/taken/${TARGET}_IMG_$b.JPG"
# done

SESSION_NUM=2
TARGET=102
l102_1=($(seq 6242 7003))
l102=("${l102_1[@]}")
for i in ${l102[@]}
do  
    b=`printf "%.4d" $i` 
    cp "/Volumes/ss${SESSION_NUM}backup/loaded/${TARGET}CANON/IMG_$b.JPG" "./datasets/231117/ss${SESSION_NUM}/taken/${TARGET}_IMG_$b.JPG"
done