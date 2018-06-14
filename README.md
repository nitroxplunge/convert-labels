# convert-labels

## Dependencies:

### Python 2.7

PIL

`pip install pillow`


## Usage

NOTE:
Dataset must be in format of a dataset directory with all the images, and a labels folder inside the dataset directory with all the labels.

`cd convert-labels.py`

`python convert-labels.py ../your/dataset/directory`


Add optional arguments:

`python convert-labels.py ../your/dataset/directory -r -v`


`-r` - Replace the existing label files

`-v` - Print actions
