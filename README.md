# CDRIPER

Easy to use CD ripper written in python using [FFMPEG](https://ffmpeg.org/)

## USAGE

cdriper by default will try to convert all tracks on the CD located at `/dev/cdrom`

### ARGUMENTS

1. -cd  Specify cdrom to use, use: `-cd <path>` 
    - Example: `-cd D:`
2. -"number"    Specify track number, use: `-1:2...`
    - Example `-2:5:10`
3. -format  Selects the format of output file, default is wav
    - Example `-format mp3`
4. -help    Displays help