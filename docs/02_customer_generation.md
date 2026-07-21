# Customer Generation & Segmentation Model

## 1. Overview

The Customer Generation & Segmentation Model is the first processing layer of the Credit Risk Analytics Suite.

Its purpose is to generate a synthetic portfolio of customers with realistic and internally consistent financial and credit characteristics.

The generator is designed to simulate a simplified population of retail banking customers while preserving logical relationships between variables.

The objective is not to create perfectly random customers.

The objective is to create **plausible synthetic customers** whose characteristics can later be evaluated by the Credit Score, Probability of Default, Risk Classification, and Credit Decision modules.

The generation pipeline follows:

```text
Customer Segment
        │
        ▼
Probabilistic Customer Profile
        │
        ▼
Customer Characteristics
        │
        ▼
Derived Financial Variables
        │
        ▼
Synthetic Customer Portfolio
```

The resulting portfolio will be represented as a `pandas.DataFrame`.

---

# 2. Design Objectives

The Customer Generation Model must satisfy the following objectives:

1. Generate a configurable number of synthetic customers.
2. Assign customers to predefined probabilistic segments.
3. Generate realistic customer characteristics based on segment profiles.
4. Use appropriate probability distributions for different types of variables.
5. Preserve logical relationships between customer variables.
6. Prevent obviously unrealistic combinations of attributes.
7. Provide reproducible results through a configurable random seed.
8. Keep the generation process reusable across notebooks and Streamlit.
9. Support future modification of segment distributions.
10. Prepare the system for the interactive Sandbox planned for version 1.3.

The generator should remain simple enough to understand while applying good programming and data science practices.

---

# 3. Customer Data Model

The generated customer portfolio will initially contain the following variables.

```text
Customer_ID
Customer_Segment

Age
Annual_Income
Monthly_Debt_Payment
Debt_to_Income_Ratio

Years_of_Experience
Employment_Years

Credit_History_Years
Number_of_Loans
Credit_Utilization
Previous_Defaults
```

These variables are divided into four conceptual groups.

---

## 3.1 Customer Identification

### Customer_ID

A unique identifier assigned to each synthetic customer.

Example:

```text
C0001
C0002
C0003
```

The identifier has no predictive value and is used only to identify observations within the portfolio.

---

### Customer_Segment

The probabilistic segment assigned to the customer.

Initial segments:

```text
Young Professional
Established Professional
Senior Professional
High Income
Credit Builder
```

Customer segments describe the customer's general demographic and financial profile.

They are not equivalent to credit risk categories.

For example:

```text
Customer Segment
        │
        ▼
Young Professional
        │
        ▼
Credit Score
        │
        ▼
Probability of Default
        │
        ▼
Risk Category
```

A Young Professional may therefore be classified as Low Risk, Medium Risk, or High Risk depending on their individual characteristics.

---

# 4. Customer Segments

The initial population will contain five probabilistic customer segments.

The segment weights define the expected composition of the generated portfolio.

The default segment distribution is:

| Customer Segment         | Default Weight |
| ------------------------ | -------------: |
| Young Professional       |            30% |
| Established Professional |            30% |
| Senior Professional      |            15% |
| High Income              |            10% |
| Credit Builder           |            15% |

The weights must satisfy:

$
\sum_{i=1}^{n} P(Segment_i) = 1
$

Therefore:

$\
0.30 + 0.30 + 0.15 + 0.10 + 0.15 = 1.00
$

The segment weights will initially be defined in the Python code as configurable parameters.

In version 1.0, the default values will be used.

In version 1.3, the same parameters will be controlled interactively through the Streamlit Sandbox.

The Customer Generator itself will not be replaced.

---

# 5. Segment Definitions

## 5.1 Young Professional

The Young Professional segment represents customers who are relatively early in their professional and credit lifecycle.

Typical characteristics include:

