import ffmpeg
import sys

cdName = "/dev/cdrom"
format = 'wav'
tracks = []
outputFolder = ''
ffmpegFolder='./ffmpeg/'

help = """Arguments:
-cd         Specify cdrom to use, use: -cd <path>
-"number"   Specify track number, use: -1:2...
-format     Selects the format of output file, default is wav
-output		Specify output folder, use: -output <path>
-h,?        Displays help"""


def numberGrab(arg):  # separates track numbers
    looping = True
    while looping:
        length = len(arg)
        x = arg.rfind(":")  # searches for the : dividing the numbers
        if (x != -1):
            trackNum = arg[x+1:length]
            # grabs the last number and removes it from the string
            arg = arg[:x]
        else:
            trackNum = arg[1:length]
            looping = False
        if (trackNum.isnumeric()):
            if (int(trackNum) not in tracks):
                tracks.append(int(trackNum))
        else:
            print("'%s' is not a track number" % trackNum)
            sys.exit(1)


args = sys.argv

if (len(args) > 1):  # checks arguments
    args.pop(0)
    for arg in args:
        if (arg.find("-") == -1 or len(arg) < 2):
            print("Invalid argument '%s'" % arg)
            sys.exit(1)

        if (arg == '-cd'):
            index = args.index(arg)
            cdName = args[index+1]
            # after grabbing the argument it pops it to save time and code
            args.pop(index+1)

        elif (arg[1].isnumeric()):
            numberGrab(arg)

        elif (arg in ["-format", "-f"]):
            index = args.index(arg)
            format = args[index+1]
            args.pop(index+1)

        elif (arg  in ["-output", "-o"]):
            index = args.index(arg)
            outputFolder = args[index+1]
            args.pop(index+1)

        elif (arg in ["-?", "-h", '-help']):
            print(help)
            sys.exit(1)

        else:
            print("Invalid argument '%s'\n" % arg)
            print(help)
            sys.exit(1)

print("Reading CD")  # informs the user

try:
    cd_info_raw = ffmpeg.probe(
        cdName, cmd=ffmpegFolder+'ffprobe',f='libcdio', print_format='json', show_chapters=None)  # reads json from the CD
except ffmpeg.Error as e:
    print(str(e.stderr), file=sys.stderr)
    sys.exit(1)

toConvert = []
if (len(tracks) > 0):  # checks the tracks to convert and if they even exist
    for track in tracks:
        if (track > len(cd_info_raw["chapters"])):
            print("'%d' is not a valid track number" % track)
            sys.exit(1)
        toConvert.append(cd_info_raw["chapters"][track-1])

else:
    toConvert = cd_info_raw["chapters"]

print("Starting to rip")
for track in toConvert:
    trackIn = ffmpeg.input(cdName, f='libcdio',
                           ss=track["start_time"], to=track["end_time"])
    if (format == 'mp3'):
        trackOut = ffmpeg.output(
            trackIn, outputFolder+track["tags"]["title"]+"."+format, audio_bitrate="325k")  # makes 320kbps mp3
    else:
        trackOut = ffmpeg.output(trackIn, outputFolder+track["tags"]["title"]+"."+format)
    print("Ripping %s..." % track["tags"]["title"])
    try:
        ffmpeg.run(trackOut, cmd=ffmpegFolder+'ffmpeg', quiet=True, overwrite_output=True)  # rips
    except ffmpeg.Error as e:
        print(str(e.stderr), file=sys.stderr)
        sys.exit(1)
    print("Ripped successfully")