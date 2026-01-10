#!/usr/bin/env python3
"""
Neural Network Implementation

Implements a feedforward neural network with backpropagation for
classification and regression tasks.

Features:
- Configurable architecture (layers and neurons)
- Multiple activation functions (ReLU, sigmoid, tanh, softmax)
- Various optimizers (SGD, momentum, Adam)
- L2 regularization and dropout
- Mini-batch training
- Early stopping

Author: Algorithms Multiverse
License: MIT
"""

import numpy as np
from typing import List, Tuple, Optional, Callable, Dict
import warnings
from collections import defaultdict


class Activation:
    """Activation functions and their derivatives."""

    @staticmethod
    def sigmoid(x: np.ndarray) -> np.ndarray:
        """Sigmoid activation function."""
        # Clip to prevent overflow
        x = np.clip(x, -500, 500)
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def sigmoid_derivative(x: np.ndarray) -> np.ndarray:
        """Derivative of sigmoid function."""
        s = Activation.sigmoid(x)
        return s * (1 - s)

    @staticmethod
    def tanh(x: np.ndarray) -> np.ndarray:
        """Hyperbolic tangent activation function."""
        return np.tanh(x)

    @staticmethod
    def tanh_derivative(x: np.ndarray) -> np.ndarray:
        """Derivative of tanh function."""
        return 1 - np.tanh(x) ** 2

    @staticmethod
    def relu(x: np.ndarray) -> np.ndarray:
        """ReLU activation function."""
        return np.maximum(0, x)

    @staticmethod
    def relu_derivative(x: np.ndarray) -> np.ndarray:
        """Derivative of ReLU function."""
        return (x > 0).astype(float)

    @staticmethod
    def leaky_relu(x: np.ndarray, alpha: float = 0.01) -> np.ndarray:
        """Leaky ReLU activation function."""
        return np.where(x > 0, x, alpha * x)

    @staticmethod
    def leaky_relu_derivative(x: np.ndarray, alpha: float = 0.01) -> np.ndarray:
        """Derivative of Leaky ReLU function."""
        return np.where(x > 0, 1, alpha)

    @staticmethod
    def softmax(x: np.ndarray) -> np.ndarray:
        """Softmax activation function for multi-class classification."""
        # Subtract max for numerical stability
        exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

    @staticmethod
    def linear(x: np.ndarray) -> np.ndarray:
        """Linear activation (identity function)."""
        return x

    @staticmethod
    def linear_derivative(x: np.ndarray) -> np.ndarray:
        """Derivative of linear activation."""
        return np.ones_like(x)


