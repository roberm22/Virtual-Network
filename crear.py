
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
