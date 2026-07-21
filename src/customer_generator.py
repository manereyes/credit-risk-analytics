"""
===============================================================================
Customer Generator Module
===============================================================================

This module generates synthetic customer portfolios for the Credit Risk
Analytics Suite.

Customers are generated according to probabilistic customer segments
designed to simulate realistic retail banking populations.

The generated data is intended exclusively for educational purposes.

Author:
    José Reyes

Project:
    Credit Risk Analytics Suite

===============================================================================
"""

# =============================================================================
# Imports
# =============================================================================

from dataclasses import dataclass
from typing import Dict

# For probabilistic distributions
import numpy as np

import pandas as pd



# =============================================================================
# Public Configuration (const)
# =============================================================================

DEFAULT_N_CUSTOMERS = 1_000
DEFAULT_RANDOM_SEED = 42



# =============================================================================
# Default Customer Segment Weights
# =============================================================================

DEFAULT_SEGMENT_WEIGHTS = {
    "Young Professional": 0.30,
    "Established Professional": 0.30,
    "Senior Professional": 0.15,
    "High Income": 0.10,
    "Credit Builder": 0.15,
} # These are the default % of profiles generated (the sum of every segment must be 1.0), e.g If "High Income" is set to .10 (10%), that means 100 of every 1000 (default n_customers) customers will fall into this segment



# =============================================================================
# Customer Segment
# =============================================================================

@dataclass
class CustomerSegment:
    """
    Represents the probabilistic profile of a customer segment.

    A CustomerSegment defines the parameters used to generate synthetic
    customers with similar demographic, financial, and credit characteristics.

    The segment does not represent an individual customer.

    Instead, it represents a probabilistic profile from which individual
    customers can be generated.
    """
    ## PARAMETERS ##
    # Segment identity
    name: str
    weight: float

    # Demographic parameters
    age_mean: float
    age_std: float

    # Income parameters
    income_mean: float
    income_std: float

    # Credit behavior parameters
    late_payment_probabilities: Dict[int, float]

    utilization_alpha: float
    utilization_beta: float

    credit_history_mean: float
    credit_history_std: float

    credit_mix_probabilities: Dict[int, float]

    inquiries_lambda: float



# =============================================================================
# Default Customer Segment Configurations
# =============================================================================
#
# Below, there are the default CustomerSegments with their own attributes and probabilities based on their
# segment. (Encapsulation)
#

YOUNG_PROFESSIONAL = CustomerSegment(
    name="Young Professional",
    weight=0.30,

    age_mean=28,
    age_std=4,

    income_mean=10.5,
    income_std=0.35,

    late_payment_probabilities={
        0: 0.40,
        1: 0.27,
        2: 0.15,
        3: 0.09,
        4: 0.06,
        5: 0.03,
    },

    utilization_alpha=2.5,
    utilization_beta=4.0,

    credit_history_mean=4,
    credit_history_std=2,

    credit_mix_probabilities={
        1: 0.35,
        2: 0.40,
        3: 0.20,
        4: 0.05,
    },

    inquiries_lambda=1.5,
)


ESTABLISHED_PROFESSIONAL = CustomerSegment(
    name="Established Professional",
    weight=0.30,

    age_mean=40,
    age_std=6,

    income_mean=11.2,
    income_std=0.40,

    late_payment_probabilities={
        0: 0.50,
        1: 0.25,
        2: 0.12,
        3: 0.06,
        4: 0.04,
        5: 0.03,
    },

    utilization_alpha=3.0,
    utilization_beta=5.0,

    credit_history_mean=10,
    credit_history_std=4,

    credit_mix_probabilities={
        1: 0.15,
        2: 0.35,
        3: 0.35,
        4: 0.15,
    },

    inquiries_lambda=1.2,
)


SENIOR_PROFESSIONAL = CustomerSegment(
    name="Senior Professional",
    weight=0.15,

    age_mean=55,
    age_std=7,

    income_mean=11.6,
    income_std=0.45,

    late_payment_probabilities={
        0: 0.60,
        1: 0.22,
        2: 0.09,
        3: 0.04,
        4: 0.03,
        5: 0.02,
    },

    utilization_alpha=3.5,
    utilization_beta=6.0,

    credit_history_mean=18,
    credit_history_std=5,

    credit_mix_probabilities={
        1: 0.10,
        2: 0.25,
        3: 0.40,
        4: 0.25,
    },

    inquiries_lambda=0.8,
)


