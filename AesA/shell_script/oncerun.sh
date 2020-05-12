# Author: Liheng Chen
# Organization: ISCAS, China

cd ../../arachne-all/Arachne ||exit
make -j"$(nproc)" -s
cd ../../AesA||exit
make AES_MT_MODE="$1"

./bin/AesATest --minNumCores "$2" --maxNumCores "$2" "$3" "$4"

