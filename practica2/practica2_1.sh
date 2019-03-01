#!/bin/bash

#----------------------------------
# Autor: Rubén Rodríguez Esteban
# NIP: 737215
#----------------------------------

IFS=$'\n'

# Peticion al usuario del fichero 
echo -n "Introduzca el nombre del fichero: " 
read nomFich

# Evaluación de si el fichero es regular o no
if [ -f $nomFich ]
then
      # Muestra los permisos del fichero 
      echo -n "Los permisos del archivo $nomFich son: "

      # Verificación de los permisos de lectura del fichero
      if [ -r $nomFich ]
      then
	      echo -n "r"       
      else
	      echo -n "-"
      fi

      # Verificación de los permisos de escritura del fichero
      if [ -w $nomFich ]
      then
      	      echo -n "w"
      else
	      echo -n "-"
      fi

       # Verificación de los permisos de ejecución del fichero
      if [ -x $nomFich ]
      then
	      echo "x"
      else
	      echo "-"
      fi
else
      # Informa de que el fichero no exite
      # Devuelve como estado de salida 1
      echo "$nomFich no existe"
      exit 1
fi
