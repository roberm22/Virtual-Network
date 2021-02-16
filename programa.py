

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

