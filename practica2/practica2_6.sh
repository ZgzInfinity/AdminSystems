#!/bin/bash

#----------------------------------
# Autor: Rubén Rodríguez Esteban
# NIP: 737215
#----------------------------------

IFS=$'\n'

# Busqueda de un directorio con el formato binXXX en el direcotrio /home/ menos recientemento modificado
dir=$(find $HOME -type d -regex "$HOME/bin[a-zA-Z0-9][a-zA-Z0-9][a-zA-Z0-9]" -exec stat -c "%y %n" {} \; | sort -r | head -n 1 | cut -d" " -f4)

# Verificación de que se ha encontrado
if [ -z $dir ]; then

	# Si no se encuentra se crea un directorio temporal
	dir=$(mktemp -d $HOME/binXXX)
	echo "Se ha creado el directorio $dir"
fi


echo "Directorio destino de copia: $dir"

# Bucle que copia los archivos
count=0
for var in *
do
	# Verifica si el archivo es ejecutable
	if [ -x $var ] 
	then
		cp $var $dir
		count=$((count+1))
		echo "./$var ha sido copiado a $dir"
	fi
done

echo "Se han copiado $count archivos"