* Younger age.
* Lower or moderate income.
* Fewer years of professional experience.
* Shorter employment history.
* Shorter credit history.
* Fewer loans.
* Moderate credit utilization.
* Mostly clean payment history.

Conceptual profile:

| Variable             | Expected Profile |
| -------------------- | ---------------- |
| Age                  | Young            |
| Annual Income        | Low to Moderate  |
| Years of Experience  | Low              |
| Employment Years     | Low              |
| Credit History Years | Short            |
| Number of Loans      | Low              |
| Credit Utilization   | Moderate         |
| Previous Defaults    | Low probability  |

The segment is not inherently high risk.

Its members simply have less financial and credit history.

---

## 5.2 Established Professional

The Established Professional segment represents customers with a more developed professional and financial profile.

Typical characteristics include:

* Moderate to mature age.
* Moderate to high income.
* Several years of professional experience.
* Longer employment history.
* Established credit history.
* Moderate number of loans.
* Low to moderate credit utilization.
* Low probability of previous defaults.

Conceptual profile:

| Variable             | Expected Profile |
| -------------------- | ---------------- |
| Age                  | Adult            |
| Annual Income        | Moderate to High |
| Years of Experience  | Moderate         |
| Employment Years     | Moderate         |
| Credit History Years | Established      |
| Number of Loans      | Moderate         |
| Credit Utilization   | Low to Moderate  |
| Previous Defaults    | Low probability  |

---

## 5.3 Senior Professional

The Senior Professional segment represents customers with long professional and credit histories.

Typical characteristics include:

* Mature age.
* High income.
* Long professional experience.
* Long employment history.
* Long credit history.
* Multiple credit products.
* Low to moderate credit utilization.
* Low probability of previous defaults.

Conceptual profile:

| Variable             | Expected Profile |
| -------------------- | ---------------- |
| Age                  | Mature           |
| Annual Income        | High             |
| Years of Experience  | High             |
| Employment Years     | High             |
| Credit History Years | Long             |
| Number of Loans      | Moderate to High |
| Credit Utilization   | Low to Moderate  |
| Previous Defaults    | Low probability  |

---

## 5.4 High Income

The High Income segment represents customers whose primary defining characteristic is high earning capacity.

Unlike the Senior Professional segment, age is not the defining characteristic.

A High Income customer may therefore be relatively young or mature.

Typical characteristics include:

* High annual income.
* Moderate to high professional experience.
* Strong financial capacity.
* Established credit access.
* Multiple loans or credit products.
* Generally lower credit utilization.
* Low probability of previous defaults.

Conceptual profile:

| Variable             | Expected Profile  |
| -------------------- | ----------------- |
| Age                  | Broad Adult Range |
| Annual Income        | Very High         |
| Years of Experience  | Moderate to High  |
| Employment Years     | Moderate to High  |
| Credit History Years | Moderate to Long  |
| Number of Loans      | Moderate to High  |
| Credit Utilization   | Low to Moderate   |
| Previous Defaults    | Low probability   |

The High Income segment may overlap with other demographic profiles.

For example, a customer can be both:

```text
High Income
```

and:

```text
Young Professional
```

The current implementation will assign one primary segment per customer for simplicity.

---

## 5.5 Credit Builder

The Credit Builder segment represents customers who are developing or rebuilding their credit profile.

Typical characteristics include:

* Broad adult age range.
* Low to moderate income.
* Short or limited credit history.
* Few loans.
* Moderate to high credit utilization.
* Higher probability of previous defaults.

Conceptual profile:

| Variable             | Expected Profile   |
| -------------------- | ------------------ |
| Age                  | Broad Adult Range  |
| Annual Income        | Low to Moderate    |
| Years of Experience  | Variable           |
| Employment Years     | Variable           |
| Credit History Years | Short              |
| Number of Loans      | Low                |
| Credit Utilization   | Moderate to High   |
| Previous Defaults    | Higher probability |

This segment is particularly useful for demonstrating how different customer populations can produce different credit risk outcomes.

