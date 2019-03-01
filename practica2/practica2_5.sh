#!/bin/bash

#----------------------------------
# Autor: Rubén Rodríguez Esteban
# NIP: 737215
#----------------------------------

IFS=$'\n'

echo -n "Introduzca el nombre de un directorio: "
read dir

# Comprobación de si el dato del usuario es un directorio
if [ -d $dir ]
then
	# Cuenta de los ficheros y subdirectorios 

	numFich=$(find $dir -maxdepth 2 -type f | wc -l)
	numDir=$(find $dir -maxdepth 1 -type d | wc -l)

	# Se debe descontar uno porque se cuenta el directorio actual
	numDir=$((numDir - 1))

	# Muestra por salida estándar los resultados
	echo "El numero de ficheros y directorios en $dir es de $numFich y $numDir, respectivamente"
else
	echo "$dir no es un directorio"
        exit 1	
fi	
# Petición al usuario del nombre del directorio
