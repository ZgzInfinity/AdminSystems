#!/bin/bash

#----------------------------------
# Autor: Rubén Rodríguez Esteban
# NIP: 737215
#----------------------------------

# Comprobación del número de parámetros
if [ $# -eq 0 ]
then
	echo "No hay suficientes parámetros"
	exit 1
fi
#Bucle de lectura de parámetros
for var in "$@"
do
	# Comprobación de si estamos gestionando el primer parámetro
	if [ "$var" != "$1" ]
	then
		# Extender el grupo con el nombre del volumen
		sudo vgextend "$1" "$var"
	fi 
done

