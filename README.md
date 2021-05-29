# lyx-extractor
This project was created to allow the extraction of important parts of summaries of formats similar to mine.
## Requirements
Python 3
## Usage
* Put your wanted `.lyx` summary file (that **must** be of the supported format - contact me for more details) in the same folder as `lyx_finder.py`  and change its name to `raw.lyx`.
* Run `python lyx_finder.py <flag>` where *flag* is any combination of d (for definitions) and t (for theorems/corollaries/claims). Your output file will be named `new.lyx` and will be in the same directory as the `lyx_finder.py` file.