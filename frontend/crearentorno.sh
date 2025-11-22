#!/bin/bash

echo "Ingrese el nombre del directorio a crear o borrar"
read nombre

if [[ "$1" == "-d" ]]; then
	rm -r $nombre
	exit
fi

sudo apt install python3-pip && echo "Instalando python..."
sudo apt install pipenv && echo "Instalando pipenv..."

mkdir $nombre
mkdir $nombre/.venv
mkdir $nombre/static
mkdir $nombre/templates
mkdir $nombre/static/css
mkdir $nombre/static/images
cd $nombre
touch app.py
pipenv install flask
pipenv install flask_mail
echo "Desea iniciar el entorno virtual?"
echo "1. Si"
echo "Otro carácter: No"
read respuesta

if [[ $respuesta == "1" ]]; then
	pipenv shell
	echo "Entorno virtual iniciado"
fi
exit
