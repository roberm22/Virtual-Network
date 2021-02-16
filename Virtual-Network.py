#!/usr/bin/python
#coding=utf-8

import sys

from lxml import etree
import subprocess
from subprocess import call

# Sirve para crear y modificar los ficheros XML de definicion de las MVs

import os

# el modulo nos permite acceder a funcionalidades dependientes del
# Sistema Operativo. Sobre  todo, aquellas que nos refieren informacion
# sobre el entorno del mismo y nos permiten manipular la estructura 
# de directorios (para leer y escribir archivos)


#######################################################################################
######				    Orden crear				 	 ######
#######################################################################################
###### 		   Para crear los ficheros *.qcow2 de diferencias y los de       ######
######   especificacion en XML de cada MV, asi como los bridges virtuales que    ###### 
######               soportan las LAN del escenario.                             ######
#######################################################################################

def crear(num):

	# El enunciado dice que el numero de servidores web a arrancar debera ser configurable (de 1 a 5).
	# Este numero se debera especificar mediante un segundo parametro de la linea de comandos que sera
	# opcional: si se proporciona, se tomara el valor especificado; y si no, se asignara el valor por
	# defecto de 2. Entonces:

	try:
		if len(sys.argv) == 2:	
			
			num_serv = 2	#Valor por defecto
		else:
			num = sys.argv[2] 

			#the len(sys.argv) function you can count the number of arguments.
			#sys.argv is a list in Python, which contains the command-line arguments passed to the script.

		# A continuacion guardamos el numero de maquinas que se introduce como parametro


		if((int(num) >= 0) and (int(num) <= 5)):
				
			num_serv = int(num)
		
		else:

			# En el enunciado pone que el script dara un error en caso contrario. Por lo que si el parametro
			# que han puesto no esta en el rango que se pide mostraremos un mensaje de error.

			sys.exit("\033[1;31m" + "\nValor fuera de rango. Introduzca un valor entre 0-5\n" + "\033[0;m")

	except ValueError:

		sys.exit("\033[1;31m" + "\nParametro invalido, debe ser un numero\n" + "\033[0;m")


	# Lo siguiente que vamos a hacer es guardar el numero de maquinas en un fichero ya que en el enunciado pone
	# "Ese numero se almacenara en un fichero de configuracion en el directorio de trabajo (pc1.cfg) y 
	# el resto de comandos (arrancar, parar, destruir) lo leeran de ese fichero."

	# os.system execute the command (a string) in a subshell. 

	# El comando touch de Linux se usa principalmente para crear archivos vacios y 
	# cambiar marcas de tiempo de archivos o carpetas. En este caso, sin ningun
	# parametro mas, unicamente crea un nuevo archivo

	# Unlike Java, the '+' does not automatically convert numbers or other types to
	# string form. The str() function converts values to a string form so they can 
	# be combined with other strings.

	# Con echo y el operador >, como el archivo existe, la salida de echo se agrega al comienzo del archivo, 
	# sobrescribiendo cualquier contenido anterior.



	if os.path.exists("/mnt/tmp/pc1"):
		print("La carpeta de la practica esta creada")
	else:
		sys.exit("\033[1;31m" + "\n¡No has creado la carpeta de la practica!.\nDebes crear la carpeta en mnt/tmp/pc1 y ejecutar el script desde ahi\n" + "\033[0;m")

	if os.path.exists("/mnt/tmp/pc1/cdps-vm-base-pc1.qcow2"):
		print("La imagen esta en la carpeta de la practica")
	else:
		sys.exit("\033[1;31m" + "\n¡No esta la imagen de la practica!.\nDebes copiarla o descargarla en la carpeta /mnt/tmp/pc1\n" + "\033[0;m")

	if os.path.exists("/mnt/tmp/pc1/plantilla-vm-pc1.xml"):
		print("La plantilla esta en la carpeta de la practica")
	else:
		sys.exit("\033[1;31m" + "\n¡No esta la plantilla xml de la practica!.\nDebes copiarla o descargarla en la carpeta /mnt/tmp/pc1\n" + "\033[0;m")


	if os.path.exists("/mnt/tmp/pc1/pc1.py"):
		print("El script esta en la carpeta de la practica")
	else:
		sys.exit("\033[1;31m" + "\n¡El script no esta en la carpeta de la practica!.\nEl script debe estar en la carpeta /mnt/tmp/pc1\n" + "\033[0;m")


	if os.path.abspath("pc1.py") == "/mnt/tmp/pc1/pc1.py":
		print("El script se esta ejecutando en la carpeta de la practica")
	else:
		print("\nLa ruta actual es:" + os.path.abspath("pc1.py"))		
		sys.exit("\033[1;31m" + "\n¡Estas ejecutando el script en la carpeta incorrecta o tienes copias del script!.\nEl script debe ser unico y ejecutarse en la carpeta /mnt/tmp/pc1\n" + "\033[0;m")


	os.system("touch pc1.cfg")
	os.system("echo "+str(num_serv)+" > pc1.cfg")




	# Por defecto siempre se crearan c1 y lb. Una vez hecho esto, se crearan el 
	# numero de servidores que se haya puesto como parametro. Hacemos uso del comando necesario (mirar practica 1)

	# Para crear las imagenes que utilizaran las maquinas virtuales derivadas de cdps-vm-base-pc1.qcow2
	os.system('qemu-img create -f qcow2 -b cdps-vm-base-pc1.qcow2 lb.qcow2')
	# Copia de la plantilla XML para la nueva maquina virtual (mirar practica 3)
	os.system('cp plantilla-vm-pc1.xml lb.xml')
	os.system('qemu-img create -f qcow2 -b cdps-vm-base-pc1.qcow2 c1.qcow2')
	os.system('cp plantilla-vm-pc1.xml c1.xml')


	################################################################
	################### 	Creacion de lb  ########################
	################################################################


	# Cargamos el fichero XML correspondiente a lb y obtenemos el nodo raiz
	# (Sacado a partir del ejemplo en el enunciado de la practica)

	tree = etree.parse('lb.xml')
	root = tree.getroot()

	# An ElementTree is mainly a document wrapper around a tree with a root node. 
	# ElementTree class serialises as a complete document. Por lo tanto,
	# guardamos en la variable "arbol" la estructura del fichero XML que modificaremos.
	# https://docs.python.org/2/library/xml.etree.elementtree.html#xml.etree.ElementTree.ElementTree.write

	arbol = etree.ElementTree(root)
	# Necesario poner root, sino: AssertionError: ElementTree not initialized, missing root


	# Buscamos la etiqueta name en el xml y la guardamos en "name"
	# (Ejemplo de fichero xml en onedrive -> apartado2.xml)

	name = root.find("name")

	# Cambiamos el valor de "name"

	name.text = 'lb'

	# Buscamos la etiqueta source bajo el nodo /devices/disk y la guardamos en "sourcedisk"

	sourcedisk = root.find("./devices/disk/source")	

	# Editamos ese valor y ponemos donde se encuentra la imagen
	# <source file='...'/>

	sourcedisk.set("file", '/mnt/tmp/pc1/lb.qcow2')	

	# Buscamos la etiqueta source bajo el nodo /devices/interfaces y la guardamos en "sourceint1"

	sourceint1 = root.find("./devices/interface/source")

	# Editamos el bridge de LAN1 (Sacado de practica 3, es lo mismo)

	sourceint1.set("bridge", 'LAN1')

	# Ahora es necesario sumar una nueva lan, LAN2, para ello tendremos que crear una nueva 
	# etiqueta interface. De la documentacion podemos sacar:
	# The SubElement factory. It accepts the same arguments as the Element factory, but 
	# additionally requires the parent as first argument. En nuestro caso, el primer parametro 
	# (padre) va a ser la etiqueta devices
 
	padredevices = root.find("devices")

	# Creamos el subElement de padredevices, que sera la etiqueta interface
	subinter = etree.SubElement(padredevices, "interface", type='bridge')

	#Ahora de esa etiqueta, salen sus dos etiquetas hijas source y model

	sourcehija = etree.SubElement(subinter, "source", bridge='LAN2')
	modelhija = etree.SubElement(subinter, "model", type='virtio')

	
	arbol.write("lb.xml")



	################################################################
	################### 	Creacion de c1  ########################
	################################################################


	# Cargamos el fichero XML correspondiente a c1 y obtenemos el nodo raiz
	tree = etree.parse('c1.xml')
	root = tree.getroot()

	# Guardamos en la variable "arbol" la estructura del fichero XML que modificaremos.
	arbol = etree.ElementTree(root)

	# Buscamos la etiqueta name en el xml y la guardamos en "name"
	name = root.find("name")

	# Cambiamos el valor de "name"
	name.text = 'c1'

	# Buscamos la etiqueta source bajo el nodo /devices/disk y la guardamos en "sourcedisk"
	sourcedisk = root.find("./devices/disk/source")	

	# Editamos ese valor y ponemos donde se encuentra la imagen
	sourcedisk.set("file", '/mnt/tmp/pc1/c1.qcow2')

	# Buscamos la etiqueta source bajo el nodo /devices/interfaces y la guardamos en "sourceint1"
	sourceint1 = root.find("./devices/interface/source")

	# Editamos el bridge de LAN1
	sourceint1.set("bridge", 'LAN1')


	arbol.write("c1.xml")


	# Imprimimos por pantalla un mensaje de que se han creado lb y c1
	print("\033[1;35m" + "\nSE HAN CREADO CON EXITO LB Y C1\n" + "\033[0;m")

	# Creamos los bridges correspondientes a las dos redes virtuales.

	os.system("sudo brctl addbr LAN1")
	os.system("sudo brctl addbr LAN2")
	os.system("sudo ifconfig LAN1 up")
	os.system("sudo ifconfig LAN2 up")


	print("\033[1;35m" + "SE HAN CREADO CON EXITO LOS BRIDGES" + "\033[0;m")

	################################################################
	###################      Crear MV's	########################
	################################################################

	if ((num_serv >= 1) and (num_serv <= 5)):



		# Comprobamos que el valor que se ha introducido esta en el rango
		# y no es cero, entonces como minimo ya tendremos que crear s1

		# Misma mecanica que para la creacion de lb y c1

		os.system("qemu-img create -f qcow2 -b cdps-vm-base-pc1.qcow2 s1.qcow2")
		os.system("cp plantilla-vm-pc1.xml s1.xml")

		# Cargamos el fichero XML correspondiente a s1 y obtenemos el nodo raiz
		tree = etree.parse('s1.xml')
		root = tree.getroot()
		# Guardamos en la variable "arbol" la estructura del fichero XML que modificaremos.
		arbol = etree.ElementTree(root)
		# Buscamos la etiqueta name en el xml y la guardamos en "name"
		name = root.find("name")
		# Cambiamos el valor de "name"
		name.text = 's1'
		# Buscamos la etiqueta source bajo el nodo /devices/disk y la guardamos en "sourcedisk"
		sourcedisk = root.find("./devices/disk/source")	
		# Editamos ese valor y ponemos donde se encuentra la imagen
		sourcedisk.set("file", '/mnt/tmp/pc1/s1.qcow2')
		# Buscamos la etiqueta source bajo el nodo /devices/interfaces y la guardamos en "sourceint1"
		sourceint1 = root.find("./devices/interface/source")
		# Editamos el bridge de LAN2
		sourceint1.set("bridge", 'LAN2')

		arbol.write("s1.xml")


		print("\033[1;35m" + "SE HA CREADO CON EXITO S1" + "\033[0;m")


		# Si el parametro que se introduce es mayor que 1, entonces tendremos que crear s2 tambien
		if (num_serv >= 2):

			os.system("qemu-img create -f qcow2 -b cdps-vm-base-pc1.qcow2 s2.qcow2")
			os.system("cp plantilla-vm-pc1.xml s2.xml")

			# Cargamos el fichero XML correspondiente a s2 y obtenemos el nodo raiz
			tree = etree.parse('s2.xml')
			root = tree.getroot()
			# Guardamos en la variable "arbol" la estructura del fichero XML que modificaremos.
			arbol = etree.ElementTree(root)
			# Buscamos la etiqueta name en el xml y la guardamos en "name"
			name = root.find("name")
			# Cambiamos el valor de "name"
			name.text = 's2'
			# Buscamos la etiqueta source bajo el nodo /devices/disk y la guardamos en "sourcedisk" 
			sourcedisk = root.find("./devices/disk/source")	
			# Editamos ese valor y ponemos donde se encuentra la imagen
			sourcedisk.set("file", 'mnt/tmp/pc1/s2.qcow2')
			# Buscamos la etiqueta source bajo el nodo /devices/interfaces y la guardamos en "sourceint1"
			sourceint1 = root.find("./devices/interface/source")
			# Editamos el bridge de LAN2
			sourceint1.set("bridge", 'LAN2')

			arbol.write("s2.xml")


			print("\033[1;35m" + "SE HA CREADO CON EXITO S2" + "\033[0;m")

		# Si el parametro que se introduce es mayor que 2, entonces tendremos que crear s3 tambien
		if (num_serv >= 3):	

			os.system("qemu-img create -f qcow2 -b cdps-vm-base-pc1.qcow2 s3.qcow2")
			os.system("cp plantilla-vm-pc1.xml s3.xml")

			# Cargamos el fichero XML correspondiente a s3 y obtenemos el nodo raiz
			tree = etree.parse('s3.xml')
			root = tree.getroot()
			# Guardamos en la variable "arbol" la estructura del fichero XML que modificaremos.
			arbol = etree.ElementTree(root)
			# Buscamos la etiqueta name en el xml y la guardamos en "name"
			name = root.find("name")
			# Cambiamos el valor de "name"
			name.text = 's3'
			# Buscamos la etiqueta source bajo el nodo /devices/disk y la guardamos en "sourcedisk" 
			sourcedisk = root.find("./devices/disk/source")	
			# Editamos ese valor y ponemos donde se encuentra la imagen
			sourcedisk.set("file", 'mnt/tmp/pc1/s3.qcow2')
			# Buscamos la etiqueta source bajo el nodo /devices/interfaces y la guardamos en "sourceint1"
			sourceint1 = root.find("./devices/interface/source")
			# Editamos el bridge de LAN2
			sourceint1.set("bridge", 'LAN2')

			arbol.write("s3.xml")


			print("\033[1;35m" + "SE HA CREADO CON EXITO S3" + "\033[0;m")


		# Si el parametro que se introduce es mayor que 3, entonces tendremos que crear s4 tambien
		if (num_serv >= 4):	

			os.system("qemu-img create -f qcow2 -b cdps-vm-base-pc1.qcow2 s4.qcow2")
			os.system("cp plantilla-vm-pc1.xml s4.xml")
			
			# Cargamos el fichero XML correspondiente a s4 y obtenemos el nodo raiz
			tree = etree.parse('s4.xml')
			root = tree.getroot()
			# Guardamos en la variable "arbol" la estructura del fichero XML que modificaremos.
			arbol = etree.ElementTree(root)
			# Buscamos la etiqueta name en el xml y la guardamos en "name"
			name = root.find("name")
			# Cambiamos el valor de "name"
			name.text = 's4'
			# Buscamos la etiqueta source bajo el nodo /devices/disk y la guardamos en "sourcedisk" 
			sourcedisk = root.find("./devices/disk/source")	
			# Editamos ese valor y ponemos donde se encuentra la imagen
			sourcedisk.set("file", 'mnt/tmp/pc1/s4.qcow2')
			# Buscamos la etiqueta source bajo el nodo /devices/interfaces y la guardamos en "sourceint1"
			sourceint1 = root.find("./devices/interface/source")
			# Editamos el bridge de LAN2
			sourceint1.set("bridge", 'LAN2')

			arbol.write("s4.xml")


			print("\033[1;35m" + "SE HA CREADO CON EXITO S4" + "\033[0;m")


		# Si el parametro que se introduce es mayor que 4, entonces tendremos que crear s5 tambien
		if (num_serv == 5):	

			os.system("qemu-img create -f qcow2 -b cdps-vm-base-pc1.qcow2 s5.qcow2")
			os.system("cp plantilla-vm-pc1.xml s5.xml")

			# Cargamos el fichero XML correspondiente a s5 y obtenemos el nodo raiz
			tree = etree.parse('s5.xml')
			root = tree.getroot()
			# Guardamos en la variable "arbol" la estructura del fichero XML que modificaremos.
			arbol = etree.ElementTree(root)
			# Buscamos la etiqueta name en el xml y la guardamos en "name"
			name = root.find("name")
			# Cambiamos el valor de "name"
			name.text = 's5'
			# Buscamos la etiqueta source bajo el nodo /devices/disk y la guardamos en "sourcedisk" 
			sourcedisk = root.find("./devices/disk/source")	
			# Editamos ese valor y ponemos donde se encuentra la imagen
			sourcedisk.set("file", 'mnt/tmp/pc1/s5.qcow2')
			# Buscamos la etiqueta source bajo el nodo /devices/interfaces y la guardamos en "sourceint1"
			sourceint1 = root.find("./devices/interface/source")
			# Editamos el bridge de LAN2
			sourceint1.set("bridge", 'LAN2')

			arbol.write("s5.xml")


			print("\033[1;35m" + "SE HA CREADO CON EXITO S5" + "\033[0;m")

	else:
		print("\033[1;31m" + "\nNO SE HAN CREADO SERVIDORES :(\n " + "\033[0;m")	



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


