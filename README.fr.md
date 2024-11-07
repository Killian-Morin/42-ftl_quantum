# ftl_quantum

_Pour lire ce readme en [anglais](README.md)_

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

<details>
  <summary>Sources</summary>

  [IBMBackend | Qiskit Documentation](https://docs.quantum.ibm.com/api/qiskit-ibm-runtime/qiskit_ibm_runtime.IBMBackend)

  [QiskitRuntimeService.backends() | Qiskit Documentation](https://docs.quantum.ibm.com/api/qiskit-ibm-runtime/qiskit_ibm_runtime.QiskitRuntimeService#backends)
</details>

## Exercice 2: Superposition

L'état à obtenir dans cet exercice est l'état $\frac{1}{\sqrt{2}}(\ket{0}+\ket{1})$.

Cet état est l'état $\ket{+}$ (plus) et fait partie des états communs.

Il peut également être noté de la façon suivante: $\frac{1}{\sqrt{2}}\ket{0}+\frac{1}{\sqrt{2}}\ket{1}$.

Cet état est une superposition égale de $\ket{0}$ et $\ket{1}$. Les coefficients $\alpha$ et $\beta$ ont les deux pour valeurs $\frac{1}{\sqrt{2}}$.
Ces coordonnées (x, y, z) sur la [sphère de Bloch](https://fr.wikipedia.org/wiki/Sph%C3%A8re_de_Bloch) sont (1, 0, 0).

## Exercice 3: Entanglement

Cette fois-ci le circuit à construire implique 2 qubits et doit créer l'état suivant: $\frac{1}{\sqrt{2}}(\ket{00}+\ket{11})$.

Le circuit créé, avec une porte d’Hadamard, une CNOT gate et les deux qubits initialisés à $\ket{00}$ permet de créer l’état $\ket{\Phi^+}$ (Phi), un des [états de Bell](https://fr.wikipedia.org/wiki/%C3%89tats_de_Bell).

## Exercice 4: Quantum noise

La création du circuit est la même que pour l’ex03 mais l'exécution du circuit ne se fait plus sur un simulateur quantique.

On va utiliser un véritable ordinateur quantique pour run ce programme.

Le but de cet exercice est de découvrir ce qu'est le **Quantum noise**. C'est du 'bruit' provoqué par un état intermédiaire, en accord avec certains des principes fondamentaux de la mécanique quantique, notamment le [principe d'incertitude](https://fr.wikipedia.org/wiki/Principe_d%27incertitude).

Cela provoque des resultats auxquels on ne s'attend pas parmi les états quantiques possibles (dans l'histogramme pour l'ordinateur quantique, cela correspond aux états `01` et `10` lors de l'exécution avec un hardware quantique).

Résultats dans un simulateur (ex03) | Résultats avec un ordinateur quantique (ex04)
:-------------:|:-------------:
![entanglement](data/img/entanglement.png) | ![quantum noise](data/img/quantum_noise.png)

> “The main source of failure in a quantum computer is noise, which comes from rogue forms of energy creeping into the quantum computer making the qubits drift away from where they should be and causing errors.” https://www.youtube.com/watch?v=-UlxHPIEVqA&t=1400s

<hr>

Le circuit doit être optimisé pour le backend sur lequel le programme va être run.

Les backends disponibles ne supportent pas forcement les mêmes configurations, certaines portes et le circuit doit ainsi être *transpilé*.
Cela permet aussi d’optimiser le circuit afin de réduire le nombre d’instructions qui seront exécutées sur l’ordinateur quantique.

Le backend possède ainsi une *Instruction Set Architecture* (ISA), un set d’instructions que ce backend peut comprendre et exécuté. Un circuit exécuté sur un backend doit se conformer à l’ISA de ce backend.

<hr>

Ce qui est retourné par `sampler.run()` est un [`RuntimeJobV2`](https://docs.quantum.ibm.com/api/qiskit-ibm-runtime/qiskit_ibm_runtime.RuntimeJobV2). Certaines méthodes intéressantes: `job_id()`, `status()` et `metrics()` (données sur le temps d’exécution, version des dépendances …).

Ce qui est retourné par `job.result()` où `job` est un `RuntimeJobV2` est un tableau de [`PrimitiveResult`](https://docs.quantum.ibm.com/api/qiskit/qiskit.primitives.PrimitiveResult) avec selon l’index le job correspondant qui à été exécuté.
Sera à `[0]` comme on lance qu’un circuit à la fois et vu les programmes que l’on va faire, l’attribut `metadata` sera souvent vide.
Dans `data` on a le circuit classique où les résultats des mesures ont été mises, ce circuit est appelé par défaut `meas` lorsqu’on utilise `measure_all()`. Dans ce `meas` on a un [`BitArray`](https://docs.quantum.ibm.com/api/qiskit/qiskit.primitives.BitArray) dont la méthode `get_counts` permet d’avoir les résultats en un dictionnaire.

<details>
  <summary>Sources</summary>

  [How to sample a Bell State using Qiskit | Qiskit Youtube](https://www.youtube.com/watch?v=9MOIBcYf9wk)

  [What are ISA circuits? | IBM Quantum Blog](https://www.ibm.com/quantum/blog/isa-circuits)
</details>

## Exercice 5: Deutsch-Jozsa

Dans les schémas d’exemple du [sujet](data/fr.subject.pdf) (page 9):

- les carrés avec le 'X' correspondent à des gates X

- le cercle avec le '+' $\oplus$ et un point sur un autre qubit correspondent aux CNOT gates. Le qubit où le cercle avec le ‘+’ à le rôle de contrôleur et le qubit avec le point est la target de cette gate.

  Dans le circuit d'Oracle Balanced: $q_3$ à une gate CNOT dont la target est $q_0$, une autre pour $q_1$ et la dernière pour $q_2$.

L’oracle *balanced* sortira toujours `111` comme états finaux pour q_0, q_1 et q_2, des CNOT et X gates sont présentes sur les trois qubits d’input.

L’oracle *constant* sortira toujours `000` comme états finaux pour q_0, q_1 et q_2 comme il n’y a pas de gates sur ces qubits d’input.

Dans mon code:
- Les fonctions *balanced* qui sont créées par `create_new_oracle_function()` pourront avoir des états à 0 et d’autres à 1 comme certains des qubits n’auront pas les mêmes portes appliquées, e.g. `010`, `100` … Dès qu’il y aura un `1` pour l’un des états alors la fonction est *balanced*.

<hr>

### Algorithme de Deutsch-Jozsa

Le Problème de Deutsch-Jozsa:
<hr>

On a une boîte noire quantique, appelé *oracle* qui implémente une fonction booléenne $f: \{0,1\}^n → \{0,1\}$, i.e. pour tout input $0$ ou $1$ où $n$ est le nombre de bits dans l'input, le résultat de la fonction sera toujours $0$ ou $1$, les proportions de sorties de ces possibilités est déterminé par le type de la fonction.

La fonction est *constante*, le résultat est $0$ ou $1$ pour toutes les entrées ou *équilibrée*, le résultat est équilibré entre $0$ et $1$ (moitié des cas 0, l’autre moitié 1).

Le but du problème est de déterminer si la fonction est *constante* ou *équilibrée* à l’aide de l’oracle.

La solution déterministe (avec des moyens classiques) à ce problème nécessite de faire $2^{n-1} + 1$ évaluations (tester la moitié des $2^n$ entrées possibles plus une) de la fonction $f$ dans le pire des cas pour trouver la solution.

L’algorithme quantique de Deutsch-Jozsa permet de déterminer le type de la fonction $f$ en une seule évaluation de celle-ci. Le speedup par rapport à la résolution classique est quadratique.

Cet algorithme quantique illustre l’utilisation de quantum parallelism ainsi que l’interférence quantique.

<hr>

Les étapes de l’algorithme, pour correspondre au sujet (4 qubits):

1. Avoir deux registres quantiques (registre composé de plusieurs qubits) initialisé à 0. Le premier est un registre ayant 3 qubit qui sont utilisés pour faire des requêtes à l’oracle (input), le second registre est un registre d’1 qubit qui stocke la réponse de l’oracle (output).

    L’état du premier registre: $\ket{000}$

    L’état du second registre: $\ket{0}$

2. Créer une superposition pour tout les qubits d’input du premier registre en appliquant une porte d’Hadamard à chaque qubit.
    - l’état

        $$
        H^{\otimes3}\ket{000}\ket{0}=\frac{1}{\sqrt{2^3}}\sum_{\substack{i=0}}^{2^3-1}{\ket{i}\ket{0}}
        $$

3. Retourne le deuxième registre et applique la porte d’Hadamard. C’est pour stocker la réponse de l’oracle dans la phase.
    - l’état

        $$
        \frac{1}{\sqrt{2^3}}\sum_{\substack{i=0}}^{2^3-1}{\ket{i}\ket{0}} \rightarrow \frac{1}{\sqrt{2^{3+1}}}\sum_{\substack{i=0}}^{2^3-1}\ket{i}(\ket{0}-\ket{1})
        $$

4. Query l’oracle
    - l’état

        $$
        \frac{1}{\sqrt{2^{3+1}}}\sum_{\substack{i=0}}^{2^3-1}\ket{i}(\ket{0}-\ket{1}) \rightarrow \frac{1}{\sqrt{2^{3+1}}}\sum_{\substack{i=0}}^{2^3-1}(-1)^{f(i)}\ket{i}(\ket{0}-\ket{1})
        $$

5. Applique la porte d’Hadamard sur le premier registre
6. Mesure le premier registre, si c’est ≠ 0 alors la fonction est balanced, sinon la fonction est constante.

Quand la fonction $f$ est constante, les états quantiques avant et après la query à l’oracle sont les mêmes. L’inverse de la porte d’Hadamard est la porte d’Hadamard elle-même. À l’étape 5., on fait l’opération inverse de celle faite à la 2. pour obtenir l’état quantique initial de tout à 0 pour le premier registre.

Quand la fonction $f$ est balanced, l’état quantique après la query à l’oracle est orthogonal à l’état quantique d’avant la query à l’oracle. À l’étape 5., quand on fait l’opération inverse, on devrait se retrouver avec un état quantique qui est orthogoné à l’état quantique initial de tout à 0 du premier registre. On ne devrait jamais obtenir l’état tout à 0.

Si on run l’algo sur un vrai ordinateur et non un simulateur, on va se retrouver avec du bruit. On ne pourra pas obtenir le type d’oracle avec certitude, contrairement à l’exécution sur simulateur.

Quand on lance le programme avec un simulateur, peu importe le nombre de `shots`, on va toujours avoir les mêmes résultats, `000` pour une fonction *constant* et `111` pour une *balanced*.

Avec un hardware, le bruit sa provoquer des états où pour certains résultats on va avoir des mélanges: `010`, `101` …

## Résultats

### Constant

Les qubits sont à `0` lorsque l'oracle est **constant**.

Résultats avec un simulateur | Résultats avec un ordinateur quantique
:-------------:|:-------------:
![Deutsch-Jozsa oracle constant résultats (simulateur)](data/img/deutsch_jozsa_constant_result_sim.png) | ![Deutsch-Jozsa oracle constant résultats (hardware)](data/img/deutsch_jozsa_constant_result.png)

### Balanced

Les qubits sont à `1` lorsque l'oracle est **balanced**.

Résultats avec un simulateur | Résultats avec un ordinateur quantique
:-------------:|:-------------:
![Deutsch-Jozsa oracle balanced résultats (simulateur)](data/img/deutsch_jozsa_balanced_result_sim.png) | ![Deutsch-Jozsa oracle balanced résultats (hardware)](data/img/deutsch_jozsa_balanced_result.png)


<details>
  <summary>Sources</summary>

  [Algorithme de Deutsch-Jozsa | Wikipedia](https://fr.wikipedia.org/wiki/Algorithme_de_Deutsch-Jozsa)

  [Deutsch-Jozsa Algorithm | Qiskit Tutorials](https://github.com/qiskit-community/qiskit-community-tutorials/blob/master/algorithms/deutsch_jozsa.ipynb)

  [Quantum query algorithms, the Deutsch-Jozsa Algorithm | Qiskit Learning](https://learning.quantum.ibm.com/course/fundamentals-of-quantum-algorithms/quantum-query-algorithms#the-deutsch-jozsa-algorithm)

  [QuantumCircuit.compose() | Qiskit Documentation](https://docs.quantum.ibm.com/api/qiskit/qiskit.circuit.QuantumCircuit#qiskit.circuit.QuantumCircuit.compose)

  [The Deutsch-Jozsa Algorithm — Math, Circuits, and Code | Medium](https://medium.com/quantum-untangled/the-deutsch-jozsa-algorithm-math-circuits-and-code-quantum-algorithms-untangled-f3b28be4cfd3)

</details>

## Exercice 6: Algorithme de recherche

De ce que je comprends de ce qui est demandé, cet exercice peut être une implémentation de l’algorithme de Grover.

<details>
  <summary>Sources</summary>

  [L'informatique quantique c'est simple en fait | Youtube](https://www.youtube.com/watch?v=wfXs7QXy4IU)

  [A Visual Introduction to Grover's Algorithm and Reflections | Gordon Ma Youtube](https://www.youtube.com/watch?v=c30KrWjHaw4)

  [Grover's Algorithm | Qiskit Textbook](https://github.com/Qiskit/textbook/blob/main/notebooks/ch-algorithms/grover.ipynb)

  [Grover's Algorithm | Qiskit Tutorials](https://github.com/Qiskit/qiskit-tutorials/blob/master/tutorials/algorithms/06_grover.ipynb)

  [Grover's Algorithm | IBM Quantum Learning](https://learning.quantum.ibm.com/tutorial/grovers-algorithm)

  [Algorithme de Grover | Wikipedia](https://fr.wikipedia.org/wiki/Algorithme_de_Grover)
</details>


# Documentation

## Mentionnées par le sujet

[La lévitation quantique - Julien Bobroff, à l'USI | Youtube](https://www.youtube.com/watch?v=6kg2yV_3B1Q)

[David Louapre Physique Quantique | Youtube](https://www.youtube.com/results?search_query=david+louapre+physique+quantique)

Vidéos interéssantes (There is more to explore here) sur le sujet de [David Louapre - ScienceEtonnante](https://www.youtube.com/@ScienceEtonnante)

  - [La mécanique quantique en 7 idées | Youtube](https://www.youtube.com/watch?v=Rj3jTw2DxXQ&pp=ygUlZGF2aWQgbG91YXByZSBwcm9ncmFtbWF0aW9uIHF1YW50aXF1ZQ==)

  - [La mécanique quantique [Vidéo]](https://scienceetonnante.com/2015/10/02/la-mecanique-quantique-video/)

  - [Les Ordinateurs Quantiques | Youtube](https://www.youtube.com/watch?v=bayTbt_8aNc)

  - [L'intrication quantique | Youtube](https://www.youtube.com/watch?v=5R6k2mEacZo)

  - [Les inégalités de BELL & les expériences d'Alain ASPECT | Youtube](https://www.youtube.com/watch?v=28UN70790Do)

  - [Les inégalités de Bell et les expériences d’Alain Aspect](https://scienceetonnante.com/2020/10/23/bell-aspect/)

  - [Alain Aspect : Intrication quantique et inégalités de Bell [Interview complète] | Youtube](https://www.youtube.com/watch?v=OeZ_63iKPho)

[Une brève histoire du temps: du big bang aux trous noirs - Stephen W. Hawking | Archive.org](https://archive.org/details/unebrevehistoire0000hawk_p0i8)

[L'univers à portée de main - Christophe Galfard | Anna's archive](https://annas-archive.org/md5/841df5dfbae95a35308591344058e517)

## Divers

[L'informatique quantique, c'est simple, en fait. - V2F | Youtube](https://www.youtube.com/watch?v=wfXs7QXy4IU)

[Understanding Superposition Physically and Mathematically in Classical and Quantum Physics](https://www.physicsforums.com/insights/understanding-superposition/)

[LinuxFoundationX: Introduction to Quantum Circuits](https://www.edx.org/learn/quantum-computing/the-linux-foundation-introduction-to-quantum-circuits?webview=false&campaign=Introduction+to+Quantum+Circuits&source=edx&product_category=course&placement_url=https://www.edx.org/school/linuxfoundationx)

[What is Quantum Computing? | IBM](https://www.ibm.com/topics/quantum-computing)

[Quantum Computing Stack Exchange](https://quantumcomputing.stackexchange.com/)

[FLP Vol. III Table of Contents](https://www.feynmanlectures.caltech.edu/III_toc.html)

[Photons Jumeaux | Youtube Channel](https://www.youtube.com/@photonsjumeaux4395/videos)

[Qiskit | Slack](https://qiskit.enterprise.slack.com)

[Qiskit | Youtube](https://www.youtube.com/@qiskit)

[IBM Quantum Documentation](https://docs.quantum.ibm.com/)

[Qiskit | IBM Quantum Computing](https://www.ibm.com/quantum/qiskit)

[qiskit | IBM Quantum Documentation](https://docs.quantum.ibm.com/api/qiskit)

[qiskit-community-tutorials | github](https://github.com/qiskit-community/qiskit-community-tutorials)

[Basics of Quantum Information | IBM Quantum Learning](https://learning.quantum.ibm.com/course/basics-of-quantum-information)

[Fundamentals of Quantum Algorithms | IBM Quantum Learning](https://learning.quantum.ibm.com/course/fundamentals-of-quantum-algorithms)

[The Map of Quantum Computing - Quantum Computing Explained](https://www.youtube.com/watch?v=-UlxHPIEVqA) ->  https://www.flickr.com/photos/95869671@N08/51721957923/

[Who Has The Best Quantum Computer? - Domain of Science | Youtube](https://www.youtube.com/watch?v=gcbMKt079l8)

[Quantum Computing - Domain of Science | Youtube](https://www.youtube.com/watch?v=VyX8E4KUkWw)

[Understanding Quantum Mechanics - Sabine Hossenfelder | Youtube Playlist](https://www.youtube.com/playlist?list=PLwgQsqtH9H5djIfFhXE6We207beTgUnyL)

[Introduction to Quantum Computing and Quantum Hardware - Qiskit | Youtube Playlist](https://www.youtube.com/playlist?list=PLOFEBzvs-VvrXTMy5Y2IqmSaUjfnhvBHR)
