# Author: Liheng Chen
# Organization: ISCAS, China

cd ../../arachne-all/CoreArbiter/||exit
make -j"$(nproc)" -s
./bin/coreArbiterServer