---

# 6. Probability Distributions

The Customer Generator will use different probability distributions depending on the nature of each variable.

The purpose of using probability distributions is to create realistic variation between customers.

A distribution describes how likely different values are to occur.

For example, instead of saying:

```text
Every customer earns exactly $50,000.
```

we can define:

```text
Most customers earn around a typical value,
while some earn less and others earn significantly more.
```

The generator will use several types of distributions.

---

# 7. Normal Distribution

The Normal Distribution is useful for variables that tend to cluster around an average value.

It is commonly represented as:

$\
X \sim N(\mu,\sigma)
$\

where:

* ($\mu$) represents the mean or average.
* ($\sigma$) represents the standard deviation or spread.

The distribution is often visualized as a bell-shaped curve.

For example:

```text
             Most Customers
                  │
                  ▼
              ███████
           █████████████
        ███████████████████
     █████████████████████████
─────────────────────────────────
       Low       Average      High
```

The Normal Distribution may be used for variables such as:

* Age.
* Some employment-related variables.
* Other approximately symmetric continuous variables.

Values will be constrained when necessary to prevent unrealistic results.

For example:

```text
Age >= 18
Age <= 65
```

This can be implemented using a clipping operation.

---

# 8. Lognormal Distribution

Income is often not well represented by a simple Normal Distribution.

A Normal Distribution is symmetric around its average.

Real-world income distributions are usually asymmetric.

There are many people around low or middle income levels and fewer people with extremely high incomes.

This creates a right-skewed distribution.

Conceptually:

```text
Customers
   │
   │ ███████████
   │ ███████████████
   │ █████████████████
   │ ███████████████████
   │ █████████████
   │ ███████
   │ ███
   └──────────────────────────────► Income
        Low       Middle     High
```

A Lognormal Distribution is useful for modeling this behavior.

Conceptually:

$\
X \sim LogNormal(\mu,\sigma)
$

The parameters will be configured separately for each customer segment.

This allows the model to generate:

* Lower income populations.
* Middle income populations.
* High income populations.

without manually defining every possible income level.

---

# 9. Beta Distribution

The Beta Distribution is useful for variables that naturally exist between two boundaries.

The primary use in this project will be:

```text
Credit_Utilization
```

Credit utilization can be represented as a percentage:

$
0 \leq Utilization \leq 100
$

The Beta Distribution naturally produces values between 0 and 1.

The generated value can therefore be transformed into a percentage:

$
Utilization = X \times 100
$

Different Beta Distribution parameters can create different shapes.

For example:

```text
Low Utilization Profile
        ↓
Most customers near lower values

High Utilization Profile
        ↓
Most customers near higher values
```

This makes the Beta Distribution useful for creating segment-specific utilization profiles.

---

# 10. Poisson Distribution

The Poisson Distribution is useful for modeling the number of times an event occurs.

It may be used for variables such as:

* Number of Loans.
* Previous Defaults.

The distribution is represented conceptually as:

$
X \sim Poisson(\lambda)
$

where (\lambda) represents the expected average number of events.

For example:

```text
Number of Previous Defaults

0 defaults → Most common
1 default  → Less common
2 defaults → Less common
3 defaults → Rare
```

The generated values will be constrained where necessary to maintain realistic ranges.

---

# 11. Discrete Probability Distributions

Some variables will be generated using explicitly defined probabilities.

For example:

```text
Previous Defaults

0 → 75%
1 → 15%
2 → 7%
3 → 3%
```

This can be implemented using a categorical or discrete probability selection mechanism.

The advantage of this approach is that the probability of each outcome can be explicitly controlled.

This is particularly useful for variables where the desired behavior is highly skewed.

---

# 12. Variable Generation Strategy

The Customer Generator will not generate all variables independently.

Instead, variables will be generated in a logical sequence.

The conceptual workflow is:

