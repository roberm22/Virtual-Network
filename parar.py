

#######################################################################################
######				    Orden parar				 	 ######
#######################################################################################
###### 		  	  Para parar las máquinas virtuales    		 	 ######
###### 		  		  MEJORA: Parar solo una    		 	 ######
#######################################################################################



def parar(nombre):
	
	# Si no se introduce ningun parametro adicional pararemos todas las maquinas
	# El numero de servidores esta guardado en el archivo pc1.cfg

	if len(sys.argv) == 2:


		if os.path.exists("/mnt/tmp/pc1/pc1.cfg"):
			print("El archivo de configuracion esta creado")
		else:
			sys.exit("\033[1;31m" + "\n¡No has creado pc1.cfg!.\nAntes de la orden <parar>, debe ir <crear>\n" + "\033[0;m")
		

		# Guardamos en la variable num_serv el numero de servidores que hay en el archivo pc1.cfg
		s = open("pc1.cfg", "r")
		num_serv = int(s.read())
		s.close()

		# Todo depende de cuanto valga num_serv

		# Si se puso un 0, solo estan arrancadas las MV's c1 y lb
		if(num_serv >= 0):
			if os.system("sudo virsh dominfo lb > /dev/null 2>&1") ==0:
				os.system("sudo virsh shutdown lb")
				print("Parando lb")
			if os.system("sudo virsh dominfo c1 > /dev/null 2>&1") ==0:	
				os.system("sudo virsh shutdown c1")
				print("Parando c1")


		# Si se puso un 1, ademas de las anteriores, esta s1
		if(num_serv >= 1):
			if os.system("sudo virsh dominfo s1 > /dev/null 2>&1") ==0:
				os.system("sudo virsh shutdown s1")
				print("Parando la maquina s1 ...")

		# Si se puso un 2, ademas de las anteriores, esta s2
		if(num_serv >= 2):
			if os.system("sudo virsh dominfo s2 > /dev/null 2>&1") ==0:
				os.system("sudo virsh shutdown s2")
				print("Parando la maquina s2 ...")

		# Si se puso un 3, ademas de las anteriores, esta s3
		if(num_serv >= 3):
			if os.system("sudo virsh dominfo s3 > /dev/null 2>&1") ==0:
				os.system("sudo virsh shutdown s3")
				print("Parando la maquina s3 ...")

		# Si se puso un 4, ademas de las anteriores, esta s4
		if(num_serv >= 4):
			if os.system("sudo virsh dominfo s4 > /dev/null 2>&1") ==0:
				os.system("sudo virsh shutdown s4")
				print("Parando la maquina s4 ...")

		# Si se puso un 5, ademas de las anteriores, esta s5
		if(num_serv >= 5):
			if os.system("sudo virsh dominfo s5 > /dev/null 2>&1") ==0:
				os.system("sudo virsh shutdown s5")
				print("Parando la maquina s5 ...")
				print("Paradas todas las MV's ...")


	
	#### MEJORA: en caso de que se ponga un parametro adicional junto a parar, se parara la maquina indicada. ####
	
	if len(sys.argv) == 3:
		
		if(nombre == "c1" or nombre == "lb" or nombre == "s1" or nombre == "s2" or nombre == "s3" or nombre == "s4" or nombre == "s5"):
			if os.system("sudo virsh dominfo " + str(nombre) + " > /dev/null 2>&1") ==0:
				os.system("sudo virsh shutdown " + str(nombre))
				print("\033[1;34m" + "Parando la maquina " + str(nombre) + "..." + "\033[0;m")
			else:
				print("\033[1;31m" + "\nLa maquina " + str(nombre) + " no esta definida\n" + "\033[0;m")

				
		else:
			sys.exit("\033[1;31m" + "\nEl parametro debe ser el nombre de una MV\n" + "\033[0;m")
