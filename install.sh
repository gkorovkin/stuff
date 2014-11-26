#!/bin/bash

#file to link emacs config
if [ ! -e ~/.emacs ]; 
then
    echo "Linking emacs_config to ~/.emacs"
    ln -s ./emacs_config ~/.emacs
else
    echo "File ~/.emacs already exist - delete it and run again"
    exit
fi