#######################################################################################
######				    Programa				 	 ######
#######################################################################################
###### 		   Para ejecutar el programa en el formato que se 	         ######
######   			pide en el enunciado    			 ###### 
######              	    pc1 <orden> <otros_parametros>                       ######
#######################################################################################


if len(sys.argv) <= 1:
	
	# El script pc1 se ejecutara pasandole un parametro obligatorio que definira
	# la operacion a realizar

	sys.exit("Ejecucion del script incorrecta. Es obligatorio el siguiente formato: pc1 <orden> <otros_parametros>")

else:

	# En la orden crear se explica que es sys.argv y en este caso,
	# su posicion 1 es la corresponde a <orden>

	orden = sys.argv[1]

	# Si la longitud de sys.argv es 2 significa que se ha introducido solo la orden
	if len(sys.argv) == 2:
		num = 2	
	# Por lo tanto, valor por defecto

	# Si la longitud de sys.argv es 3 significa que se ha introducido el numero de servidores
	if len(sys.argv) == 3:
		num = sys.argv[2]
	# Por lo tanto, valor introducido

	# Si la longitud de sys.argv es 4 significa que has escrito de mas
	if len(sys.argv) >= 4:
		sys.exit("\033[1;31m" + "\nEjecucion del script incorrecta. Es obligatorio el siguiente formato:\npc1 <orden> <otros_parametros>\n" + "\033[0;m")

# https://www.w3schools.com/python/python_dictionaries.asp

dictionary = {
	"crear": crear, 
	"create": crear,
	"arrancar": arrancar, 
	"start" : arrancar,
	"parar": parar, 
	"stop": parar,
	"destruir": destruir,
	"destroy": destruir,
	"release": destruir,
	"monitor": monitor
}
	
# https://stackoverflow.com/questions/5312778/how-to-test-if-a-dictionary-contains-a-specific-key
# El if...in comprueba si orden esta en el diccionario
if orden in dictionary:	
	dictionary[orden](num)

else:
	sys.exit("\033[1;31m" + "\nEjecucion del script incorrecta. Es obligatorio el siguiente formato:\npc1 <orden> <otros_parametros>\n" + "\033[0;m")