```text
1. Assign Customer Segment
          │
          ▼
2. Generate Age
          │
          ▼
3. Generate Years of Experience
          │
          ▼
4. Generate Employment Years
          │
          ▼
5. Generate Annual Income
          │
          ▼
6. Generate Credit History Years
          │
          ▼
7. Generate Number of Loans
          │
          ▼
8. Generate Credit Utilization
          │
          ▼
9. Generate Previous Defaults
          │
          ▼
10. Generate Monthly Debt Payment
          │
          ▼
11. Calculate Debt-to-Income Ratio
```

This approach helps maintain logical consistency.

---

# 13. Variable Relationships

The generator will use relationships between variables where appropriate.

The objective is to avoid treating every variable as independent.

---

## 13.1 Age and Experience

Professional experience should generally increase with age.

The generator should respect the conceptual relationship:

$
YearsOfExperience \leq Age - 18
$

This assumes that professional experience begins no earlier than approximately age 18.

For example:

```text
Age = 22
Maximum Experience ≈ 4 years
```

A customer should not be generated with:

```text
Age = 22
Years_of_Experience = 30
```

---

## 13.2 Age and Employment

Employment years should also be constrained by age.

Conceptually:

$
EmploymentYears \leq YearsOfExperience
$

This prevents situations such as:

```text
Years of Experience = 5
Employment Years = 15
```

---

## 13.3 Age and Credit History

Credit history should generally be related to age.

A customer cannot have a credit history that significantly exceeds their plausible financial lifecycle.

Therefore:

$
CreditHistoryYears \leq Age - 18
$

The exact implementation may use additional constraints to reflect realistic differences between the beginning of employment and the beginning of credit activity.

---

## 13.4 Income and Debt Payments

Annual income represents gross yearly income.

Monthly debt payment represents the customer's recurring monthly debt obligations.

The two variables will be related through the Debt-to-Income Ratio.

Monthly income is:

$
MonthlyIncome =
\frac{AnnualIncome}{12}
$

Debt-to-Income Ratio is:

$
DTI =
\frac{MonthlyDebtPayment}
{MonthlyIncome}
$

or equivalently:

$
DTI =
\frac{MonthlyDebtPayment \times 12}
{AnnualIncome}
$

The ratio may be stored as a decimal or percentage depending on the implementation.

For example:

```text
Annual Income = $60,000
Monthly Income = $5,000
Monthly Debt Payment = $1,000

DTI = 1,000 / 5,000
DTI = 0.20
DTI = 20%
```

The DTI will be calculated rather than independently generated.

This makes it a **derived variable**.

---

## 13.5 Credit History and Number of Loans

Customers with longer credit histories may have had more opportunities to acquire credit products.

Therefore, the Number of Loans may be positively related to Credit History Years.

However, this relationship should not be deterministic.

Two customers with the same credit history length may have very different numbers of loans.

The generator will therefore use probabilistic variation.

---

## 13.6 Credit Utilization and Previous Defaults

Credit utilization and previous defaults are both indicators of credit behavior.

The initial generator may allow these variables to vary independently within segment-specific distributions.

The relationship between them will primarily emerge later through:

* Credit Score.
* Probability of Default.
* Credit Decision.

This keeps the generation model simple and prevents over-engineering the synthetic data generation process.

---

# 14. Derived Variables

Some variables should not be generated directly.

Instead, they should be calculated from other variables.

The primary derived variable is:

```text
Debt_to_Income_Ratio
```

The relationship is:

[
DTI =
\frac{MonthlyDebtPayment}
{AnnualIncome / 12}
]

The process is therefore:

```text
Annual Income
      │
      ▼
Monthly Income
      │
      │
Monthly Debt Payment
      │
      ▼
Debt-to-Income Ratio
```

This approach improves internal consistency and demonstrates an important Data Analytics concept:

> A variable can be derived from underlying business information instead of being independently generated.

---

# 15. CustomerSegment Class

The `CustomerSegment` class represents the probabilistic profile of a customer segment.

