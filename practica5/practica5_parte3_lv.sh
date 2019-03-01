#!/bin/bash

#-----------------------------------
# Autor: Rubén Rodríguez Esteban ---
# NIP: 737215 ----------------------
#-----------------------------------


# Verificación de si el fichero de volúmes lógicos existe o no
if [ ! -e $1 ]
then
    echo "El fichero $1 no existe"
    exit 1
fi

# Bucle de lectura línea a línea del fichero
while read linea 
do
    # Obtención de los datos
    grupoVolumen=$(echo "$linea" | cut -d "," -f1)
    volumenLogico=$(echo "$linea" | cut -d "," -f2)
    tamanyo=$(echo "$linea" | cut -d "," -f3)
    sistemaFich=$(echo "$linea" | cut -d "," -f4)
    montaje=$(echo "$linea" | cut -d "," -f5)

    # Comprobación de la existencia del volumen lógico en el grupo
    if [ -e /dev/"$grupoVolumen"/"$volumenLogico" ]
    then
        # El volumen lógico ya existía y se procede a extender
	echo "El volumen logico ya existe"
	sudo lvextend -L "$tamanyo" /dev/"$grupoVolumen"/"$volumenLogico" 

	# Comprobación de si el volumen lógico se extiende bien
	if [ $? -ne 0 ]
	then
	     # Hay un fallo en la extensión
	     echo "La extensión del volumen lógico ha fallado"
	     exit 2
	fi
	sudo resize2fs /dev/"$grupoVolumen"/"$volumenLogico" 
    else
	# El volumen lógico no existe y debe crearse 
	sudo lvcreate -L "$tamanyo" -n "$volumenLogico" "$grupoVolumen" 

	# Verificación de si el volumen logico se ha creado bien
	if [ $? -ne 0 ]
	then
	     # Se ha producido un fallo y notifica el error 
	     echo "El volumen lógico $volumenLogico no se ha creado correctamente"
	     exit 3
	fi
	
	# Creación del sistema de ficheros
	sudo mkfs -t "$sistemaFich" /dev/"$grupoVolumen"/"$volumenLogico" 

	# Verificación de si el sistema de ficheros se ha creado bien
	if [ $? -ne 0 ]
	then
	     # Se ha producido un fallo en la creación del sistema de ficheros 
	     echo "El sistema de ficheros no se ha creado correctamente"
	     exit 4
	fi

	sudo bash -c "echo /dev/mapper/$grupoVolumen-$volumenLogico $montaje $sistemaFich auto 0 0 >> /etc/fstab"
    fi
done < $1
