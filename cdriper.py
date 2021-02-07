import sys, os
import subprocess
import pycdio, cdio


cdName = '/dev/cdrom' #variable para localizacion de cdrom default: /dev/cdrom
format = 'wav' #variable para formato de salida default: wav
isTrackNum = False  #variable para checkear si se aclaro un numero de track
faso_array = [] #array para guardar los diferentes tracks


help = """ Parameters: 
-cd 		changes what cdrom cdriper uses. eg: -cd /dev/cdrom 
-"num" 		selects a single track from the cd. eg: -2 (only converts second track)
-open 		opens cdrom
-format 	selects the output file format default: wav. eg: -format flac
-h 			displays help.
-? 			displays help.""" #string con toda la info de ayuda

d = cdio.Device(cdName) #Variable usada luego para abrir el cd

faso = str(sys.argv) #se chequea si hay argumentos
argument = faso.find('-') #se busca - para señalizar un comando


if argument != -1: #si hay un argumentos

	faso = faso[argument:]
	firstLine = faso.find("-")
	secondLine = faso.rfind("-")
	
	while True: #se comienza un loop para checkear argumentos 

		firstLine = faso.find("-")
		secondLine = faso.rfind("-") # se checkea si hay mas de 1 argumento

		x = faso.find("-")
		faso = faso[x+1:]
		x = faso.find("'")
		faso2 = faso[:x] #separa el argumento y lo pasa a faso2
			

#checkeo de argumentos
#-----------------------------------------------------------------------------------------------------------------------------------------
		

		if faso2 == "open": #checkea si dice open
			d.eject_media_drive()
			exit()

		elif faso2 == 'cd': #checkea si dice cd
			x = faso.find(",")
			cdName = faso[x+3:]
			x = cdName.find("'")
			cdName = cdName[:x] #se aisla en nombre del cd-rom

		elif faso2 == 'format': #se checkea si dice format
			x = faso.find(",")
			format = faso[x+3:]
			x = format.find("'")
			format = format[:x] #se aisla el formato

		elif faso2 == 'h' or faso2 == '?':
			print(help) #si la palabra es h o ? se imprime la ayuda
			exit()

		while True: #se comienza otro loop

			fasofind = faso2.find(":")
			x = faso2.rfind(":")
			j = len(faso2)
			faso_int = (faso2[x+1:j]) #se busca y se aisla cada valor de track ingresado

			isTrackNum = faso_int.isnumeric() #se checkea que lo ingresado sea un valor de track
			if isTrackNum == True:

				faso_array.append(int(faso_int)) #se pone el valor de track en una array
				faso2 = faso2[:x]

			if fasofind == -1: #en caso de no encontrarse : se rompe el loop, esto se hace asi para que el usuario tambien pueda ingresar un solo numero de track
				break 
			

		else: #si no dice ninguna de las anteriores dice invalid argument
			print("Invalid Argument:", faso2)
			exit()		
		
		if firstLine == secondLine: #si solo queda un argumento se rompe el loop
			break

#------------------------------------------------------------------------------------------------------------------------------------------

#Conversion
#------------------------------------------------------------------------------------------------------------------------------------------
command = "ffprobe -f libcdio -i " + cdName + " -print_format json -show_chapters -loglevel error" #se corre ffprobe para conseguir la informacion del cd

subprocess = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE) #se lee la salida del comento	
cd_info = subprocess.stdout.read()
cd_info_str = str(cd_info) #se guarda la salida del comando en un string

i=cd_info_str
j=cd_info_str.find("start_time") #se busca en la info del cd el comienzo del primer track
while(j > 0): #loopea mientras encuentre tracks

	j=i.find("start_time") 
	if j != -1:
		j=i.find("start_time")
		i = i[j+14:]
		x = i.find('"') 
		start_time = i[:x] #se aisla el tiempo de comienzo
		j=i.find("end_time") #se busca el tiempo final
		i = i[j+12:]
		x = i.find('"')
		end_time = i[:x] #se aisla el tiempo final
		j=i.find("title") #se busca el titulo del track (track X)
		i = i[j+9:]
		x = i.find('"')
		name = i[:x] #se aisla en nombre
		if argument != -1: #si un argumento fue pesto
			if isTrackNum == True: #se checkea si el argumento son tracks
				j=name.find(" ")
				trackNum = name[j+1:]
				x = trackNum.find('') #se encuentra el numero de track dentro de la info del cd
				if trackNum.isnumeric() == True:
					trackNum = int(trackNum) #se checke y aisla el numero del track del nombre 
					if trackNum in faso_array: #si el numero del track esta en la array de tracks del usuario se convierte
						convert = 'ffmpeg -f libcdio -ss '+start_time+' -to '+end_time+' -i '+cdName+' "'+name+'.'+format+'"'
						os.system(convert)
			else: #en caso de que no haya argumento se convierten todos los tracks
				convert = 'ffmpeg -f libcdio -ss '+start_time+' -to '+end_time+' -i '+cdName+' "'+name+'.'+format+'"'
				os.system(convert)
#------------------------------------------------------------------------------------------------------------------------------------------