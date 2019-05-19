# Rotator 
Log rotate utility for log rotation.

## Prerequisites 
-  Python 3.7 + 

## How to use?
 `python main.py -c [path to config json with params]`
```
Arguments:
  -c , --config         Path to json with params
  -l , --logginglevel   Logging Level. Can be
                        DEBUG/INFO/WARNING/ERROR/CRITICAL
``` 
 You can see params example config in `example_params.json`
 
### Params in config file:
- Input(string) - Source folder or file. Mind that Windows path requires double slash  `C://like//this`
- Output(string) - Folder where rotated files would be.
- RotatedFileSize(int, string) - File size for each rotated file. 
  Can be like 13GB(MB/KB) or a pure integer 
- NeedToBeArchived (boolean) - Specify if rotated files need to be archived.  By default False


## ToDo:
- :black_square_button: Make logs more informative!
- :black_square_button: Add tests with unittest or pytest lib
- :black_square_button: Add possibility to choose logging level in param config 
- :black_square_button: Add multiprocessing in writing process. Should be much faster!