The class is responsible for storing the parameters that define how a segment behaves.

Conceptually:

```python
class CustomerSegment:
    ...
```

The class may contain attributes representing:

* Segment name.
* Segment weight.
* Age parameters.
* Income parameters.
* Experience parameters.
* Employment parameters.
* Credit history parameters.
* Loan parameters.
* Utilization parameters.
* Previous default parameters.

The class may also provide methods responsible for generating segment-specific values.

Examples:

```text
generate_age()
generate_income()
generate_experience()
generate_employment_years()
generate_credit_history()
generate_number_of_loans()
generate_credit_utilization()
generate_previous_defaults()
```

The class encapsulates the probabilistic behavior of a customer segment.

This means that the logic defining how a segment generates its values is grouped inside the segment object rather than scattered throughout the project.

---

# 16. CustomerGenerator Class

The `CustomerGenerator` class coordinates the generation of the complete customer portfolio.

Conceptually:

```python
class CustomerGenerator:
    ...
```

The generator is responsible for:

* Number of customers.
* Random seed.
* Available customer segments.
* Segment selection.
* Customer generation.
* DataFrame construction.
* Derived variable calculation.

The generator will expose a main method such as:

```python
generate()
```

The conceptual flow is:

```text
CustomerGenerator
        │
        ├── Select Customer Segment
        │
        ▼
CustomerSegment
        │
        ├── Generate Customer Variables
        │
        ▼
Apply Business Constraints
        │
        ▼
Calculate Derived Variables
        │
        ▼
Build DataFrame
```

The generator will return a `pandas.DataFrame`.

---

# 17. Object-Oriented Design

The project will use Object-Oriented Programming where it improves organization and reusability.

The two primary classes are:

```text
CustomerSegment
CustomerGenerator
```

The relationship can be represented as:

```text
CustomerGenerator
        │
        ├── CustomerSegment
        ├── CustomerSegment
        ├── CustomerSegment
        ├── CustomerSegment
        └── CustomerSegment
```

This is an example of **composition**.

The `CustomerGenerator` uses multiple `CustomerSegment` objects to generate the final portfolio.

Inheritance will not be introduced unless it provides a clear benefit.

The project is intended to demonstrate useful OOP concepts rather than maximize the number of classes or abstractions.

---

# 18. Encapsulation

Encapsulation means grouping data and the logic that operates on that data within an appropriate object.

In this project, the parameters and generation behavior of a customer segment will be grouped inside `CustomerSegment`.

Conceptually:

```text
CustomerSegment
│
├── Parameters
│
└── Generation Methods
```

This allows the rest of the project to interact with a segment without needing to know every internal detail of how its values are generated.

For example:

```python
segment.generate_income()
```

The caller does not need to manually implement the underlying probability distribution.

This improves:

* Reusability.
* Readability.
* Maintainability.
* Separation of responsibilities.

---

# 19. Random Seed

The Customer Generator will support a configurable random seed.

The default value will be:

```python
DEFAULT_RANDOM_SEED = 42
```

The purpose of the random seed is reproducibility.

Without a fixed seed:

```text
Run 1 → Portfolio A
Run 2 → Portfolio B
Run 3 → Portfolio C
```

With the same seed:

```text
Run 1 → Portfolio A
Run 2 → Portfolio A
Run 3 → Portfolio A
```

This is useful for:

* Debugging.
* Testing.
* Educational demonstrations.
* Reproducing results.
* Comparing different modeling approaches.

The seed will be configurable so that users can generate different populations when desired.

---

# 20. Number of Customers

The generator will use:

```python
DEFAULT_N_CUSTOMERS = 1000
```

The number of customers will be configurable.

Conceptually:

```python
CustomerGenerator(
    n_customers=1000
)
```

The default value of 1,000 customers provides enough observations for portfolio-level analysis while remaining computationally lightweight.

