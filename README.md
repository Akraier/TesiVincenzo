## Settings

The `main_path` variable in the config file `<projectPath>/utils/config.py` needs to be set with the base directory of the project.

## Setup environment
Install `virtualenv`
```
sudo apt install python3-virtualenv
```
### Create the environment

Create the virtual environment
```
virtualenv venv
```
Activate the virtual environment
```
source venv/bin/activate
```
Install the required libraries listed in `requirements.txt`
```
pip install -r requirements.txt
```
### Test the environment
Install the required libraries listed in `requirements.txt`
```
python main.py -m BASIC -d DATASETS/dataset1_PREPROCESSED/ -i 50x1 -e 3
```
Check the input parameters with
```
 python main.py --help
```
