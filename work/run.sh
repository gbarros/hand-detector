opencv_traincascade -data haar2 -vec "../images/LetraA/merged_A.vec" -bg ../images/background/bg1.txt -numPos 850 -numNeg 1034 -numStages 20 -featureType HAAR -w 40 -h 40 -precalcIdxBufSize 1024 -precalcValBufSize 1024 -mode ALL

