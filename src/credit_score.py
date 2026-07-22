"""
===============================================================================
Credit Score Calculator Module
===============================================================================

This module calculates an educational credit score for synthetic customers.

The module evaluates several dimensions of credit behavior, including:

    - Payment History
    - Credit Utilization
    - Credit History Length
    - Credit Mix
    - Recent Credit Activity

The calculated component scores are combined using predefined weights to
produce a Raw Credit Score.

The Raw Credit Score is then normalized into an educational Credit Score
between approximately 400 and 850.

This module is intended exclusively for educational purposes.

Author:
    José Reyes

Project:
    Credit Risk Analytics Suite

===============================================================================
"""

# =============================================================================
# Imports
# =============================================================================

import pandas as pd



# =============================================================================
# Credit Score Weights
# =============================================================================

PAYMENT_HISTORY_WEIGHT = 0.35
UTILIZATION_WEIGHT = 0.30
CREDIT_HISTORY_WEIGHT = 0.15
CREDIT_MIX_WEIGHT = 0.10
RECENT_ACTIVITY_WEIGHT = 0.10



# =============================================================================
# Payment History Score
# =============================================================================

def calculate_payment_history_score(
    late_payments: int
 ) -> int:
    """
    Calculate the Payment History Score.

    Fewer late payments result in a higher score.

    Parameters
    ----------
    late_payments : int
        Number of historical late payments.

    Returns
    -------
    int
        Payment history score between 20 and 100.
    """

    if late_payments == 0:
        return 100

    elif late_payments == 1:
        return 90

    elif late_payments == 2:
        return 75

    elif late_payments == 3:
        return 55

    else:
        return 20
    

# =============================================================================
# Credit Utilization Score
# =============================================================================

def calculate_utilization_score(
    utilization: float
) -> int:
    """
    Calculate the Credit Utilization Score.

    Lower credit utilization results in a higher score.

    Parameters
    ----------
    utilization : float
        Percentage of available credit currently being used.

    Returns
    -------
    int
        Utilization score between 25 and 100.
    """

    if utilization < 30:
        return 100

    elif utilization < 50:
        return 80

    elif utilization < 70:
        return 60

    else:
        return 25


# =============================================================================
# Credit History Score
# =============================================================================

def calculate_credit_history_score(
    years: int
) -> int:
    """
    Calculate the Credit History Score.

    A longer credit history generally provides more information
    about the customer's historical credit behavior.

    Parameters
    ----------
    years : int
        Number of years of credit history.

    Returns
    -------
    int
        Credit history score between 30 and 100.
    """

    if years > 10:
        return 100

    elif years >= 5:
        return 80

    elif years >= 2:
        return 60

    else:
        return 30
    
    
# =============================================================================
# Credit Mix Score
# =============================================================================

def calculate_credit_mix_score(
    products: int
) -> int:
    """
    Calculate the Credit Mix Score.

    A broader mix of credit products may provide more information
    about the customer's ability to manage different types of credit.

    Parameters
    ----------
    products : int
        Number of active credit products.

    Returns
    -------
    int
        Credit mix score between 40 and 100.
    """

    if products >= 4:
        return 100

    elif products == 3:
        return 80

    elif products == 2:
        return 60

    else:
        return 40
    
    
# =============================================================================
# Recent Credit Activity Score
# =============================================================================

def calculate_recent_activity_score(
    inquiries: int
) -> int:
    """
    Calculate the Recent Credit Activity Score.

    Fewer recent credit inquiries result in a higher score.

    Parameters
    ----------
    inquiries : int
        Number of recent credit inquiries.

    Returns
    -------
    int
        Recent activity score between 30 and 100.
    """

    if inquiries == 0:
        return 100

    elif inquiries == 1:
        return 90

    elif inquiries == 2:
        return 75

    elif inquiries == 3:
        return 60

    else:
        return 30
    

