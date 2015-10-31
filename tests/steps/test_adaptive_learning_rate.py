from functools import partial

import numpy as np

from neupy import algorithms, layers

from base import BaseTestCase
from utils import compare_networks


even_input_train = np.array([[1, 2], [2, 1], [3, 1], [5, 1], [1, 6]])
even_target_train = np.array([[-1], [-1], [1], [1], [-1]])


class LeakStepAdaptationTestCase(BaseTestCase):
    def test_adaptive_learning_rate(self):
        network_default_error, network_tested_error = compare_networks(
            # Test classes
            algorithms.Backpropagation,
            partial(
                algorithms.Backpropagation,
                # Adaptive learning rate settings
                leak_size=0.5,
                alpha=0.5,
                beta=0.5,
                optimizations=[algorithms.LeakStepAdaptation]
            ),
            # Test data
            (even_input_train, even_target_train),
            # Network configurations
            connection=[
                layers.SigmoidLayer(2),
                layers.TanhLayer(3),
                layers.OutputLayer(1)
            ],
            step=0.1,
            shuffle_data=True,
            # Adaptive learning rate parameters
            # Test configurations
            epochs=30,
            # is_comparison_plot=True,
        )
        self.assertGreater(network_default_error, network_tested_error)
