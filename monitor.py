

#######################################################################################
######				    Orden monitor			 	 ######
#######################################################################################
###### 		  	 	  Presente el estado de todas     		 ######
###### 		  	       las maquinas del escenario 	    		 ######
###### 		  			  MEJORA			 	 ######
#######################################################################################


def monitor(nombre):
	if len(sys.argv) == 3:
		
		if(nombre == "c1" or nombre == "lb" or nombre == "s1" or nombre == "s2" or nombre == "s3" or nombre == "s4" or nombre == "s5"):

			if os.system("sudo virsh dominfo " + str(nombre)+ " > /dev/null 2>&1") ==0:
				print("\033[1;34m" + "\nInformacion basica del dominio " + str(nombre) + "\n" +'\033[0;m')		
				os.system("sudo virsh dominfo " + str(nombre))
				print("\033[1;34m" + "\nEstado del dominio " + str(nombre) + "\n" +'\033[0;m')		
				os.system("sudo virsh domstate " + str(nombre))
				print("\033[1;34m" + "\nEstado de la CPU del dominio " + str(nombre) + "\n" +'\033[0;m')		
				os.system("sudo virsh cpu-stats " + str(nombre))
			else:
				print("\033[1;31m" + "\nEl dominio no esta definido. Se requiere arrancar " + str(nombre) + " previamente\n" +'\033[0;m')
			
	else:
		sys.exit("\033[1;31m" + "\nEjecucion incorrecta. Es obligatorio el siguiente formato: pc1 monitor <nombre MV>\n" +'\033[0;m')
