"""
===============================================================================
Probability of Default (PD) Model
===============================================================================

This module implements an educational Probability of Default model
using Logistic Regression.

The module is responsible for:

    1. Generating a synthetic default target.
    2. Preparing customer features.
    3. Training a Logistic Regression model.
    4. Estimating Probability of Default (PD).
    5. Classifying customers into risk categories.

The model is intended exclusively for educational purposes.

Author:
    José Reyes

Project:
    Credit Risk Analytics Suite

===============================================================================
"""

# =============================================================================
# Imports
# =============================================================================

from typing import Tuple

import numpy as np
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split



# =============================================================================
# Public Configuration
# =============================================================================

DEFAULT_TEST_SIZE = 0.20  # % of testing data
DEFAULT_RANDOM_STATE = 42
DEFAULT_MAX_ITER = 1_000  # Max of 1000 iterations to find the optimal solution



# =============================================================================
# Synthetic Default Flag Generation
# =============================================================================

def generate_default_flag(
    customer: pd.Series,
    rng: np.random.Generator
) -> int:
    """
    Generate a synthetic default event for a customer.

    The default probability is derived from the customer's
    financial and credit characteristics.

    This function is used exclusively to create synthetic
    historical outcomes for educational model training.

    Parameters
    ----------
    customer : pd.Series
        Customer financial and credit information.

    rng : numpy.random.Generator
        Random number generator used to simulate the default event.

    Returns
    -------
    int
        1 if the customer defaults.
        0 otherwise.
    """

    # 1. Initialize a synthetic risk score
    risk_score = 0.0

    # 2. Late payments
    risk_score += customer["Late_Payments"] * 0.08


    # 3. Credit utilization
    risk_score += customer["Credit_Utilization"] / 100 * 0.25


    # 4. Credit history
    if customer["Credit_History_Years"] < 3:
        risk_score += 0.15

    elif customer["Credit_History_Years"] < 7:
        risk_score += 0.05


    # 5. Recent inquiries
    risk_score += customer["Recent_Inquiries"] * 0.04


    # 6. Employment stability
    if customer["Employment_Years"] < 2:
        risk_score += 0.10

    elif customer["Employment_Years"] < 5:
        risk_score += 0.05


    # 7. Convert risk score into probability
    default_probability = min(risk_score, 0.95)


    # 8. Simulate default event
    default_event = rng.random() < default_probability

    return int(default_event)



# =============================================================================
# Train Probability of Default Model
# =============================================================================

def train_pd_model(
    X: pd.DataFrame,
    y: pd.Series
) -> LogisticRegression:
    """
    Train a Logistic Regression model for Probability of Default.

    Parameters
    ----------
    X : pandas.DataFrame
        Predictor variables used by the model.

    y : pandas.Series
        Target variable representing simulated default events.

    Returns
    -------
    LogisticRegression
        Trained Logistic Regression model.
    """


    # 1. Create the Logistic Regression model
    model = LogisticRegression(
        random_state=42,
        max_iter=1000
    )

    # 2. Train the model
    model.fit(X, y)
    
    
    # 3. Return the trained model
    return model