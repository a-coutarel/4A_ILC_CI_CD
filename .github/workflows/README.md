# Dossier de Workflows

Ce dossier contient les différents workflows qui seront utilisés dans le projet.

Il y a trois github actions : 

* Une déclenchée à chaque changement pour builder l’application.
    > ![Status_actions](https://github.com/a-coutarel/4A_ILC_CI_CD/actions/workflows/app_build.yml/badge.svg)
* Une déclenchée manuellement pour utiliser le fichier Dockerfile pour créer une image.
    > ![Status_actions](https://github.com/a-coutarel/4A_ILC_CI_CD/actions/workflows/build_image.yml/badge.svg)
* Une déclenchée pour chaque tag semver pour utiliser le fichier Dockerfile pour créer et pousser l’image de l’API dans un GCR avec en tag la version semver spécifiée.
    > ![Status_actions](https://github.com/a-coutarel/4A_ILC_CI_CD/actions/workflows/build_and_push.yml/badge.svg)