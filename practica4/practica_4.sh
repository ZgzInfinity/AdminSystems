#!/bin/bash

#----------------------------------
# Autor: Rubén Rodríguez Esteban
# NIP: 737215
#----------------------------------

# Comprobación del número de parámetros del script
if [ $# -ne 3 ]
then
    echo "Numero incorrecto de parametros"
    exit 1
fi

# Verificación de la existencia del fichero de máquinas
if [ ! -e $3 ]
then
    echo "El fichero de maquinas no existe"
    exit 2
fi

# Verificación de la existencia del fichero de usuarios
if [ ! -e $2 ]
then
    echo "El fichero de usuarios no existe"
    exit 3
fi

# Bucle de lectura del fichero de maquinas
while read linea
do

    # Guardar maquina leída de fichero
    # Comprobación de conexión con ella a través de ssh
    maquinaLeida=$(echo "$linea" | cut -d "," -f1)
    ssh -n -q -o ConnectTimeout=1 as@$maquinaLeida -i $HOME/.ssh/id_as_ed25519 exit
    if [ $? -ne 0 ]
    then
        # La conexión ssh no ha funcionado
        echo "$maquinaLeida no es accesible"
        exit 4
    fi

    # LocalHost se ha conectado bien con la máquina
    echo "LocalHost conectado con la maquina virtual $maquinaLeida"
    if [ "$1" = "-a" ]
    then
        # Bucle para añadir usuarios de fichero
        while read lineaUser
        do
            # Obtención de los datos
            idUsuario=$(echo "$lineaUser" | cut -d ","  -f1)
	          password=$(echo "$lineaUser" | cut -d "," -f2)
	          nombUser=$(echo "$lineaUser" | cut -d "," -f3)

            # Verificación de que los campos son correctos
            if test -n "$idUsuario"  && test -n "$password" && test -n "$nombUser"
            then
                # Comprobar la ya posible existencia del usuario leído
                ssh -n as@$maquinaLeida -i $HOME/.ssh/id_as_ed25519 id -u $idUsuario &> /dev/null

                if [ $? -ne 0 ]
	              then
                    # El usuario no existe y se añade
                    ssh -n as@$maquinaLeida -i $HOME/.ssh/id_as_ed25519 "sudo useradd -c "\"${nombUser}\"" -U -K UID_MIN=1000 -m -k /etc/skel $idUsuario"
                    ssh -n as@$maquinaLeida -i $HOME/.ssh/id_as_ed25519 "echo $idUsuario:$password | sudo chpasswd"
                    ssh -n as@$maquinaLeida -i $HOME/.ssh/id_as_ed25519 "sudo passwd -x30 "$idUsuario" &> /dev/null"
                    ssh -n as@$maquinaLeida -i $HOME/.ssh/id_as_ed25519 "sudo usermod -s /bin/bash "$idUsuario" &> /dev/null"
                    echo "$nombUser ha sido creado"
		            else
                    # El usuario ya existe en la máquina
                    echo "El usuario $idUsuario ya existe"
                fi
            else
                # Opción inválida
                echo "Campo invalido"
            fi
         done < $2
    elif [ "$1" = "-s" ]
    then
          # Comrpobar si existe en raíz el diretorio /extra/backup
          ssh -n as@$maquinaLeida -i $HOME/.ssh/id_as_ed25519 test -d /extra/backup
          if [ $? -ne 0 ]
          then
              # El directorio /extra/backup no existe y lo crea
              ssh -n as@$maquinaLeida -i $HOME/.ssh/id_as_ed25519 "sudo mkdir -p /extra/backup"
      	  fi
          while read lineaUser
          do
              # Lee del fichero el usuario a borrar y verifica si existe
              idUsuario=$(echo "$lineaUser" | cut -d ","  -f1)
              ssh -n as@$maquinaLeida -i $HOME/.ssh/id_as_ed25519 id -u $idUsuario &> /dev/null
              if [ $? -ne 0 ]
              then
                  # El usuario no existe y por tanto no se borra
                  echo "El usuario $idUsuario no existe"
              else
                  # El usuario existe y lo borra
                  ssh -n as@$maquinaLeida -i $HOME/.ssh/id_as_ed25519 "sudo usermod -L "$idUsuario" &> /dev/null"
                  ssh -n as@$maquinaLeida -i $HOME/.ssh/id_as_ed25519 "sudo tar -zcvf /extra/backup/"$idUsuario".tar ~"$idUsuario" &> /dev/null"
                  ssh -n as@$maquinaLeida -i $HOME/.ssh/id_as_ed25519 "test -e /extra/backup/"$idUsuario".tar " &> /dev/null
                  # Comprobación de si el tar se ha hecho bien
                  if [ $? -ne 0 ]
                  then
                      # El proceso de creado de tar ha ido mal
                      echo "El archivo tar no se ha creado "
                      exit 5
                  else
                      # El tar se ha creado bien y el usuario se elimina
                      echo "El archivo tar se ha creado correctamente"
                      ssh -n as@$maquinaLeida -i $HOME/.ssh/id_as_ed25519 "sudo userdel -r "$idUsuario" &> /dev/null"
			                echo "El usuario $idUsuario ha sido eliminado"
                  fi
               fi
            done < $2
    else
        echo "Campo invalido"
    fi
done < $3