# Using Weighted Mean to calculate the Raw Credit Score
def calculate_raw_score(customer: pd.Series) -> float:
    """
    Calculate the weighted raw credit score for a single customer.

    Parameters
    ----------
    customer : pandas.Series
        Customer record containing credit behavior variables.

    Returns
    -------
    float
        Weighted raw credit score between 0 and 100.
    """
    
    # The function takes a pandas Series and then:
    # 1. Calculates the individual component scores using the respective functions.
    # 2. Applies the predefined weights to each component score.
    # 3. Sums the weighted scores to produce a raw score.

    payment_score = calculate_payment_history_score(
        customer["Late_Payments"]
    )

    utilization_score = calculate_utilization_score(
        customer["Credit_Utilization"]
    )

    history_score = calculate_credit_history_score(
        customer["Credit_History_Years"]
    )

    mix_score = calculate_credit_mix_score(
        customer["Credit_Mix"]
    )

    activity_score = calculate_recent_activity_score(
        customer["Recent_Inquiries"]
    )

    raw_score = (
        payment_score * PAYMENT_HISTORY_WEIGHT
        + utilization_score * UTILIZATION_WEIGHT
        + history_score * CREDIT_HISTORY_WEIGHT
        + mix_score * CREDIT_MIX_WEIGHT
        + activity_score * RECENT_ACTIVITY_WEIGHT
    )

    return round(raw_score, 2)



# Normalizing the Raw Credit Score to an educational Credit Score function
def normalize_credit_score(raw_score: float) -> int:
    """
    Convert the raw credit score into the educational
    standardized credit score scale.

    Parameters
    ----------
    raw_score : float
        Weighted raw score between 0 and 100.

    Returns
    -------
    int
        Credit score between 400 and 850.
    """

    credit_score = 400 + (4.5 * raw_score)

    return round(credit_score)


# Function to assign a rating level based on the credit score
def assign_credit_rating(score: int) -> str:
    """
    Assign a credit rating based on the credit score.

    Parameters
    ----------
    score : int
        Standardized credit score.

    Returns
    -------
    str
        Credit rating category.
    """

    if score >= 750:
        return "Excellent"

    elif score >= 650:
        return "Good"

    elif score >= 550:
        return "Fair"

    return "Poor"


# Orchestrator function to calculate the credit score and rating for a customer
def calculate_credit_scores(
    customers: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate credit scores for a customer portfolio.

    This function applies the complete educational credit
    scoring pipeline to each customer.

    Parameters
    ----------
    customers : pandas.DataFrame
        Customer portfolio generated by the Customer Generator.

    Returns
    -------
    pandas.DataFrame
        Original customer portfolio enriched with credit
        component scores, Raw Credit Score, Credit Score,
        and Credit Rating.
    """

    # Create a copy to avoid modifying the original DataFrame
    scored_customers = customers.copy()

    # ---------------------------------------------------------
    # 1. Calculate individual component scores
    # ---------------------------------------------------------

    scored_customers["Payment_History_Score"] = (
        scored_customers["Late_Payments"]
        .apply(calculate_payment_history_score)
    )

    scored_customers["Utilization_Score"] = (
        scored_customers["Credit_Utilization"]
        .apply(calculate_utilization_score)
    )

    scored_customers["Credit_History_Score"] = (
        scored_customers["Credit_History_Years"]
        .apply(calculate_credit_history_score)
    )

    scored_customers["Credit_Mix_Score"] = (
        scored_customers["Credit_Mix"]
        .apply(calculate_credit_mix_score)
    )

    scored_customers["Recent_Activity_Score"] = (
        scored_customers["Recent_Inquiries"]
        .apply(calculate_recent_activity_score)
    )

    # ---------------------------------------------------------
    # 2. Calculate Raw Credit Score
    # ---------------------------------------------------------

    scored_customers["Raw_Credit_Score"] = (
        scored_customers.apply(
            calculate_raw_score,
            axis=1
        )
    )

    # ---------------------------------------------------------
    # 3. Normalize Raw Score into Credit Score
    # ---------------------------------------------------------

    scored_customers["Credit_Score"] = (
        scored_customers["Raw_Credit_Score"]
        .apply(normalize_credit_score)
    )

    # ---------------------------------------------------------
    # 4. Assign Credit Rating
    # ---------------------------------------------------------

    scored_customers["Credit_Rating"] = (
        scored_customers["Credit_Score"]
        .apply(assign_credit_rating)
    )

    # ---------------------------------------------------------
    # 5. Return enriched DataFrame
    # ---------------------------------------------------------

    return scored_customers