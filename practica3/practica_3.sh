#!/bin/bash

IFS=$'\n'

# Comprobación de los privilegios del usuario 
if [ $UID -ne 0 ]
then
     echo "Este script necesita privilegios de administracion"
     exit 1
fi
 	
#Verificación del número de parámetros
if [ $# -ne 2 ]
then
     echo "Numero incorrecto de parametros"
fi

# Constatar borrado o adición de usuarios 
if [ "$1" = "-a" ]
then
     while read linea
     do
        # Bucle para añadir usuariosi

        idUser=$(echo "$linea" | cut -d ","  -f1)
        password=$(echo "$linea" | cut -d "," -f2)
        nombUser=$(echo "$linea" | cut -d "," -f3)

        # Verificar si los campos no son nulos
        if [ -n $idUser ] && [ -n $password ] && [ -n $nombUser ]
        then
	      # Comprobar existencia de usuario
	      id -u $idUser &> /dev/null 
	      if [ $? -eq 0 ]
              then
		   echo "El usuario $idUser ya existe"
	      else
		   useradd -c "$nombUser" -U -K UID_MIN=1000 -m -k /etc/skel $idUser &> /dev/null
		   echo "$idUser:$password" | chpasswd
		   passwd -x30 $idUser &> /dev/null
		   usermod -s /bin/bash $idUser &> /dev/null		
		   echo "$nombUser ha sido creado"
              fi
         else	       
              echo "Campo invalido"
        fi
     done < $2
elif [ "$1" = "-s" ]
then
      if [ ! -d /extra/backup ]
      then
	   mkdir -p /extra/backup 
      fi
      while read linea
      do
	 idUser=$(echo "$linea" | cut -d "," -f1)
	 tar -zcvf "$idUser".tar /home/$idUser &> /dev/null 
	 mv $idUser.tar /extra/backup
	 userdel -r $idUser &> /dev/null

      done < $2
else
      echo "Opcion invalida"
fi
