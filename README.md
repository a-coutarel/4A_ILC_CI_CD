# 4A_ILC_CI_CD - ESIREM

Groupe :
--------
**COUTAREL Allan**    
**DEVOUCOUX Maxime**

----

## Descriptif du langage Python

Python est un langage de programmation populaire, conçu pour être lisible et facile à apprendre. Il est souvent utilisé comme langage de script pour automatiser des tâches, mais peut également être utilisé pour développer des applications à grande échelle. Python est connu pour être très flexible et est utilisé dans de nombreux domaines, y compris la science des données, l'intelligence artificielle et le développement web. Il est également compatible avec de nombreux systèmes d'exploitation et peut être utilisé avec de nombreuses bibliothèques et frameworks.

----

## TD1

Découverte et prise en main des commandes Git via les activités du site : https://learngitbranching.js.org/

----

## TD2

* Création et configuration du dépôt

* Création de diverses actions : 

    - Une action qui se déclenche à chaque push pour exécuter echo "New push !"
        >(4A_ILC_CI_CD/.github/workflows/echo_on_push.yml)
        >> ![Status_actions](https://github.com/a-coutarel/4A_ILC_CI_CD/actions/workflows/echo_on_push.yml/badge.svg)

    - Une action qui se déclenche sur commande manuel pour exécuter une commande curl sur l’adresse wttr.in/Moon
        > (4A_ILC_CI_CD/.github/workflows/curl_moon.yml)
        >> ![Status_actions](https://github.com/a-coutarel/4A_ILC_CI_CD/actions/workflows/curl_moon.yml/badge.svg)

    - Une action qui se déclenche à chaque Pull Request avec un job utilisant actions/checkout@v3 pour accéder au code, actions/setup-python@v4 pour installer python et exécutant la commande python main.py :
        > (4A_ILC_CI_CD/.github/workflows/python_install_and_run.yml)
        >> ![Status_actions](https://github.com/a-coutarel/4A_ILC_CI_CD/actions/workflows/python_install_and_run.yml/badge.svg)

----
