# ftl_quantum

_Tu peux lire ce readme en [anglais](README.md)_

Ma version du projet nécessite un fichier `.env`.

Celui-ci contient une variable `TOKEN` dont la valeur est le token API de IMBQ que l'on peut obtenir de https://quantum.ibm.com/

```
TOKEN=ton token ...
```

## Exercice 1: Token
Le sujet pour cet exercice à la consigne suivante:
> En utilisant la fonction IBMQ.get_provider, écrivez un programme qui va devoir:
>
    > - Lister tous les simulateurs quantiques disponibles avec leur queue actuelle.
    > - Lister tous les ordinateurs quantiques disponibles avec leur queue actuelle ainsi que le nombre de qubits qu’ils disposent.

La fonction `IBMQ.get_provider()` et l’objet `IBMQ` mentionnés sont, depuis la version 0.40.0 du package `qiskit-ibmq-provider` et 0.20.0 de Qiskit obsolète, et ont été supprimés avec la 1.0.0.

J'ai essayé de faire l'exercice avec une ancienne version de Qiskit (0.22.0) mais obtient l'erreur `ImportError: cannot import name 'IBMQ' from partially initialized module 'qiskit'` en voulant importer `IBMQ` de `qiskit`, c.f. la branche dediée: https://github.com/Killian-Morin/ftl_quantum/tree/qiskit_pre_0.40.0

sources annoncant la fin du support `IBMQ.get_provider()`:
- https://github.com/Qiskit/qiskit-ibmq-provider
- https://github.com/Qiskit/qiskit/blob/d86f9958516ee7f48359ddc7364050bb791602d1/releasenotes/notes/1.0/remove-ibmq-4bb57a04991da9af.yaml#L4
- https://medium.com/qiskit/release-news-qiskit-v0-40-is-here-cdcdc8d400d4
- https://docs.quantum.ibm.com/api/migration-guides/qiskit-runtime-from-ibmq-provider → guide de migration pour remplacer `IBMQ.get_provider()`
- https://quantumcomputing.stackexchange.com/questions/37042/ibmq-import-error

## Exercice 2: Superposition
L'état à obtenir dans cet exercice est l'état $\frac{1}{\sqrt{2}}(\ket{0}+\ket{1})$.

Cet état est l'état $\ket{+}$ (plus) et fait partie des états communs.

Il peut également être noté de la façon suivante: $\frac{1}{\sqrt{2}}\ket{0}+\frac{1}{\sqrt{2}}\ket{1}$.

Cet état est une superposition égale de $\ket{0}$ et $\ket{1}$. Les coefficients $\alpha$ et $\beta$ ont les deux pour valeurs $\frac{1}{\sqrt{2}}$.
Ces coordonnées (x, y, z) sur la [sphère de Bloch](https://fr.wikipedia.org/wiki/Sph%C3%A8re_de_Bloch) sont (1, 0, 0).

## Exercice 3: Entanglement
Cette fois-ci le circuit à construire implique 2 qubits et doit créer l'état suivant: $\frac{1}{\sqrt{2}}(\ket{00}+\ket{11})$.

Le circuit créé, avec une porte d’Hadamard, une CNOT gate et les deux qubits initialisés à $\ket{00}$ permet de créer l’état $\ket{\Phi^+}$ (Phi), un des [état de Bell](https://fr.wikipedia.org/wiki/%C3%89tats_de_Bell).

## Exercice 4: Quantum noise
La création du circuit est la même que pour l’ex03 mais l'exécution du circuit ne se fait plus sur un simulateur quantique, c'est désormais sur un vrai ordinateur quantique qu'on le run.

## Exercice 5: Deutsch-Jozsa

## Exercice 6: Algorithme de recherche