In version 1.3, the same parameter will be exposed through the Streamlit Sandbox.

For example:

```text
Number of Customers
        │
        ▼
[ Slider ]
        │
        ▼
CustomerGenerator
```

The Sandbox will modify the input parameter rather than introducing a new generation mechanism.

---

# 21. Version 1.0 Behavior

In version 1.0, the Customer Generator will use predefined segment profiles and default probability parameters.

The user will be able to:

1. Generate the customer portfolio.
2. View the resulting DataFrame.
3. Execute the downstream credit risk pipeline.

The default generation process will use:

```text
Customers
    = 1,000

Random Seed
    = 42

Segment Distribution
    = Predefined Default Weights
```

The resulting dataset will be passed to the Credit Score Calculator.

---

# 22. Version 1.3 Sandbox Preparation

The Customer Generation Model is intentionally designed to support future interactive experimentation.

In version 1.3, users will be able to modify:

* Number of customers.
* Customer segment weights.
* Population composition.
* Selected probabilistic generation parameters.

For example:

```text
Young Professional
[██████████████████] 60%

Established Professional
[██████] 20%

Senior Professional
[███] 10%

High Income
[█] 5%

Credit Builder
[█] 5%
```

The modified parameters will be passed to the existing `CustomerGenerator`.

The generator will therefore remain the central source of truth for customer population generation.

The Streamlit application will control parameters.

The Python module will perform the generation.

This maintains a clean separation between:

```text
User Interface
        │
        ▼
Parameters
        │
        ▼
Business Logic
        │
        ▼
Generated Data
```

---

# 23. Expected Output

The Customer Generator will return a DataFrame with the following columns:

```text
Customer_ID
Customer_Segment
Age
Annual_Income
Monthly_Debt_Payment
Debt_to_Income_Ratio
Years_of_Experience
Employment_Years
Credit_History_Years
Number_of_Loans
Credit_Utilization
Previous_Defaults
```

At this stage, the dataset will not yet contain:

```text
Raw_Credit_Score
Credit_Score
Probability_of_Default
Risk_Category
Decision
Decision_Reason
Loan_Amount
```

These fields will be added by the subsequent modules.

The resulting data flow will therefore be:

```text
Customer Generator
        │
        ▼
Customer Profile DataFrame
        │
        ▼
Credit Score Calculator
        │
        ▼
PD Model
        │
        ▼
Risk & Credit Decision Engine
```

---

# 24. Design Principles

The Customer Generation Model follows the following principles.

### Realism over Complexity

The generator should produce plausible customers without becoming unnecessarily complex.

### Probability over Determinism

Customers should vary naturally within each segment.

### Relationships over Independence

Variables should be logically related where appropriate.

### Derived Variables over Redundant Generation

Variables that can be calculated from underlying information should be derived.

### Reusability

The same generator should work in notebooks and Streamlit.

### Explainability

The logic behind the generation process should be understandable.

### Extensibility

The design should allow parameters to be modified in version 1.3.

---

# 25. Final Architecture

The Customer Generation Layer can be summarized as:

```text
                    Customer Generator
                           │
             ┌─────────────┴─────────────┐
             │                           │
      Segment Weights             Random Seed
             │                           │
             └─────────────┬─────────────┘
                           │
                           ▼
                  Customer Segmentation
                           │
                           ▼
                 CustomerSegment Objects
                           │
                           ▼
                Probabilistic Generation
                           │
                           ▼
                  Business Constraints
                           │
                           ▼
                 Derived Variables
                           │
                           ▼
                  Customer DataFrame
```

The output of this layer becomes the input of the Credit Score Calculator.

The Customer Generation Layer therefore represents the first stage of the complete Credit Risk Analytics pipeline.

```text
Customer Generation
        ↓
Credit Scoring
        ↓
Probability of Default
        ↓
Risk Classification
        ↓
Credit Decision
        ↓
Loan Amount
        ↓
Portfolio Analytics
```

---