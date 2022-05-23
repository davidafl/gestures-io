# useful information

##installing
1. create a python virtual environment (venv)
2. open terminal and execute: venv/Scripts/activate
3. execute: pip install -r requirements.txt

## running
1. open terminal and "venv/Scripts/activate"
2. execute: python ui.py

## teaching a new gesture
1. edit the file model\keypoint_classifier\keypoint_classifier_label.csv
   1. add the new label of the gesture at the end
   2. becareful not to add an extra empty line
   3. remember the index of the new gesture 
2. line 30 of keypoint_classification.py: put the index+1 (number of total gestures)
3. open terminal and execute: venv/Scripts/activate
4. execute: python app.py
5. type "k" , then the index of the new gesture. Then type continuously the digit for at least a minute to have 500-1500 images.
6. type ESC to exit the program

## how to create a venv manually
1. open terminal in project
2. check python version (must be >= 3)
3. type:
   1. py -m pip install --upgrade pip
   2. py -m pip install --user virtualenv
   3. py -m venv env
   4. then for any command always make sure to execute: .\env\Scripts\activate
   
## links
1. https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#installing-virtualenv
2. 
