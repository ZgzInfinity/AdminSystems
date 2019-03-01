#!/bin/bash

#----------------------------------
# Autor: Rubén Rodríguez Esteban
# NIP: 737215
#----------------------------------

# Petición de la tecla por teclado
echo -n "Introduzca una tecla: "
read tecla

# Evaluación del contenido de tecla
case "$tecla" in
	# La tecla es una letra mayúscula o minúscula

	[a-zA-Z] )
	    echo $tecla "es una letra ";;

	# La tecla es un dígito
	[0-9] )
	    echo $tecla "es un numero ";;

	# Resto de posibles caracteres
	* )
	    echo "$tecla" "es un caracter especial ";;
esac

