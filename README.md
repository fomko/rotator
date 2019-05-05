# Rotator 
Log rotate utility for log rotation.

## How to use?
 python rotator.py [path to config json with params]
 
 You can see params example config in `example_params.json`
 
### Params:
- Input(string) - Source folder or file 
- Output(string) - Folder where rotated files would be.
- RotatedFileSize(int, string) - File size for each rotated file. 
  Can be like 13GB(MB/KB) or pure integer 
- NeedToBeArchived (boolean) - Specify if rotated files need to be archived.


## ToDo:
- :black_square_button: Add tests on unittest
- :black_square_button: Add possibility to choose logging level in param config 
- :black_square_button: Add multiprocessing in writting process. Should be much faster!

