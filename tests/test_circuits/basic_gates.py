##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import pytest

from qiskit import QuantumCircuit
from . import custom_mx

# All of the following dictionaries map from the names of methods on Qiskit QuantumCircuit objects
# to the name of the equivalent pyqir BasicQisBuilder method

_zero_qubit_operations = {"barrier": "barrier"}

_one_qubit_gates = {
    "h": "h",
    "reset": "reset",
    "s": "s",
    "t": "t",
    "x": "x",
    "y": "y",
    "z": "z",
}

_adj_gates = {"sdg": "s", "tdg": "t"}

_measurements = {"measure": "mz", "measure_x": "mx"}

_delays = {"delay": "delay"}

_rotations = {"rx": "rx", "ry": "ry", "rz": "rz"}

_prepares = {
    "0": "prepare_z",
    "1": "prepare_z",
    "+": "prepare_x",
    "-": "prepare_x",
}

_two_qubit_gates = {"cx": "cnot", "cz": "cz", "swap": "swap"}

_three_qubit_gates = {"ccx": "ccx"}


def _fixture_name(s: str) -> str:
    return f"Fixture_{s}"


def _map_gate_name(gate: str) -> str:
    if gate in _one_qubit_gates:
        return _one_qubit_gates[gate]
    elif gate in _adj_gates:
        return _adj_gates[gate]
    elif gate in _measurements:
        return _measurements[gate]
    elif gate in _delays:
        return _delays[gate]
    elif gate in _rotations:
        return _rotations[gate]
    elif gate in _two_qubit_gates:
        return _two_qubit_gates[gate]
    elif gate in _three_qubit_gates:
        return _three_qubit_gates[gate]
    elif gate in _zero_qubit_operations:
        return _zero_qubit_operations[gate]
    elif gate in _prepares:
        return _prepares[gate]
    else:
        raise ValueError(f"Unknown Qiskit gate {gate}")


def _map_prepare_name(state: str) -> str:
    return _prepares[state]


def _generate_one_qubit_fixture(gate: str):
    @pytest.fixture()
    def test_fixture():
        circuit = QuantumCircuit(1)
        getattr(circuit, gate)(0)
        return _map_gate_name(gate), circuit

    return test_fixture


# Generate simple single-qubit gate fixtures
for gate in _one_qubit_gates.keys():
    name = _fixture_name(gate)
    locals()[name] = _generate_one_qubit_fixture(gate)

# Generate adjoint single-qubit gate fixtures
for gate in _adj_gates.keys():
    name = _fixture_name(gate)
    locals()[name] = _generate_one_qubit_fixture(gate)


def _generate_delay_gate_fixture(unit: str):
    @pytest.fixture()
    def test_fixture():
        circuit = QuantumCircuit(1)
        if unit == "dt":
            circuit.delay(1, 0, unit=unit)
        else:
            circuit.delay(0.5, 0, unit=unit)
        return _map_gate_name("delay"), unit, circuit

    return test_fixture


delay_tests = []
# Generate time param operation fixtures
for unit in {"s", "ms", "us", "ns", "ps", "dt"}:
    name = _fixture_name("delay_" + unit)
    delay_tests.append(name)
    locals()[name] = _generate_delay_gate_fixture(unit)


def _generate_prepare_fixture(state: str):
    @pytest.fixture()
    def test_fixture():
        circuit = QuantumCircuit(1)
        circuit.initialize(state, 0)
        return _map_prepare_name(state), state, circuit

    return test_fixture


prepare_tests = []
# Generate time param operation fixtures
for state in {"0", "1", "+", "-"}:
    name = _fixture_name("initialize_" + unit)
    prepare_tests.append(name)
    locals()[name] = _generate_prepare_fixture(state)


def _generate_rotation_fixture(gate: str):
    @pytest.fixture()
    def test_fixture():
        circuit = QuantumCircuit(1)
        getattr(circuit, gate)(0.5, 0)
        return _map_gate_name(gate), circuit

    return test_fixture


# Generate rotation gate fixtures
for gate in _rotations.keys():
    name = _fixture_name(gate)
    locals()[name] = _generate_rotation_fixture(gate)


def _generate_two_qubit_fixture(gate: str):
    @pytest.fixture()
    def test_fixture():
        circuit = QuantumCircuit(2)
        getattr(circuit, gate)(0, 1)
        return _map_gate_name(gate), circuit

    return test_fixture


# Generate double-qubit gate fixtures
for gate in _two_qubit_gates.keys():
    name = _fixture_name(gate)
    locals()[name] = _generate_two_qubit_fixture(gate)


def _generate_three_qubit_fixture(gate: str):
    @pytest.fixture()
    def test_fixture():
        circuit = QuantumCircuit(3)
        getattr(circuit, gate)(2, 0, 1)
        return _map_gate_name(gate), circuit

    return test_fixture


# Generate three-qubit gate fixtures
for gate in _three_qubit_gates.keys():
    name = _fixture_name(gate)
    locals()[name] = _generate_three_qubit_fixture(gate)


def _generate_measurement_fixture(gate: str):
    @pytest.fixture()
    def test_fixture():
        circuit = QuantumCircuit(1, 1)
        getattr(circuit, gate)(0, 0)
        return _map_gate_name(gate), circuit

    return test_fixture


# Generate measurement fixtures
for gate in _measurements.keys():
    name = _fixture_name(gate)
    locals()[name] = _generate_measurement_fixture(gate)

single_op_tests = [_fixture_name(s) for s in _one_qubit_gates.keys()]
adj_op_tests = [_fixture_name(s) for s in _adj_gates.keys()]
rotation_tests = [_fixture_name(s) for s in _rotations.keys()]
double_op_tests = [_fixture_name(s) for s in _two_qubit_gates.keys()]
triple_op_tests = [_fixture_name(s) for s in _three_qubit_gates.keys()]
measurement_tests = [_fixture_name(s) for s in _measurements.keys()]