HIGH_INCOME = CustomerSegment(
    name="High Income",
    weight=0.10,

    age_mean=45,
    age_std=8,

    income_mean=12.2,
    income_std=0.55,

    late_payment_probabilities={
        0: 0.70,
        1: 0.18,
        2: 0.06,
        3: 0.03,
        4: 0.02,
        5: 0.01,
    },

    utilization_alpha=4.0,
    utilization_beta=8.0,

    credit_history_mean=15,
    credit_history_std=5,

    credit_mix_probabilities={
        1: 0.05,
        2: 0.20,
        3: 0.40,
        4: 0.35,
    },

    inquiries_lambda=0.7,
)


CREDIT_BUILDER = CustomerSegment(
    name="Credit Builder",
    weight=0.15,

    age_mean=32,
    age_std=8,

    income_mean=10.4,
    income_std=0.40,

    late_payment_probabilities={
        0: 0.50,
        1: 0.25,
        2: 0.12,
        3: 0.06,
        4: 0.04,
        5: 0.03,
    },

    utilization_alpha=2.0,
    utilization_beta=3.5,

    credit_history_mean=3,
    credit_history_std=2,

    credit_mix_probabilities={
        1: 0.50,
        2: 0.35,
        3: 0.12,
        4: 0.03,
    },

    inquiries_lambda=1.8,
)



# =============================================================================
# Default Segment Collection
# =============================================================================
#
# A list of CustomerSegments with their own params to assign for each client further
#

DEFAULT_SEGMENTS = [
    YOUNG_PROFESSIONAL,
    ESTABLISHED_PROFESSIONAL,
    SENIOR_PROFESSIONAL,
    HIGH_INCOME,
    CREDIT_BUILDER,
]


# =============================================================================
# Public Callable Methods
# =============================================================================
#
# The methods will be used to generate every customer's characteristic based on:
#     - Their segment's parameters
#     - probability (rng)
# Further, these methods will be used by a generate_everything() method to generate every
# customer characteristic 
#

def generate_age(
    segment: CustomerSegment,
    rng: np.random.Generator
) -> int:
    """
    Generate a customer's age based on the segment's
    age distribution.

    Parameters
    ----------
    segment : CustomerSegment
        Customer segment containing age distribution parameters.

    rng : numpy.random.Generator
        Random number generator.

    Returns
    -------
    int
        Generated customer age.
    """
    # Generating a normal distributed age
    age = rng.normal(
        loc=segment.age_mean, # Takes the age mean of the segment param
        scale=segment.age_std # Takes the stdv of the segment param
    )

    return max(round(age), 18)  # Let's say, if a generated age = 16.9, it will be rounded to 17, and replaced by 18 thanks to "max()"


def generate_income(
    segment: CustomerSegment,
    rng: np.random.Generator
) -> float:
    """
    Generate annual income based on the segment's
    log-normal income distribution.

    Parameters
    ----------
    segment : CustomerSegment
        Customer segment containing income parameters.

    rng : numpy.random.Generator
        Random number generator.

    Returns
    -------
    float
        Annual income in USD.
    """
    # Generating a normal distributed income
    income = rng.lognormal(
        mean=segment.income_mean,
        sigma=segment.income_std
    )

    return round(income, 2)


def generate_employment_years(
    age: int,
    rng: np.random.Generator
) -> int:
    """
    Generate realistic employment years based on age.

    Employment years are constrained by the assumption that
    formal employment begins at approximately age 18.

    Parameters
    ----------
    age : int
        Customer age.

    rng : numpy.random.Generator
        Random number generator.

    Returns
    -------
    int
        Employment years.
    """

    # Our max_exmployment_years will be generated by this logic
    max_employment_years = max(age - 18, 1)

    # Our employment_years will be generated by this logic:
    #    - a random integer between 1 and the max possible/realistic number of employment years
    # e.g:
    #    - Age = 25 maximum employment years will be always 7 (25-18)
    #    - The employment_years will fall between 1 and 7, for a more realistic approach
    employment_years = rng.integers(
        low=1,
        high=max_employment_years + 1 # high number is allways exclusive, that's why we add 1A
    )

    return int(employment_years)


def generate_late_payments(
    segment: CustomerSegment,
    rng: np.random.Generator
) -> int:
    """
    Generate historical late payments based on
    segment-specific probabilities.

    Parameters
    ----------
    segment : CustomerSegment
        Customer segment containing late payment probabilities.

    rng : numpy.random.Generator
        Random number generator.

    Returns
    -------
    int
        Number of historical late payments.
    """
    
    # First we set 2 lists:
    #    - late_payment_values with the keys of the late_payment_probabilities parameter of the given segment
    #    - late_payment_probabilities with the values of the late_payment_probabilities parameter of the given segment
    late_payment_values = list(
        segment.late_payment_probabilities.keys()
    )

    late_payment_probabilities = list(
        segment.late_payment_probabilities.values()
    )

    # We compute a random choice between the values and the probabilities, and set the value to late_payments
    # e.g.
    #    - For a given list of values [0, 1, 2]
    #    - And a given list of probs [0.10, 0.50, 0.40]
    #    - rng.choice will compute a random choice and return a value based on its probability (like a gacha game)
    late_payments = rng.choice(
        late_payment_values,
        p=late_payment_probabilities
    )

    return int(late_payments)


