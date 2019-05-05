# Rotator 
Log rotate utility for log rotation.

## How to use?
 python rotator.py [path to json with params]
 
 You can see json with params example in `example_params.json`
 
### Params:
- Input(string) - Source folder or file 
- Output(string) - Folder where rotated files would be.
- RotatedFileSize(int, string) - File size for each rotated file. 
  Can be like 13GB(MB/KB) or pure integer 
- NeedToBeArchived (boolean) - Specify if rotated files need to be archived.

