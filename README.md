# ftl_quantum branch qiskit_pre_0.40.0

The subject of the first exercice: Token asks us to use the `IBMQ.get_provider()` function to get info on simulated and real quantum computers. However the `IBMQ` object, part of the package `qiskit-ibmq-provider` (https://github.com/Qiskit/qiskit-ibmq-provider) is deprecated.

So in this branch I tried to install a previous version of qiskit to use `IBMQ.get_provider()` but still can't make it for it to work.

I get the following error: cannot import name 'IBMQ' from partially initialized module 'qiskit’.

# sources for deprecation
- https://github.com/Qiskit/qiskit-ibmq-provider
- https://medium.com/qiskit/release-news-qiskit-v0-40-is-here-cdcdc8d400d4
- https://docs.quantum.ibm.com/api/migration-guides/qiskit-runtime-from-ibmq-provider
- https://quantumcomputing.stackexchange.com/questions/37042/ibmq-import-error