# ftl_quantum

_You can read this in [french](README.fr.md)_

My version of the project requires an `.env` file.

It contains a `TOKEN` field, whose value is your IMBQ API token, which you can obtain from https://quantum.ibm.com/

```
TOKEN=Your token ...
```

## Exercice 1: Token
The subject for this exercice asked the following:
> By using the IBMQ.get_provider function, write a program that will have to:
>
    > - List all available quantum simulators with their current queue.
    > - List all available quantum computers with their current queue and the number of qubits they have.

The function `IBMQ.get_provider()` and the object `IBMQ` are deprecated since the version 0.40.0 of the package `qiskit-ibmq-provider` and 0.20.0 of Qiskit. They were deleted with the version 1.0.0 of Qiskit.

I attempted to create an environment with a previous version of Qiskit but I was not able to make it work. See the dedicated branch if you're interested: https://github.com/Killian-Morin/ftl_quantum/tree/qiskit_pre_0.40.0

sources for the deprecation
- https://github.com/Qiskit/qiskit-ibmq-provider
- https://github.com/Qiskit/qiskit/blob/d86f9958516ee7f48359ddc7364050bb791602d1/releasenotes/notes/1.0/remove-ibmq-4bb57a04991da9af.yaml#L4
- https://medium.com/qiskit/release-news-qiskit-v0-40-is-here-cdcdc8d400d4
- https://docs.quantum.ibm.com/api/migration-guides/qiskit-runtime-from-ibmq-provider -> migration guide to replace `IBMQ.get_provider()`
- https://quantumcomputing.stackexchange.com/questions/37042/ibmq-import-error

## Exercice 2: Superposition
The state to create in this exercice is the following: $\frac{1}{\sqrt{2}}(\ket{0}+\ket{1})$.

This state is the 'plus' state, $\ket{+}$.

It can also be written as $\frac{1}{\sqrt{2}}\ket{0}+\frac{1}{\sqrt{2}}\ket{1}$.

This state has an equal superposition of $\ket{0}$ and $\ket{1}$. The factors $\alpha$ and $\beta$ each has a value of $\frac{1}{\sqrt{2}}$. The coordinates for the 'plus' state on the [Bloch Sphere](https://en.wikipedia.org/wiki/Bloch_sphere) are (1, 0, 0).
