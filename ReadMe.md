A simple python script that makes an ETL job 
on json file and commits it to csv.

- the script reads json file from a directory.
- loads it and do smoe transformation.
- the script can take optional argument "-u" to maintain UNIX time format.
- then it saves the output dataframe ascsv.
