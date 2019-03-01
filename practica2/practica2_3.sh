#!/bin/bash

#----------------------------------
# Autor: Rubén Rodríguez Esteban
# NIP: 737215
#----------------------------------

IFS=$'\n'

# Verificación del número de parámetros
if test $# -ne 1
then
     # El número de parámetros es distinto de 1
     echo "Sintaxis: practica2_3.sh <nombre_archivo>" 
     exit 1
fi

# Se le ha pasado un parñametro

# Evaluación de si el fichero es regular
if test -f $1	
then
    # Se le dan permisos de ejecución al propietario y al grupo
    chmod u+x $1
    chmod g+x $1	

    # Se muestran en salida estándar en formato rwx
    stat -c %A $1 
else
    echo "$1 no existe"
fi
