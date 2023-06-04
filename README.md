# Clustering_DBSCAN

## Run
> .../Clustering_DBSCAN> python clustering.py (input data) (# of clusters) (Eps) (MinPts)
```
python clustering.py input3.txt 4 5 5
```
Execute the program with four arguments: **input data file name, n, Eps and MinPts**  

### recommended values for parameter (n, eps, MinPts)
- (input 1) n=8, Eps=15, MinPts=22
- (input 2) n=5, Eps=2, MinPts=7
- (input 3) n=4, Eps=5, MinPts=5


## Test
❗Before testing, place the files generated while running clustering.py in the /test directory

```
PA3.exe input1
```
>.../Clustering_DBSCAN/test> PA3.exe (input data)  


### proper test result
- input1 : around 99
- input2 : around 95
- input3 : around 99

test result with /output_files
- input1 : around 99.77579
- input2 : around 94.08309
- input3 : around 100


## File format for an input data   
 [object_id_1]\t[x_coordinate]\t[y_coordinate]\n   
 [object_id_2]\t[x_coordinate]\t[y_coordinate]\n   
 [object_id_3]\t[x_coordinate]\t[y_coordinate]\n   
 [object_id_4]\t[x_coordinate]\t[y_coordinate]\n   
 ...
