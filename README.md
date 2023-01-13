# CDRIPER

Easy to use CD ripper written in python using [FFMPEG](https://ffmpeg.org/)

## USAGE

cdriper by default will try to convert all tracks on the CD located at `/dev/cdrom`

### ARGUMENTS

1. -cd  Specify cdrom to use, use: `-cd <path>` 
    - Example: `-cd D:`
2. -"number"    Specify track number, use: `-1:2...`
    - Example `-2:5:10`
3. -format,f  Selects the format of output file, default is wav
    - Example `-format mp3`
4. -output,o  Specify output folder, use: `-output <path>` It's important to add `/` or `\` after the folder path
    - Example `-output /some/folder/`
5. -help    Displays help