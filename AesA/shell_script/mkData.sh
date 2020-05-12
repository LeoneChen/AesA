# Author: Liheng Chen
# Organization: ISCAS, China

cd ../python_script || exit

mkdir -p ../data

python3 mkData.py 100m
python3 truncateData.py 100m 100b
python3 truncateData.py 100m 1k
python3 truncateData.py 100m 10k
python3 truncateData.py 100m 100k
python3 truncateData.py 100m 1m
python3 truncateData.py 100m 10m
