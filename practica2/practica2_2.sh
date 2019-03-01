#!/bin/bash

#----------------------------------
# Autor: Rubén Rodríguez Esteban
# NIP: 737215
#----------------------------------

IFS=$'\n'

# Recorrido de los parámetros del script
for var in "$@"
do
      # Evaluación de si el fichero es regular	
      if test -f $var
      then
	    # Muestra por salida estándar el contenido de los ficheros
	    more $var
      else
	    # El parámetro no existe 
	    echo -n $var no es un fichero 
      fi 
done
