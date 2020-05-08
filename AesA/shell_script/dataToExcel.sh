cd ../python_script || exit
python3 getAvg.py ArachneEnable
python3 getAvg.py PthreadSiblingCore
python3 getAvg.py PthreadDiffCore
python3 dataToExcel.py