def generate_credit_utilization(
    segment: CustomerSegment,
    rng: np.random.Generator
) -> float:
    """
    Generate credit utilization percentage.

    Parameters
    ----------
    segment : CustomerSegment
        Customer segment containing Beta distribution parameters.

    rng : numpy.random.Generator
        Random number generator.

    Returns
    -------
    float
        Credit utilization percentage between 0 and 100.
    """

    # We compute a value beta distributed with the alpha and beta parameters of the segment, it always return values between 0 and 1
    # a beta distribution is always fittable for results between 0 <= x <= 1
    # In this case, is used to generate a credit utilization %
    utilization = rng.beta(
        a=segment.utilization_alpha,
        b=segment.utilization_beta
    )

    return round(utilization * 100, 2) # We return the value, but normalized into a percentage. e.g. round(0.10 * 100, 2) = 10


def generate_credit_history(
    segment: CustomerSegment,
    age: int, # We need the generated customer's age
    rng: np.random.Generator
) -> int:
    """
    Generate credit history years based on segment parameters
    and constrained by customer age.

    Parameters
    ----------
    segment : CustomerSegment
        Customer segment containing credit history parameters.

    age : int
        Customer age.

    rng : numpy.random.Generator
        Random number generator.

    Returns
    -------
    int
        Credit history years.
    """

    # A normal distribution with the segment's credit history mean & stdv
    # We set an estimation of the credit history years of the customer
    generated_history = rng.normal(
        loc=segment.credit_history_mean,
        scale=segment.credit_history_std
    )

    # The required max_credit_history a customer could have will be a result of their age - 18
    # Like employment_years
    # But this helps creating the maximum possible years a customer could have using credit
    # e.g
    #    - A customer with 34 years can have at least 16 maximum years of credit history (16+18=36)
    max_credit_history = max(age - 18, 1)

    # The credit history is generated by this logic:
    #    - The generated_history is an estimated value a customer for normal distribution
    #    - we choose the minimal number between the generated_history and max_credit_history 
    # e.g 
    #    - A customer with 34 years can have at least 16 maximum years of credit history (16+18=36)
    #    - If the normal distributed estimated generated_history value is 10.8 (rounded to 11), then:
    #         - If the estimated history years (11) is chosen, that means the customer began asking for
    #         credits since he was 25 y/o, which is suitable
    #         - If the max_credit_history (16) is chosen, that means the customer began asking for
    #         credits since he was 18
    #    - The credit_history will take the minimum value to benefit the normal distribution but...
    #    It can help to prevent or avoid poor-assumed history years
    credit_history = min(
        round(generated_history),
        max_credit_history
    )

    return max(1, int(credit_history))


def generate_credit_mix(
    segment: CustomerSegment,
    rng: np.random.Generator
) -> int:
    """
    Generate the number of active credit products.

    Parameters
    ----------
    segment : CustomerSegment
        Customer segment containing credit mix probabilities.

    rng : numpy.random.Generator
        Random number generator.

    Returns
    -------
    int
        Number of active credit products.
    """

    # Works the same as late_payments
    credit_mix_values = list(
        segment.credit_mix_probabilities.keys()
    )

    credit_mix_probabilities = list(
        segment.credit_mix_probabilities.values()
    )

    credit_mix = rng.choice(
        credit_mix_values,
        p=credit_mix_probabilities
    )

    return int(credit_mix)


def generate_recent_inquiries(
    segment: CustomerSegment,
    rng: np.random.Generator
) -> int:
    """
    Generate recent credit inquiries.

    Parameters
    ----------
    segment : CustomerSegment
        Customer segment containing the Poisson distribution parameter.

    rng : numpy.random.Generator
        Random number generator.

    Returns
    -------
    int
        Number of recent credit inquiries.
    """

    # Generates a poisson distributed inquiries number with the lambda parameter of the given segment class
    inquiries = rng.poisson(
        lam=segment.inquiries_lambda
    )

    return int(inquiries)


##########################################
### generate_customers() is on the way ###
##########################################