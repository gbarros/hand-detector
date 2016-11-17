opencv_traincascade -data haar -vec "../images/LetraV/merged_V.vec" -bg bg.txt -numPos 430 -numNeg 2006 -numStages 20 -featureType HAAR -w 40 -h 40 -precalcIdxBufSize 15360 -precalcValBufSize 15360 -mode ALL

