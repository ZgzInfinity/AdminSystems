#!/bin/bash

#----------------------------------
# Autor: Rubén Rodríguez Esteban
# NIP: 737215
#----------------------------------

# Comprobación del número de parámetros del script
if [ $# -ne 1 ]
then
    echo "Numero incorrecto de parametros"
    exit 1
fi

for var in "$@"
do
	# Establecer conexión ssh con la máquina virtual 
	ssh -n -q -o ConnectTimeout=1 as@$var -i $HOME/.ssh/id_as_ed25519 exit
	if [ $? -ne 0 ]
    	then
		# La conexión ssh ha fallado y se informa del error
        	echo "$var no es accesible"
        	exit 2
	fi

	echo "LocalHost conectado con la maquina virtual $var"

	# Informar de los discos duros disponibles y de su tamaño en bloques
	echo "Disco       Bloques"
	muestra=$(ssh -n as@$var -i $HOME/.ssh/id_as_ed25519 "sudo sfdisk -s")
	numLineas=$(echo "$muestra" | wc -l)
	echo "$muestra" | head -n $((numLineas - 1)) | awk '{ print $1 "   " $2 }'


	# Informar de particiones y de sus tamaños
	orden=$(ssh -n as@$var -i $HOME/.ssh/id_as_ed25519 "sudo sfdisk -l")
	filtro=$(echo "$orden" | grep '/dev/sd[a-z][0-9]')
	numLineas=$(echo "$filtro" | wc -l)
	echo "$filtro" | head -n 1 | awk '{ print $1 "   " $6 }'
	echo "$filtro" | tail -n $((numLineas - 1)) | awk '{ print $1 "   " $5  }'
	

	# Informar de los discos montajes capacidad 
	orden3=$(ssh -n as@$var -i $HOME/.ssh/id_as_ed25519 "sudo df -hT")
	filtro=$(echo "$orden3" | grep -v "^tmpfs")
	echo "$filtro" | awk '{ print $1  "    "  $2  "    "  $3  "    "  $5  "   "  $7 }'
done

   
