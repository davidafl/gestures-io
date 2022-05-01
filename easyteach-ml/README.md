# useful information

##installing
1. create a python virtual environment (venv)
2. open terminal and execute: venv/Scripts/activate
3. execute: pip install -f requirements.txt

## running
1. open terminal and "venv/Scripts/activate"
2. execute: python ui.py

## teaching a new gesture
1. edit the file model\keypoint_classifier\keypoint_classifier_label.csv\
   1. add the new label of the gesture at the end
   2. becareful not to add an extra empty line
   3. remember the index of the new gesture 
2. line 3 of keypoint_classification.ipynb: put the index+1 (number of total gestures)
3. open terminal and execute: venv/Scripts/activate
4. execute: python app.main
5. type "?" and the index of the new gesture (type continuous for at leasta minute to have 500-1500 images)
6. type ESC to exit the program