class Layer:
    """A single layer in the neural network."""

    def __init__(self,
                 input_size: int,
                 output_size: int,
                 activation: str = 'relu',
                 dropout_rate: float = 0.0):
        """
        Initialize a layer.

        Args:
            input_size: Number of input features
            output_size: Number of neurons in this layer
            activation: Activation function name
            dropout_rate: Dropout rate for regularization
        """
        self.input_size = input_size
        self.output_size = output_size
        self.activation_name = activation
        self.dropout_rate = dropout_rate

        # Initialize weights using He/Xavier initialization
        if activation in ['relu', 'leaky_relu']:
            # He initialization for ReLU
            self.weights = np.random.randn(input_size, output_size) * np.sqrt(2 / input_size)
        else:
            # Xavier initialization for sigmoid/tanh
            self.weights = np.random.randn(input_size, output_size) * np.sqrt(1 / input_size)

        self.biases = np.zeros((1, output_size))

        # Set activation functions
        self._set_activation_functions()

        # For storing intermediate values during forward pass
        self.input = None
        self.output = None
        self.z = None  # Pre-activation values
        self.dropout_mask = None

        # For storing gradients
        self.weights_grad = None
        self.biases_grad = None

    def _set_activation_functions(self):
        """Set activation and derivative functions based on name."""
        activations = {
            'sigmoid': (Activation.sigmoid, Activation.sigmoid_derivative),
            'tanh': (Activation.tanh, Activation.tanh_derivative),
            'relu': (Activation.relu, Activation.relu_derivative),
            'leaky_relu': (Activation.leaky_relu, Activation.leaky_relu_derivative),
            'softmax': (Activation.softmax, None),  # Softmax derivative handled separately
            'linear': (Activation.linear, Activation.linear_derivative)
        }

        if self.activation_name not in activations:
            raise ValueError(f"Unknown activation: {self.activation_name}")

        self.activation, self.activation_derivative = activations[self.activation_name]

    def forward(self, input_data: np.ndarray, training: bool = True) -> np.ndarray:
        """
        Forward pass through the layer.

        Args:
            input_data: Input to the layer
            training: Whether in training mode (applies dropout)

        Returns:
            Output of the layer
        """
        self.input = input_data
        self.z = np.dot(input_data, self.weights) + self.biases

        if self.activation_name == 'softmax':
            self.output = self.activation(self.z)
        else:
            self.output = self.activation(self.z)

        # Apply dropout during training
        if training and self.dropout_rate > 0:
            self.dropout_mask = np.random.binomial(1, 1 - self.dropout_rate,
                                                  size=self.output.shape)
            self.output *= self.dropout_mask / (1 - self.dropout_rate)
        else:
            self.dropout_mask = None

        return self.output

    def backward(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        """
        Backward pass through the layer.

        Args:
            output_gradient: Gradient from the next layer
            learning_rate: Learning rate for weight updates

        Returns:
            Gradient to pass to the previous layer
        """
        # Apply dropout mask if it was used in forward pass
        if self.dropout_mask is not None:
            output_gradient *= self.dropout_mask / (1 - self.dropout_rate)

        # Calculate gradient w.r.t pre-activation
        if self.activation_name == 'softmax':
            # Softmax gradient is handled differently (combined with cross-entropy)
            z_gradient = output_gradient
        else:
            z_gradient = output_gradient * self.activation_derivative(self.z)

        # Calculate gradients for weights and biases
        self.weights_grad = np.dot(self.input.T, z_gradient) / self.input.shape[0]
        self.biases_grad = np.mean(z_gradient, axis=0, keepdims=True)

        # Calculate gradient to pass to previous layer
        input_gradient = np.dot(z_gradient, self.weights.T)

        return input_gradient


class NeuralNetwork:
    """
    Feedforward neural network with backpropagation.

    Supports multiple hidden layers, various activation functions,
    and different optimization algorithms.
    """

    def __init__(self,
                 layer_sizes: List[int],
                 activations: Optional[List[str]] = None,
                 learning_rate: float = 0.01,
                 optimizer: str = 'adam',
                 regularization: float = 0.0,
                 dropout: float = 0.0,
                 batch_size: int = 32,
                 epochs: int = 100,
                 early_stopping: bool = False,
                 patience: int = 10,
                 verbose: bool = False,
                 random_state: Optional[int] = None):
        """
        Initialize neural network.

        Args:
            layer_sizes: List of layer sizes [input_size, hidden1, hidden2, ..., output_size]
            activations: Activation functions for each layer (excluding input)
            learning_rate: Learning rate for training
            optimizer: Optimizer type ('sgd', 'momentum', 'adam')
            regularization: L2 regularization parameter
            dropout: Dropout rate for hidden layers
            batch_size: Mini-batch size
            epochs: Number of training epochs
            early_stopping: Whether to use early stopping
            patience: Patience for early stopping
            verbose: Whether to print training progress
            random_state: Random seed for reproducibility
        """
        self.layer_sizes = layer_sizes
        self.learning_rate = learning_rate
        self.optimizer = optimizer
        self.regularization = regularization
        self.dropout = dropout
        self.batch_size = batch_size
        self.epochs = epochs
        self.early_stopping = early_stopping
        self.patience = patience
        self.verbose = verbose
        self.random_state = random_state

        # Set random seed
        if random_state is not None:
            np.random.seed(random_state)

        # Set default activations if not provided
        if activations is None:
            # Default: ReLU for hidden layers, sigmoid/softmax for output
            n_layers = len(layer_sizes) - 1
            activations = ['relu'] * (n_layers - 1)
            # Output activation based on output size
            if layer_sizes[-1] == 1:
                activations.append('sigmoid')  # Binary classification or regression
            elif layer_sizes[-1] > 1:
                activations.append('softmax')  # Multi-class classification
            else:
                activations.append('linear')  # Regression

        self.activations = activations

        # Initialize layers
        self.layers = []
        for i in range(len(layer_sizes) - 1):
            # Apply dropout only to hidden layers, not output
            dropout_rate = dropout if i < len(layer_sizes) - 2 else 0.0

            layer = Layer(
                input_size=layer_sizes[i],
                output_size=layer_sizes[i + 1],
                activation=activations[i],
                dropout_rate=dropout_rate
            )
            self.layers.append(layer)

        # Initialize optimizer parameters
        self._init_optimizer()

        # Training history
        self.history = {
            'loss': [],
            'val_loss': [],
            'accuracy': [],
            'val_accuracy': []
        }

    def _init_optimizer(self):
        """Initialize optimizer-specific parameters."""
        if self.optimizer == 'momentum':
            self.momentum = 0.9
            self.velocities = []
            for layer in self.layers:
                self.velocities.append({
                    'weights': np.zeros_like(layer.weights),
                    'biases': np.zeros_like(layer.biases)
                })

        elif self.optimizer == 'adam':
            self.beta1 = 0.9
            self.beta2 = 0.999
            self.epsilon = 1e-8
            self.m = []  # First moment
            self.v = []  # Second moment
            self.t = 0   # Time step

            for layer in self.layers:
                self.m.append({
                    'weights': np.zeros_like(layer.weights),
                    'biases': np.zeros_like(layer.biases)
                })
                self.v.append({
                    'weights': np.zeros_like(layer.weights),
                    'biases': np.zeros_like(layer.biases)
                })

    def forward(self, X: np.ndarray, training: bool = True) -> np.ndarray:
        """
        Forward pass through the network.

        Args:
            X: Input data
            training: Whether in training mode

        Returns:
            Output of the network
        """
        output = X
        for layer in self.layers:
            output = layer.forward(output, training=training)
        return output

    def backward(self, X: np.ndarray, y: np.ndarray) -> float:
        """
        Backward pass through the network.

        Args:
            X: Input data
            y: True labels

        Returns:
            Loss value
        """
        # Forward pass
        predictions = self.forward(X, training=True)

        # Calculate loss and initial gradient
        loss, grad = self._calculate_loss_and_gradient(predictions, y)

        # Add L2 regularization to loss
        if self.regularization > 0:
            for layer in self.layers:
                loss += 0.5 * self.regularization * np.sum(layer.weights ** 2)

        # Backward pass through layers
        for i in range(len(self.layers) - 1, -1, -1):
            grad = self.layers[i].backward(grad, self.learning_rate)

        # Update weights using optimizer
        self._update_weights()

        return loss

    def _calculate_loss_and_gradient(self, predictions: np.ndarray,
                                    y: np.ndarray) -> Tuple[float, np.ndarray]:
        """
        Calculate loss and initial gradient for backpropagation.

        Args:
            predictions: Network predictions
            y: True labels

        Returns:
            Loss value and gradient
        """
        n_samples = y.shape[0]

        # Check if this is classification or regression
        if self.layers[-1].activation_name == 'softmax':
            # Multi-class classification with cross-entropy loss
            # Convert y to one-hot if needed
            if len(y.shape) == 1:
                y_one_hot = np.zeros((n_samples, self.layer_sizes[-1]))
                y_one_hot[np.arange(n_samples), y.astype(int)] = 1
                y = y_one_hot

            # Cross-entropy loss
            epsilon = 1e-10
            loss = -np.sum(y * np.log(predictions + epsilon)) / n_samples

            # Gradient for softmax + cross-entropy
            grad = predictions - y

        elif self.layers[-1].activation_name == 'sigmoid':
            # Binary classification with binary cross-entropy
            epsilon = 1e-10
            predictions = np.clip(predictions, epsilon, 1 - epsilon)
            loss = -np.mean(y * np.log(predictions) + (1 - y) * np.log(1 - predictions))

            # Gradient
            grad = (predictions - y) / n_samples

        else:
            # Regression with MSE loss
            loss = np.mean((predictions - y) ** 2) / 2
            grad = (predictions - y) / n_samples

        return loss, grad

    def _update_weights(self):
        """Update weights using the specified optimizer."""
        for i, layer in enumerate(self.layers):
            # Add L2 regularization to gradients
            if self.regularization > 0:
                layer.weights_grad += self.regularization * layer.weights

            if self.optimizer == 'sgd':
                # Standard SGD
                layer.weights -= self.learning_rate * layer.weights_grad
                layer.biases -= self.learning_rate * layer.biases_grad

            elif self.optimizer == 'momentum':
                # SGD with momentum
                self.velocities[i]['weights'] = (self.momentum * self.velocities[i]['weights'] -
                                                self.learning_rate * layer.weights_grad)
                self.velocities[i]['biases'] = (self.momentum * self.velocities[i]['biases'] -
                                               self.learning_rate * layer.biases_grad)

                layer.weights += self.velocities[i]['weights']
                layer.biases += self.velocities[i]['biases']

            elif self.optimizer == 'adam':
                # Adam optimizer
                self.t += 1

                # Update biased first moment
                self.m[i]['weights'] = (self.beta1 * self.m[i]['weights'] +
                                       (1 - self.beta1) * layer.weights_grad)
                self.m[i]['biases'] = (self.beta1 * self.m[i]['biases'] +
                                      (1 - self.beta1) * layer.biases_grad)

                # Update biased second moment
                self.v[i]['weights'] = (self.beta2 * self.v[i]['weights'] +
                                       (1 - self.beta2) * layer.weights_grad ** 2)
                self.v[i]['biases'] = (self.beta2 * self.v[i]['biases'] +
                                      (1 - self.beta2) * layer.biases_grad ** 2)

                # Bias correction
                m_hat_w = self.m[i]['weights'] / (1 - self.beta1 ** self.t)
                m_hat_b = self.m[i]['biases'] / (1 - self.beta1 ** self.t)
                v_hat_w = self.v[i]['weights'] / (1 - self.beta2 ** self.t)
                v_hat_b = self.v[i]['biases'] / (1 - self.beta2 ** self.t)

                # Update weights
                layer.weights -= self.learning_rate * m_hat_w / (np.sqrt(v_hat_w) + self.epsilon)
                layer.biases -= self.learning_rate * m_hat_b / (np.sqrt(v_hat_b) + self.epsilon)

    def fit(self, X: np.ndarray, y: np.ndarray,
            X_val: Optional[np.ndarray] = None,
            y_val: Optional[np.ndarray] = None) -> 'NeuralNetwork':
        """
        Train the neural network.

        Args:
            X: Training features
            y: Training labels
            X_val: Validation features (optional)
            y_val: Validation labels (optional)

        Returns:
            Self for method chaining
        """
        X = np.asarray(X)
        y = np.asarray(y)

        n_samples = X.shape[0]
        best_val_loss = np.inf
        patience_counter = 0

        for epoch in range(self.epochs):
            # Shuffle data
            indices = np.random.permutation(n_samples)
            X_shuffled = X[indices]
            y_shuffled = y[indices]

            # Mini-batch training
            epoch_loss = 0
            n_batches = 0

            for i in range(0, n_samples, self.batch_size):
                batch_X = X_shuffled[i:i + self.batch_size]
                batch_y = y_shuffled[i:i + self.batch_size]

                loss = self.backward(batch_X, batch_y)
                epoch_loss += loss
                n_batches += 1

            avg_loss = epoch_loss / n_batches
            self.history['loss'].append(avg_loss)

            # Validation
            if X_val is not None and y_val is not None:
                val_predictions = self.predict_proba(X_val) if self.layers[-1].activation_name == 'softmax' \
                                else self.predict(X_val)
                val_loss, _ = self._calculate_loss_and_gradient(val_predictions, y_val)
                self.history['val_loss'].append(val_loss)

                # Early stopping
                if self.early_stopping:
                    if val_loss < best_val_loss:
                        best_val_loss = val_loss
                        patience_counter = 0
                    else:
                        patience_counter += 1

                    if patience_counter >= self.patience:
                        if self.verbose:
                            print(f"Early stopping at epoch {epoch + 1}")
                        break

            # Print progress
            if self.verbose and (epoch + 1) % 10 == 0:
                msg = f"Epoch {epoch + 1}/{self.epochs} - Loss: {avg_loss:.4f}"
                if X_val is not None:
                    msg += f" - Val Loss: {val_loss:.4f}"
                print(msg)

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions for input data.

        Args:
            X: Input features

        Returns:
            Predictions (class labels for classification, values for regression)
        """
        X = np.asarray(X)
        predictions = self.forward(X, training=False)

        if self.layers[-1].activation_name == 'softmax':
            # Return class labels for multi-class classification
            return np.argmax(predictions, axis=1)
        elif self.layers[-1].activation_name == 'sigmoid':
            # Return binary labels
            return (predictions > 0.5).astype(int).flatten()
        else:
            # Return regression values
            return predictions.flatten()

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """
        Predict class probabilities.

        Args:
            X: Input features

        Returns:
            Class probabilities
        """
        X = np.asarray(X)
        return self.forward(X, training=False)

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """
        Calculate accuracy (classification) or R² score (regression).

        Args:
            X: Features
            y: True labels

        Returns:
            Accuracy or R² score
        """
        predictions = self.predict(X)

        if self.layers[-1].activation_name in ['softmax', 'sigmoid']:
            # Classification accuracy
            return np.mean(predictions == y)
        else:
            # Regression R² score
            ss_res = np.sum((y - predictions) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            return 1 - (ss_res / ss_tot) if ss_tot != 0 else 0.0


def create_classification_data(n_samples: int = 200,
                              n_features: int = 2,
                              n_classes: int = 2,
                              random_state: Optional[int] = None) -> Tuple[np.ndarray, np.ndarray]:
    """Create synthetic classification data."""
    np.random.seed(random_state)

    X = np.random.randn(n_samples, n_features)

    if n_classes == 2:
        # Binary classification (XOR-like problem)
        y = ((X[:, 0] > 0) != (X[:, 1] > 0)).astype(int)
    else:
        # Multi-class (radial pattern)
        distances = np.sqrt(np.sum(X ** 2, axis=1))
        y = (distances * n_classes / 3).astype(int)
        y = np.clip(y, 0, n_classes - 1)

    return X, y


def demonstrate_neural_network():
    """Demonstrate neural network capabilities."""
    print("=" * 60)
    print("Neural Network Demonstration")
    print("=" * 60)

    # 1. Binary Classification (XOR problem)
    print("\n1. Binary Classification (XOR Problem)")
    print("-" * 40)

    X_binary, y_binary = create_classification_data(
        n_samples=200, n_features=2, n_classes=2, random_state=42
    )

    # Split data
    n_train = 150
    X_train, X_test = X_binary[:n_train], X_binary[n_train:]
    y_train, y_test = y_binary[:n_train], y_binary[n_train:]

    # Create neural network
    nn_binary = NeuralNetwork(
        layer_sizes=[2, 8, 4, 1],  # 2 input, 2 hidden layers, 1 output
        activations=['relu', 'relu', 'sigmoid'],
        learning_rate=0.01,
        optimizer='adam',
        epochs=100,
        batch_size=32,
        verbose=True,
        random_state=42
    )

    nn_binary.fit(X_train, y_train)

    train_acc = nn_binary.score(X_train, y_train)
    test_acc = nn_binary.score(X_test, y_test)

    print(f"\nTraining accuracy: {train_acc:.3f}")
    print(f"Testing accuracy: {test_acc:.3f}")

    # 2. Multi-class Classification
    print("\n2. Multi-class Classification")
    print("-" * 40)

    X_multi, y_multi = create_classification_data(
        n_samples=300, n_features=2, n_classes=3, random_state=42
    )

    X_train, X_test = X_multi[:250], X_multi[250:]
    y_train, y_test = y_multi[:250], y_multi[250:]

    nn_multi = NeuralNetwork(
        layer_sizes=[2, 16, 8, 3],  # 3 output neurons for 3 classes
        activations=['relu', 'relu', 'softmax'],
        learning_rate=0.01,
        optimizer='adam',
        regularization=0.01,
        dropout=0.2,
        epochs=100,
        batch_size=32,
        random_state=42
    )

    nn_multi.fit(X_train, y_train)

    train_acc = nn_multi.score(X_train, y_train)
    test_acc = nn_multi.score(X_test, y_test)

    print(f"Training accuracy: {train_acc:.3f}")
    print(f"Testing accuracy: {test_acc:.3f}")

    # Get probability predictions
    proba = nn_multi.predict_proba(X_test[:5])
    print(f"\nSample probability predictions:")
    for i in range(5):
        print(f"  Sample {i+1}: {proba[i].round(3)}")

    # 3. Regression
    print("\n3. Regression Task")
    print("-" * 40)

    # Generate regression data
    X_reg = np.random.randn(200, 3)
    y_reg = X_reg[:, 0] ** 2 + 2 * X_reg[:, 1] - X_reg[:, 2] + 0.1 * np.random.randn(200)

    X_train, X_test = X_reg[:150], X_reg[150:]
    y_train, y_test = y_reg[:150], y_reg[150:]

    nn_reg = NeuralNetwork(
        layer_sizes=[3, 16, 8, 1],
        activations=['relu', 'relu', 'linear'],
        learning_rate=0.01,
        optimizer='adam',
        epochs=100,
        batch_size=32,
        random_state=42
    )

    nn_reg.fit(X_train, y_train)

    train_r2 = nn_reg.score(X_train, y_train)
    test_r2 = nn_reg.score(X_test, y_test)

    print(f"Training R² score: {train_r2:.3f}")
    print(f"Testing R² score: {test_r2:.3f}")

    # 4. Effect of network depth
    print("\n4. Effect of Network Depth")
    print("-" * 40)

    architectures = [
        ([2, 4, 1], "Shallow (1 hidden)"),
        ([2, 8, 4, 1], "Medium (2 hidden)"),
        ([2, 16, 8, 4, 1], "Deep (3 hidden)")
    ]

    for layers, name in architectures:
        nn = NeuralNetwork(
            layer_sizes=layers,
            learning_rate=0.01,
            optimizer='adam',
            epochs=50,
            random_state=42,
            verbose=False
        )
        nn.fit(X_train, y_train)
        acc = nn.score(X_test, y_test)
        print(f"{name:20s}: Accuracy = {acc:.3f}")

    # 5. Compare optimizers
    print("\n5. Optimizer Comparison")
    print("-" * 40)

    optimizers = ['sgd', 'momentum', 'adam']

    for opt in optimizers:
        nn = NeuralNetwork(
            layer_sizes=[2, 8, 4, 1],
            optimizer=opt,
            epochs=50,
            random_state=42,
            verbose=False
        )
        nn.fit(X_train, y_train)
        acc = nn.score(X_test, y_test)
        final_loss = nn.history['loss'][-1]
        print(f"{opt:10s}: Accuracy = {acc:.3f}, Final loss = {final_loss:.4f}")


if __name__ == "__main__":
    demonstrate_neural_network()