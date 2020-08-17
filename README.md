# opencv__feature_matching

## Goal 
- for a input photo, find the closest one  
- match features in one image with others

## Libraries 
- opencv
- Brute-Force Matching with ORB Descriptors (https://docs.opencv.org/master/dc/dc3/tutorial_py_matcher.html)
- google vision api (https://cloud.google.com/vision/docs/)


<img width="445" src="https://user-images.githubusercontent.com/39558070/90326794-a2bcf580-dfc7-11ea-9b34-13fe1de6133d.png">
<br>
<img width="891" src="https://user-images.githubusercontent.com/39558070/90326856-8b323c80-dfc8-11ea-8917-ef41ae737cb6.png">
<br>
<img width="495" src="https://user-images.githubusercontent.com/39558070/90326871-b7e65400-dfc8-11ea-8ae2-bcfd529b1b14.png">
<br>


## How to use
usage example

python ./get_rank.py [input_image] [db_directory] [output_file] <br>
ex) python ./get_rank.py /Users/kim-yeseul/Documents/user_lv/네버풀_모노그램.jpeg /Users/kim-yeseul/Documents/lv /Users/kim-yeseul/Documents/out_files/네버풀_모노그램.txt  
<br>
./get_ranks.pl [input_directory] [db_directory] [output_directory] <br>
ex) get_ranks.pl  /Users/kim-yeseul/Documents/user_lv /Users/kim-yeseul/Documents/lv /Users/kim-yeseul/Documents/result
<br>
<br>
[<< alma 제품에 대한 결과 output파일 >>](https://github.com/admirebg/opencv__feature_matching/files/5080009/Alma.txt)
