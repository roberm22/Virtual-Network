

#######################################################################################
######				    Orden arrancar			 	 ######
#######################################################################################
###### 		  	  Para arrancar las máquinas virtuales    		 ######
######   			 y mostrar su consola.    			 ######
######   			 MEJORA: Arrancar solo una    			 ###### 
#######################################################################################



def arrancar(nombre):


	# Si no se introduce ningun parametro adicional arrancaremos todas las maquinas
	# El numero de servidores esta guardado en el archivo pc1.cfg

	if len(sys.argv) == 2:

		if os.path.exists("/mnt/tmp/pc1/pc1.cfg"):
			print("El archivo de configuracion esta creado")
		else:
			sys.exit("\033[1;31m" + "\n¡No has creado pc1.cfg!.\nAntes de la orden <arrancar>, debe ir <crear>\n" + "\033[0;m")
		

		print ("\nLas maquinas lb y c1 se estan arrancando...\n")

		# Guardamos en la variable num_serv el numero de servidores que hay en el archivo pc1.cfg
		s = open("pc1.cfg", "r")
		num_serv = int(s.read())
		s.close()


		# Arrancamos el gestor de máquinas virtuales para monitorizar su arranque
		os.system("HOME=/mnt/tmp sudo virt-manager")

		# Arrancamos lb y c1 (las maquinas minimas necesarias) utilizando el comando virsh


		################### Configuracion de lb ########################
		if os.system("sudo virsh dominfo lb > /dev/null 2>&1") !=0:
			os.system("sudo virsh define lb.xml")

		# Creamos el fichero de configuarion hostname en el que ponemos el nombre de la MV lb
		# Hacemos uso del mismo comando que para crear el fichero pc1.cfg
		os.system("touch /mnt/tmp/pc1/hostname")
		os.system("echo lb > /mnt/tmp/pc1/hostname")


		# Copiamos el fichero hostname en el directorio /etc de lb
		# Dice el enunciado que se puede sobrescribir sin problema
		os.system("sudo virt-copy-in -a lb.qcow2 /mnt/tmp/pc1/hostname /etc")
		

		# Creamos el fichero interfaces
		os.system("touch /mnt/tmp/pc1/interfaces")

		# Escribimos en el fichero interfaces para introducir las interfaces correspondientes de nuestra red para lb
		n = open('/mnt/tmp/pc1/interfaces',"w") 	    
		n.write("auto lo\niface lo inet loopback\n\nauto eth0\niface eth0 inet static\naddress 10.0.1.1\nnetmask 255.255.255.0\ngateway 10.0.1.2\n\nauto eth1\niface eth1 inet static\naddress 10.0.2.1\nnetmask 255.255.255.0\ngateway 10.0.2.0\n")      		
		n.close()

		# Copiamos el fichero interfaces en el directorio /etc/network de lb
		os.system("sudo virt-copy-in -a lb.qcow2 /mnt/tmp/pc1/interfaces /etc/network")

		# Edicion del fichero /etc/sysctl.conf para configurar el balanceador como router
		os.system("sudo virt-edit -a lb.qcow2 /etc/sysctl.conf -e 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/'")

		# -e: Instead of launching the external editor, non-interactively apply the Perl expression EXPR 
		# (lo que esta entre ') to each line in the file.
		# For example to replace all instances of foo with bar in a file: 's/foo/bar/'
		# Entonces teniendo en cuenta que en el archivo sysctl.conf pone: 
		# Uncomment the next line to enable packet forwarding for IPv4
		# #net.ipv4.ip_forward=1
		# Todo lo que tenemos que hacer es descomentarla, mismo procedimiento que foo y bar.



		os.system("sudo virsh start lb")



		################### Configuracion de c1 ########################

		if os.system("sudo virsh dominfo c1 > /dev/null 2>&1") !=0:
			os.system("sudo virsh define c1.xml")

		# Definimos el nombre de la maquina virtual c1
		os.system("echo c1 > /mnt/tmp/pc1/hostname")

		# Copiamos el fichero hostname en el directorio /etc de c1
		os.system("sudo virt-copy-in -a c1.qcow2 /mnt/tmp/pc1/hostname /etc")

		
		# Reescribimos interfaces para introducir las interfaces de c1
		n = open('/mnt/tmp/pc1/interfaces',"w") 	    
		n.write("auto lo\niface lo inet loopback\n\nauto eth0\niface eth0 inet static\naddress 10.0.1.2\nnetmask 255.255.255.0\ngateway 10.0.1.1\n")      		
		n.close()
		# Copiamos el fichero interfaces en el directorio /etc/network de c1
		os.system("sudo virt-copy-in -a c1.qcow2 /mnt/tmp/pc1/interfaces /etc/network")

		os.system("sudo virsh start c1")



		# Arrancar un nuevo terminal (consola textual) para cada una. 
		# (Comando sacado de la practica 3, es mejor que el que se da en el enunciado de pc1)

		os.system("xterm -rv -sb -rightbar -fa monospace -fs 10 -title 'lb' -e 'sudo virsh console lb' &")
		os.system("xterm -rv -sb -rightbar -fa monospace -fs 10 -title 'c1' -e 'sudo virsh console c1' &")

		print ("\nLas maquinas lb y c1 se han arrancado con exito\n")

		################################################################
		##############      Arrancar servidores	      ##################
		################################################################


		if ((num_serv >= 1) and (num_serv <= 5)):
			

			print ("\nArrancando servidores...\n")
		

		################### Configuracion de s1 ########################
			
			if os.system("sudo virsh dominfo s1 > /dev/null 2>&1") !=0:
				os.system("sudo virsh define s1.xml")

			# Definimos el nombre de la maquina virtual s1
			os.system("echo s1 > /mnt/tmp/pc1/hostname")

			# Copiamos el fichero hostname en el directorio /etc de nuestra maquina para actualizar el fichero hostname de esta
			os.system("sudo virt-copy-in -a s1.qcow2 /mnt/tmp/pc1/hostname /etc")


			# Reescribimos el fichero interfaces para introducir las interfaces de s1
			n = open('/mnt/tmp/pc1/interfaces',"w") 	    
			n.write("auto lo\niface lo inet loopback\n\nauto eth0\niface eth0 inet static\naddress 10.0.2.11\nnetmask 255.255.255.0\ngateway 10.0.2.1\n")      		
			n.close()

			# Copiamos el fichero interfaces en el directorio /etc/network de s1
			os.system("sudo virt-copy-in -a s1.qcow2 /mnt/tmp/pc1/interfaces /etc/network")


			os.system("sudo virsh start s1")
			os.system("xterm -rv -sb -rightbar -fa monospace -fs 10 -title 's1' -e 'sudo virsh console s1' &")

			print("\nMaquina S1 arrancada con exito\n")
			



			# Si el valor introducido es superior a 1 arrancaremos s2
			if(num_serv >= 2):


				################### Configuracion de s2 ########################

				if os.system("sudo virsh dominfo s2 > /dev/null 2>&1") !=0:
					os.system("sudo virsh define s2.xml")

				# Definimos el nombre de la maquina virtual s2
				os.system("echo s2 > /mnt/tmp/pc1/hostname")

				# Copiamos el fichero hostname en el directorio /etc de s2
				os.system("sudo virt-copy-in -a s2.qcow2 /mnt/tmp/pc1/hostname /etc")


				# Reescribimos el fichero interfaces para introducir las interfaces de s2
				n = open("/mnt/tmp/pc1/interfaces","w") 	    
				n.write("auto lo\niface lo inet loopback\n\nauto eth0\niface eth0 inet static\naddress 10.0.2.12\nnetmask 255.255.255.0\ngateway 10.0.2.1\n")      		
				n.close()

				# Copiamos el fichero interfaces en el directorio /etc/network de s2
				os.system("sudo virt-copy-in -a s2.qcow2 /mnt/tmp/pc1/interfaces /etc/network")


				os.system("sudo virsh start s2")
				os.system("xterm -rv -sb -rightbar -fa monospace -fs 10 -title 's2' -e 'sudo virsh console s2' &")

				print("\nMaquina S2 arrancada con exito\n")



			# Si el valor introducido es superior a 2 arrancaremos s3
			if(num_serv >= 3):


				################### Configuracion de s3 ########################

				if os.system("sudo virsh dominfo s3 > /dev/null 2>&1") !=0:
					os.system("sudo virsh define s3.xml")

				# Definimos el nombre de la maquina virtual s3
				os.system("echo s3 > /mnt/tmp/pc1/hostname")

				# Copiamos el fichero hostname en el directorio /etc de s3
				os.system("sudo virt-copy-in -a s3.qcow2 /mnt/tmp/pc1/hostname /etc")


				# Reescribimos el fichero interfaces para introducir las interfaces de s3
				n = open('/mnt/tmp/pc1/interfaces',"w") 	    
				n.write("auto lo\niface lo inet loopback\n\nauto eth0\niface eth0 inet static\naddress 10.0.2.13\nnetmask 255.255.255.0\ngateway 10.0.2.1\n")      		
				n.close()

				# Copiamos el fichero interfaces en el directorio /etc/network de s3
				os.system("sudo virt-copy-in -a s3.qcow2 /mnt/tmp/pc1/interfaces /etc/network")


				os.system("sudo virsh start s3")
				os.system("xterm -rv -sb -rightbar -fa monospace -fs 10 -title 's3' -e 'sudo virsh console s3' &")

				print("\nMaquina S3 arrancada con exito\n")



			# Si el valor introducido es superior a 3 arrancaremos s4
			if(num_serv >= 4):


				################### Configuracion de s4 ########################

				if os.system("sudo virsh dominfo s4 > /dev/null 2>&1") !=0:
					os.system("sudo virsh define s4.xml")

				# Definimos el nombre de la maquina virtual s4
				os.system("echo s4 > /mnt/tmp/pc1/hostname")

				# Copiamos el fichero hostname en el directorio /etc de s4
				os.system("sudo virt-copy-in -a s4.qcow2 /mnt/tmp/pc1/hostname /etc")


				# Reescribimos el fichero interfaces para introducir las interfaces de s4
				n = open('/mnt/tmp/pc1/interfaces',"w") 	    
				n.write("auto lo\niface lo inet loopback\n\nauto eth0\niface eth0 inet static\naddress 10.0.2.14\nnetmask 255.255.255.0\ngateway 10.0.2.1\n")      		
				n.close()

				# Copiamos el fichero interfaces en el directorio /etc/network de s4
				os.system("sudo virt-copy-in -a s4.qcow2 /mnt/tmp/pc1/interfaces /etc/network")


				os.system("sudo virsh start s4")
				os.system("xterm -rv -sb -rightbar -fa monospace -fs 10 -title 's4' -e 'sudo virsh console s4' &")

				print("\nMaquina S4 arrancada con exito\n")




			# Si el valor introducido es superior a 4 arrancaremos s5
			if(num_serv == 5):

				################### Configuracion de s5 ########################

				if os.system("sudo virsh dominfo s5 > /dev/null 2>&1") !=0:
					os.system("sudo virsh define s5.xml")

				# Definimos el nombre de la maquina virtual s5
				os.system("echo s5 > /mnt/tmp/pc1/hostname")

				# Copiamos el fichero hostname en el directorio /etc de s5
				os.system("sudo virt-copy-in -a s5.qcow2 /mnt/tmp/pc1/hostname /etc")


				# Reescribimos el fichero interfaces para introducir las interfaces de s5
				n = open('/mnt/tmp/pc1/interfaces',"w") 	    
				n.write("auto lo\niface lo inet loopback\n\nauto eth0\niface eth0 inet static\naddress 10.0.2.15\nnetmask 255.255.255.0\ngateway 10.0.2.1\n")      		
				n.close()

				# Copiamos el fichero interfaces en el directorio /etc/network de s5
				os.system("sudo virt-copy-in -a s5.qcow2 /mnt/tmp/pc1/interfaces /etc/network")



				os.system("sudo virsh start s5")
				os.system("xterm -rv -sb -rightbar -fa monospace -fs 10 -title 's5' -e 'sudo virsh console s5' &")

				print("\nMaquina S5 arrancada con exito\n")
				print("\nTodas las maquinas arrancadas con exito\n")


		else:
			print("\033[1;31m" + "NO ES VALIDO EL PARAMETRO INTRODUCIDO, NO SE HAN CREADO SERVIDORES" + "\033[0;m") 



	#### MEJORA: en caso de que se ponga un parametro adicional junto a arrancar, se arrancara la maquina indicada. ####

	if len(sys.argv) == 3:	# la longitud tiene que ser obviamente 3, ya que hay un argumento mas


		if(nombre == "lb" or nombre == "c1" or nombre == "s1" or nombre == "s2" or nombre == "s3" or nombre == "s4" or nombre == "s5"):

			# Arrancamos el gestor de máquinas virtuales para monitorizar su arranque
			os.system("HOME=/mnt/tmp sudo virt-manager")
			
			print("\nCargando...\n")

			################### Configuracion de lb ########################

			if os.system("sudo virsh dominfo " + str(nombre) + " > /dev/null 2>&1") !=0:

				if os.path.exists(str(nombre) + ".xml"):
					os.system("sudo virsh define " + str(nombre) + ".xml")
				else:
					sys.exit("\033[1;31m" + "\n¡No has creado esta MV. Debes crearla previamente!\n" + "\033[0;m")

			# Creamos el fichero de configuarion hostname en el que ponemos el nombre de la MV lb
			# Hacemos uso del mismo comando que para crear el fichero pc1.cfg
			os.system("touch /mnt/tmp/pc1/hostname")
			os.system("echo " + str(nombre) + " > /mnt/tmp/pc1/hostname")


			# Copiamos el fichero hostname en el directorio /etc de lb
			# Dice el enunciado que se puede sobrescribir sin problema
			os.system("sudo virt-copy-in -a " + str(nombre) + ".qcow2 /mnt/tmp/pc1/hostname /etc")
			



			# Creamos el fichero interfaces
			os.system("touch /mnt/tmp/pc1/interfaces")

			if(nombre == "lb"):
				# Reescribimos el fichero interfaces para introducir las interfaces correspondientes de nuestra red para lb
				n = open('/mnt/tmp/pc1/interfaces',"w") 	    
				n.write("auto lo\niface lo inet loopback\n\nauto eth0\niface eth0 inet static\naddress 10.0.1.1\nnetmask 255.255.255.0\ngateway 10.0.1.2\n\nauto eth1\n\niface eth1 inet static\naddress 10.0.2.1\nnetmask 255.255.255.0\ngateway 10.0.2.0\n")      		
				n.close()

			if(nombre == "c1"):
				# Reescribimos interfaces para introducir las interfaces de c1
				n = open('/mnt/tmp/pc1/interfaces',"w") 	    
				n.write("auto lo\niface lo inet loopback\n\nauto eth0\niface eth0 inet static\naddress 10.0.1.2\nnetmask 255.255.255.0\ngateway 10.0.1.1\n")      	
				n.close()

			if(nombre == "s1"):
				# Reescribimos el fichero interfaces para introducir las interfaces de s1
				n = open('/mnt/tmp/pc1/interfaces',"w") 	    
				n.write("auto lo\niface lo inet loopback\n\nauto eth0\niface eth0 inet static\naddress 10.0.2.11\nnetmask 255.255.255.0\ngateway 10.0.2.1\n")      		
				n.close()
			

			if(nombre == "s2"):
				# Reescribimos el fichero interfaces para introducir las interfaces de s2
				n = open("/mnt/tmp/pc1/interfaces","w") 	    
				n.write("auto lo\niface lo inet loopback\n\nauto eth0\niface eth0 inet static\naddress 10.0.2.12\nnetmask 255.255.255.0\ngateway 10.0.2.1\n")      		
				n.close()


			if(nombre == "s3"):
				# Reescribimos el fichero interfaces para introducir las interfaces de s3
				n = open('/mnt/tmp/pc1/interfaces',"w") 	    
				n.write("auto lo\niface lo inet loopback\n\nauto eth0\niface eth0 inet static\naddress 10.0.2.13\nnetmask 255.255.255.0\ngateway 10.0.2.1\n")      		
				n.close()

			if(nombre == "s4"):
				# Reescribimos el fichero interfaces para introducir las interfaces de s4
				n = open('/mnt/tmp/pc1/interfaces',"w") 	    
				n.write("auto lo\niface lo inet loopback\n\nauto eth0\niface eth0 inet static\naddress 10.0.2.14\nnetmask 255.255.255.0\ngateway 10.0.2.1\n")      		
				n.close()

			if(nombre == "s5"):
				# Reescribimos el fichero interfaces para introducir las interfaces de s5
				n = open('/mnt/tmp/pc1/interfaces',"w") 	    
				n.write("auto lo\niface lo inet loopback\n\nauto eth0\niface eth0 inet static\naddress 10.0.2.15\nnetmask 255.255.255.0\ngateway 10.0.2.1\n")      		
				n.close()

			# Copiamos el fichero interfaces en el directorio /etc/network de lb
			os.system("sudo virt-copy-in -a " + str(nombre) + ".qcow2 /mnt/tmp/pc1/interfaces /etc/network")

			if(nombre == "lb"):

				# Edicion del fichero /etc/sysctl.conf para configurar el balanceador como router
				os.system("sudo virt-edit -a " + str(nombre) + ".qcow2 /etc/sysctl.conf -e 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/'")

				# -e: Instead of launching the external editor, non-interactively apply the Perl expression EXPR 
				# (lo que esta entre ') to each line in the file.
				# For example to replace all instances of foo with bar in a file: 's/foo/bar/'
				# Entonces teniendo en cuenta que en el archivo sysctl.conf pone: 
				# Uncomment the next line to enable packet forwarding for IPv4
				# #net.ipv4.ip_forward=1
				# Todo lo que tenemos que hacer es descomentarla, mismo procedimiento que foo y bar.


			os.system("sudo virsh start " + str(nombre) + "")
			os.system("xterm -rv -sb -rightbar -fa monospace -fs 10 -title '" + str(nombre) + "' -e 'sudo virsh console " + str(nombre) + "' &")
			print("\nMaquina " + str(nombre) + " arrancada con exito\n")



		else:
			print("\033[1;31m" + "\nNO ES VALIDO EL PARAMETRO INTRODUCIDO\n" + "\033[0;m")
