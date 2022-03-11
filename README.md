# qiskit-qir

Qiskit to QIR translator.

## Example

```python
from qiskit import QuantumCircuit
from qiskit_qir import to_qir

circuit = QuantumCircuit(3, 3, name="my-circuit")
circuit.h(0)
circuit.cx(0, 1)
circuit.cx(1, 2)
circuit.measure([0,1,2], [0, 1, 2])

qir = to_qir(circuit)
```

## Development

### Install from source

To install the package from source, clone the repo onto your machine, browse to `qdk-python/qiskit-qir` and run

```bash
pip install -e .
```

### Tests

First, install the development dependencies using

```bash
pip install -r requirements_dev.txt
```

To run the tests in your local environment, run

```bash
make test
```

To run the tests in virtual environments on supported Python versions, run

```bash
make test-all
```

### Docs

To build the docs using Sphinx, run

```bash
make docs
```
