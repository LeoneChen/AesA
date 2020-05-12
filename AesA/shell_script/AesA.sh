# Author: Liheng Chen
# Organization: ISCAS, China

cd ../../arachne-all/Arachne || exit
make -j$(nproc) -s
cd ../../AesA || exit
mkdir -p bin
make AES_MT_MODE="$1"

mkdir -p out/"$1"
for k in {"100b","1k","10k","100k","1m","10m","100m"}; do
  for j in {2,4,6}; do
    for i in {1..5}; do
      t=$(expr $j / 2)
      for l in {1..5}; do
        echo $k $j $t $i
        ./bin/AesATest --minNumCores $j --maxNumCores $j $t "data/${k}.txt" >./out/"$1"/"$k"_"$1"_"$j"core_"$t"thread_"$i"round.txt
        t=$(expr $t \* 2)
      done
    done
  done
done
