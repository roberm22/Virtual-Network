

#######################################################################################
######				    Orden destruir			 	 ######
#######################################################################################
###### 		  	   Para liberar el escenario, borrando    		 ######
###### 		  	       todos los ficheros creados. 	    		 ######
###### 		  		  MEJORA: Destruir solo una		 	 ######
#######################################################################################


def destruir(nombre):

	# Si no se introduce ningun parametro adicional destruiremos todas las maquinas
	# El numero de servidores esta guardado en el archivo pc1.cfg

	# el comando rm -f -> Forzado, ignora archivos no existentes y elimina cualquier aviso de confirmación.

	if len(sys.argv) == 2:    


		if os.path.exists("/mnt/tmp/pc1/pc1.cfg"):
			print("El archivo de configuracion esta creado")
		else:
			sys.exit("\033[1;31m" + "\n¡No has creado pc1.cfg!.\nAntes de la orden <destruir>, debe ir <crear>\n" + "\033[0;m")


		# Guardamos en la variable num_serv el numero de servidores que hay en el archivo pc1.cfg
		s = open("pc1.cfg", "r")
		num_serv = int(s.read())
		s.close()


		# Todo depende de cuanto valga num_serv

		# Si se puso un 0, solo existen las MV's c1 y lb
		if(num_serv >= 0):

			if os.system("sudo virsh dominfo lb > /dev/null 2>&1") ==0:	
				print("Destruyendo lb...") 
				os.system("sudo virsh destroy lb")
				os.system("sudo virsh undefine lb")

			if os.system("sudo virsh dominfo c1 > /dev/null 2>&1") ==0:
				print("Destruyendo c1...")
				os.system("sudo virsh destroy c1")
				os.system("sudo virsh undefine c1")


			os.system("rm lb.qcow2 -f")
			os.system("rm lb.xml -f")
			os.system("rm c1.qcow2 -f")
			os.system("rm c1.xml -f")


		# Si se puso un 1, ademas de las anteriores, esta s1
		if(num_serv >= 1):
			if os.system("sudo virsh dominfo s1 > /dev/null 2>&1") ==0:
				print("Destruyendo la maquina s1 ...")
				os.system("sudo virsh destroy s1")
				os.system("sudo virsh undefine s1")

			os.system("rm s1.qcow2 -f")
			os.system("rm s1.xml -f")

		# Si se puso un 2, ademas de las anteriores, esta s2
		if(num_serv >= 2):
			if os.system("sudo virsh dominfo s2 > /dev/null 2>&1") ==0:
				print("Destruyendo la maquina s2 ...")
				os.system("sudo virsh undefine s2")
				os.system("sudo virsh destroy s2")
			
			os.system("rm s2.qcow2 -f")
			os.system("rm s2.xml -f")

		# Si se puso un 3, ademas de las anteriores, esta s3
		if(num_serv >= 3):
			if os.system("sudo virsh dominfo s3 > /dev/null 2>&1") ==0:
				print("Destruyendo la maquina s3 ...")
				os.system("sudo virsh destroy s3")
				os.system("sudo virsh undefine s3")

			os.system("rm s3.qcow2 -f")
			os.system("rm s3.xml -f")

		# Si se puso un 4, ademas de las anteriores, esta s4
		if(num_serv >= 4):
			if os.system("sudo virsh dominfo s4 > /dev/null 2>&1") ==0:
				print("Destruyendo la maquina s4 ...")
				os.system("sudo virsh destroy s4")
				os.system("sudo virsh undefine s4")

			os.system("rm s4.qcow2 -f")
			os.system("rm s4.xml -f")

		# Si se puso un 5, ademas de las anteriores, esta s5
		if(num_serv >= 5):
			if os.system("sudo virsh dominfo s5 > /dev/null 2>&1") ==0:
				print("Destruyendo la maquina s5 ...")
				os.system("sudo virsh destroy s5")
				os.system("sudo virsh undefine s5")
				print("Destruidas todas las MV's ...")

			os.system("rm s5.qcow2 -f")
			os.system("rm s5.xml -f")


		# Una vez hecho esto, tambien es necesario eliminar los ficheros de configuracion

		os.system("sudo ifconfig LAN1 down")
		os.system("sudo ifconfig LAN2 down")
		os.system("sudo brctl delbr LAN1")
		os.system("sudo brctl delbr LAN2")

		os.system("rm pc1.cfg -f")
		os.system("rm hostname -f")
		os.system("rm interfaces -f")
		os.system("rm cdps-vm-base-pc1.qcow2 -f")
		os.system("rm plantilla-vm-pc1.xml -f")

	
	#### MEJORA: en caso de que se ponga un parametro adicional junto a destruir, se destruira la maquina indicada. ####
	
	if len(sys.argv) == 3:
		
		if(nombre == "c1" or nombre == "lb" or nombre == "s1" or nombre == "s2" or nombre == "s3" or nombre == "s4" or nombre == "s5"):
			if os.system("sudo virsh dominfo "+str(nombre)+" > /dev/null 2>&1") ==0:
				os.system("sudo virsh destroy " + str(nombre))
				os.system("sudo virsh undefine " + str(nombre))
				os.system("rm " + str(nombre) +".qcow2 -f")
				os.system("rm " + str(nombre) +".xml -f")
			else:
				print("\033[1;31m" + "\nLa maquina "+ str(nombre)+" no esta definida\n" + "\033[0;m")

		else:

			sys.exit("\033[1;31m" + "\nEl parametro debe ser el nombre de una MV\n" + "\033[0;m")


