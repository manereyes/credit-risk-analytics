# Customer Generator

## Credit Risk Analytics Suite

---

## 1. Purpose

The `customer_generator.py` module is responsible for generating a synthetic portfolio of customers for the **Credit Risk Analytics Suite**.

The purpose of this module is to create realistic fictional customers that can later be evaluated by the credit risk pipeline.

The generated customers will eventually pass through the following process:

```text
Customer Generation
        ↓
Credit Score Calculation
        ↓
Probability of Default (PD)
        ↓
Risk Classification
        ↓
Credit Decision
        ↓
Loan Amount
```

The `customer_generator.py` module is therefore the **starting point of the entire credit risk pipeline**.

It does not calculate Credit Scores.

It does not calculate Probability of Default.

It does not approve or reject loans.

Its only responsibility is to answer:

> "What kind of customers exist in our simulated portfolio?"

Each customer is generated with a combination of:

* Demographic characteristics
* Employment characteristics
* Income
* Historical credit behavior
* Current credit utilization
* Credit history
* Credit product mix
* Recent credit activity

The module uses **probability distributions** to generate realistic variation between customers.

---

# 2. Why Do We Need Synthetic Customers?

In a real banking environment, a credit risk model would normally use historical customer data.

For example:

```text
Customer Data
      ↓
Historical Credit Behavior
      ↓
Did the customer default?
      ↓
Train Statistical / ML Model
      ↓
Predict Future Default Risk
```

However, this educational project does not use a real bank's private customer database.

Therefore, we need to simulate a portfolio.

The generator creates fictional customers whose characteristics behave approximately like customers in a retail banking portfolio.

For example:

```text
Customer A
Age: 24
Income: $45,000
Late Payments: 2
Credit Utilization: 68%
Credit History: 3 years
Credit Mix: 1
Recent Inquiries: 4
```

And:

```text
Customer B
Age: 52
Income: $95,000
Late Payments: 0
Credit Utilization: 24%
Credit History: 20 years
Credit Mix: 4
Recent Inquiries: 0
```

These customers are different because the generator introduces controlled randomness.

This randomness is important.

If every customer had exactly the same characteristics, the portfolio would not be useful for studying credit risk.

---

# 3. The Main Idea: Customer Segments

The generator does not create completely random customers.

Instead, it first determines **what type of customer** is being generated.

This is called a **customer segment**.

The project currently defines five segments:

| Segment                  | Typical Profile                                                                  |
| ------------------------ | -------------------------------------------------------------------------------- |
| Young Professional       | Younger customer starting their career and credit journey                        |
| Established Professional | More stable career and longer credit history                                     |
| Senior Professional      | Older customer with extensive financial and credit experience                    |
| High Income              | Customer with substantially higher income and generally stronger credit behavior |
| Credit Builder           | Customer actively building or rebuilding their credit profile                    |

The process works like this:

```text
Generate Customer
        ↓
Select Segment
        ↓
Generate Age
        ↓
Generate Employment Years
        ↓
Generate Income
        ↓
Generate Credit Behavior
        ↓
Generate Credit History
        ↓
Generate Credit Mix
        ↓
Generate Recent Inquiries
        ↓
Return Customer
```

The segment acts as the customer's **probabilistic profile**.

For example:

A `Young Professional` is more likely to have:

* Lower age
* Shorter employment history
* Lower income
* Shorter credit history
* Higher credit utilization
* More recent credit inquiries

A `Senior Professional` is more likely to have:

* Higher age
* Longer employment history
* Longer credit history
* Lower credit utilization
* Fewer recent inquiries

This makes the generated portfolio more realistic.

---

# 4. Object-Oriented Design

The generator uses a simple form of **Object-Oriented Programming (OOP)**.

The central class is:

```python
@dataclass
class CustomerSegment:
```

This class represents a **customer segment**, not an individual customer.

For example:

```python
YOUNG_PROFESSIONAL = CustomerSegment(
    name="Young Professional",
    weight=0.30,
    age_mean=28,
    age_std=4,
    ...
)
```

The important distinction is:

```text
CustomerSegment
        ↓
Describes how customers should behave

Customer
        ↓
An individual generated from that profile
```

A useful analogy is a cookie cutter.

The `CustomerSegment` is the cookie cutter.

The individual customers are the cookies.

The cookie cutter defines the general shape, but every cookie can still be slightly different.

---

# 5. The `CustomerSegment` Class

The class contains the parameters required to generate customers.

Its structure is:

```python
@dataclass
class CustomerSegment:

    name: str
    weight: float

    age_mean: float
    age_std: float

    income_mean: float
    income_std: float

    late_payment_probabilities: Dict[int, float]

    utilization_alpha: float
    utilization_beta: float

    credit_history_mean: float
    credit_history_std: float

    credit_mix_probabilities: Dict[int, float]

    inquiries_lambda: float
```

The class groups all parameters related to a segment in one object.

This is an example of **encapsulation**.

Instead of having many independent variables:

```python
young_age_mean = 28
young_age_std = 4

young_income_mean = 10.5
young_income_std = 0.35

young_utilization_alpha = 2.5
young_utilization_beta = 4.0
```

We group them together:

```python
YOUNG_PROFESSIONAL.age_mean
YOUNG_PROFESSIONAL.income_mean
YOUNG_PROFESSIONAL.utilization_alpha
```

This makes the code easier to organize and maintain.

---

# 6. What Is a Distribution?

A probability distribution describes how likely different values are.

Imagine generating the age of a Young Professional.

We could simply say:

```text
Age = 28
```

But then every Young Professional would be 28 years old.

That would be unrealistic.

Instead, we say:

```text
Average age = 28
Variation = 4
```

Now the generator can produce:

```text
24
26
27
28
29
31
34
```

The values are not equally likely.

Values closer to the average are generally more common.

This is the basic idea behind a probability distribution.

---

# 7. Normal Distribution

The project uses the Normal Distribution for variables where values tend to cluster around an average.

The formula is commonly represented as:

[
X \sim N(\mu, \sigma^2)
]

Where:

* (\mu) = mean
* (\sigma) = standard deviation

In Python:

```python
rng.normal(
    loc=segment.age_mean,
    scale=segment.age_std
)
```

For example:

```python
age_mean = 28
age_std = 4
```

This means:

```text
Average age ≈ 28
Typical variation ≈ 4 years
```

The generator might produce:

```text
25
27
28
29
32
```

This does not mean every value is equally probable.

The distribution is concentrated around the mean.

The Normal Distribution is used for:

* Age
* Income parameters
* Credit history

---

# 8. Log-Normal Distribution for Income

Income is generated using a Log-Normal Distribution.

```python
rng.lognormal(
    mean=segment.income_mean,
    sigma=segment.income_std
)
```

This is useful because income is naturally:

* Positive
* Often right-skewed
* More likely to have a small number of very high-income individuals

A Normal Distribution could theoretically generate negative income values.

For example:

```text
$50,000
$60,000
$70,000
-$10,000
```

A negative annual income would not make sense for the simplified model.

The Log-Normal Distribution avoids this problem because its generated values are positive.

The important conceptual difference is:

```text
Normal Distribution

       /\ 
      /  \
_____/    \_____
```

Versus a right-skewed income distribution:

```text
       /\
      /  \
_____/    \___________
                  ↑
            Few high incomes
```

This makes the Log-Normal Distribution a reasonable educational choice for income.

---

# 9. Employment Years

Employment years are not generated independently of age.

This is an important example of **business logic constraints**.

The first step is:

```python
max_employment_years = max(age - 18, 1)
```

The assumption is that formal employment begins at approximately age 18.

Therefore:

```text
Age = 25

25 - 18 = 7
```

The customer can have at most approximately:

```text
7 years of employment
```

The generator then selects a random value between:

```text
1 and 7
```

For example:

```text
Age = 25
Employment Years = 3
```

Or:

```text
Age = 25
Employment Years = 6
```

But never:

```text
Age = 25
Employment Years = 30
```

This is an example of a **logical constraint**.

Probability generates the variability.

Business rules prevent impossible or unrealistic combinations.

This distinction is very important:

```text
Probability
    ↓
Creates realistic variation

Business Rules
    ↓
Prevent unrealistic combinations
```

Together they produce more realistic synthetic data.

---

# 10. Categorical Distribution: Late Payments

Late payments are generated using a categorical probability distribution.

For example:

```python
late_payment_probabilities = {
    0: 0.40,
    1: 0.27,
    2: 0.15,
    3: 0.09,
    4: 0.06,
    5: 0.03,
}
```

This means:

```text
0 late payments → 40% probability
1 late payment   → 27% probability
2 late payments  → 15% probability
3 late payments  → 9% probability
4 late payments  → 6% probability
5 late payments  → 3% probability
```

The generator uses:

```python
rng.choice(
    late_payment_values,
    p=late_payment_probabilities
)
```

Conceptually, this is similar to a weighted lottery.

The possible results are:

```text
[0, 1, 2, 3, 4, 5]
```

But the probability of selecting each value is different.

The important improvement in this project is that the probabilities are **segment-specific**.

For example:

```text
Young Professional
        ↓
Higher probability of late payments

Senior Professional
        ↓
Lower probability of late payments

High Income
        ↓
Lower probability of late payments
```

This means the model does not assume that every customer behaves identically.

However, the distributions do not imply that every High Income customer is financially responsible.

They only define probabilities.

Therefore, a High Income customer can still have late payments.

The difference is that the event is less probable.

This is an important concept in probabilistic modeling:

> A probability distribution describes likelihood, not certainty.

---

# 11. Beta Distribution: Credit Utilization

Credit utilization represents how much of the customer's available credit is currently being used.

For example:

```text
Credit Limit = $10,000
Current Balance = $3,000

Utilization = 30%
```

The generator uses a Beta Distribution:

```python
rng.beta(
    a=segment.utilization_alpha,
    b=segment.utilization_beta
)
```

The Beta Distribution always generates values between:

[
0 \leq X \leq 1
]

Therefore:

```text
0.00 = 0%
0.25 = 25%
0.50 = 50%
0.80 = 80%
1.00 = 100%
```

The project multiplies the result by 100:

```python
utilization * 100
```

So:

```text
0.35 → 35%
```

The parameters:

```python
alpha
beta
```

control the shape of the distribution.

For example:

```text
alpha = 2.5
beta = 4.0
```

will produce a different utilization profile from:

```text
alpha = 4.0
beta = 8.0
```

This allows different customer segments to have different credit utilization behaviors.

For example:

```text
Credit Builder
    ↓
Higher typical utilization

High Income
    ↓
Lower typical utilization
```

Again, this does not guarantee individual behavior.

It only changes the probabilities.

---

# 12. Credit History

Credit history represents approximately how many years a customer has had active credit experience.

The generator uses a Normal Distribution:

```python
generated_history = rng.normal(
    loc=segment.credit_history_mean,
    scale=segment.credit_history_std
)
```

However, this value cannot simply be accepted.

Consider:

```text
Age = 25
Generated Credit History = 15 years
```

That would imply the customer started using credit around:

```text
25 - 15 = 10 years old
```

This is unrealistic for our simplified model.

Therefore, we calculate:

```python
max_credit_history = max(age - 18, 1)
```

For:

```text
Age = 25
```

We get:

```text
25 - 18 = 7
```

The maximum possible credit history becomes:

```text
7 years
```

Then:

```python
credit_history = min(
    round(generated_history),
    max_credit_history
)
```

This means:

```text
Generated history = 12
Maximum realistic history = 7

Final history = 7
```

Or:

```text
Generated history = 4
Maximum realistic history = 7

Final history = 4
```

The `min()` function chooses the smaller value.

The final process is therefore:

```text
Probability Distribution
        ↓
Generate Estimated History
        ↓
Apply Age Constraint
        ↓
Final Credit History
```

This is another example of combining:

```text
Statistical Modeling
+
Business Logic
```

---

# 13. Credit Mix

Credit Mix represents the number of active credit products.

The project uses a categorical distribution.

For example:

```python
credit_mix_probabilities = {
    1: 0.35,
    2: 0.40,
    3: 0.20,
    4: 0.05,
}
```

The possible values are:

```text
1 credit product
2 credit products
3 credit products
4 credit products
```

The probabilities differ according to the customer segment.

A Credit Builder might be more likely to have:

```text
1 or 2 products
```

While a Senior Professional might be more likely to have:

```text
3 or 4 products
```

This variable later contributes to the customer's Credit Score and Probability of Default.

---

# 14. Recent Credit Inquiries

Recent inquiries represent how many recent credit applications or credit checks a customer has made.

The project uses a Poisson Distribution:

```python
rng.poisson(
    lam=segment.inquiries_lambda
)
```

The parameter:

[
\lambda
]

represents the expected average number of events.

For example:

```text
lambda = 0.7
```

means relatively few recent inquiries are expected.

While:

```text
lambda = 1.8
```

represents a customer profile with more frequent recent credit activity.

This is useful because credit inquiries are count data.

The variable is not:

```text
0.72 inquiries
```

It is:

```text
0 inquiries
1 inquiry
2 inquiries
3 inquiries
...
```

The Poisson Distribution is therefore a natural educational choice for modeling event counts.

---

# 15. Segment Selection

Before generating a customer, the system must determine which segment they belong to.

The process is:

```text
Customer
    ↓
Select Segment
    ↓
Use Segment Parameters
    ↓
Generate Customer Attributes
```

For example:

```text
Customer C00001
        ↓
Young Professional
        ↓
Age parameters from Young Professional
Income parameters from Young Professional
Credit behavior from Young Professional
```

Another customer could be:

```text
Customer C00002
        ↓
High Income
        ↓
Age parameters from High Income
Income parameters from High Income
Credit behavior from High Income
```

The segment selection itself is probabilistic.

The default portfolio uses:

```python
DEFAULT_SEGMENT_WEIGHTS = {
    "Young Professional": 0.30,
    "Established Professional": 0.30,
    "Senior Professional": 0.15,
    "High Income": 0.10,
    "Credit Builder": 0.15,
}
```

Conceptually:

```text
30% Young Professionals
30% Established Professionals
15% Senior Professionals
10% High Income
15% Credit Builders
```

For a portfolio of 1,000 customers, we would expect approximately:

```text
300 Young Professionals
300 Established Professionals
150 Senior Professionals
100 High Income
150 Credit Builders
```

However, because the process is probabilistic, the exact result may vary.

For example:

```text
298 Young Professionals
304 Established Professionals
147 Senior Professionals
103 High Income
148 Credit Builders
```

This is expected.

The probabilities define the expected distribution, not an exact quota.

---

# 16. Random Number Generator

The project uses:

```python
rng = np.random.default_rng(random_state)
```

This creates a NumPy random number generator.

The `random_state` parameter controls reproducibility.

For example:

```python
generate_customers(
    n_customers=1000,
    random_state=42
)
```

If the same seed is used again:

```python
generate_customers(
    n_customers=1000,
    random_state=42
)
```

the same synthetic portfolio will be generated.

This is important for:

* Debugging
* Testing
* Comparing model versions
* Reproducing experiments
* Educational demonstrations

The random seed does not eliminate randomness.

Instead, it makes the randomness **reproducible**.

---

# 17. The `generate_customer()` Function

The `generate_customer()` function is responsible for generating one customer.

The process is sequential.

```text
1. Select Segment
        ↓
2. Generate Age
        ↓
3. Generate Employment Years
        ↓
4. Generate Income
        ↓
5. Generate Late Payments
        ↓
6. Generate Credit Utilization
        ↓
7. Generate Credit History
        ↓
8. Generate Credit Mix
        ↓
9. Generate Recent Inquiries
        ↓
10. Return Customer
```

The function returns a Python dictionary:

```python
return {
    "Customer_ID": customer_id,
    "Segment": segment.name,
    "Age": age,
    "Employment_Years": employment_years,
    "Annual_Income": annual_income,
    "Late_Payments": late_payments,
    "Credit_Utilization": credit_utilization,
    "Credit_History_Years": credit_history_years,
    "Credit_Mix": credit_mix,
    "Recent_Inquiries": recent_inquiries
}
```

This dictionary represents one row of the final dataset.

For example:

```text
Customer_ID: C00001
Segment: Young Professional
Age: 27
Employment_Years: 5
Annual_Income: $42,000
Late_Payments: 1
Credit_Utilization: 54%
Credit_History_Years: 5
Credit_Mix: 2
Recent_Inquiries: 1
```

---

# 18. The `generate_customers()` Function

The `generate_customers()` function is the main orchestrator of the module.

An **orchestrator** is a function responsible for coordinating several smaller operations.

It does not calculate every attribute itself.

Instead, it coordinates the process:

```text
generate_customers()
        │
        ├── generate_customer()
        │       ├── generate_age()
        │       ├── generate_income()
        │       ├── generate_employment_years()
        │       ├── generate_late_payments()
        │       ├── generate_credit_utilization()
        │       ├── generate_credit_history()
        │       ├── generate_credit_mix()
        │       └── generate_recent_inquiries()
        │
        └── pandas.DataFrame()
```

The function repeats this process:

```python
for i in range(1, n_customers + 1):
```

Each customer receives a unique identifier:

```python
C00001
C00002
C00003
...
```

The generated dictionaries are stored in a list.

Finally:

```python
pd.DataFrame(customers)
```

converts the list of dictionaries into a DataFrame.

The result is the customer portfolio used by the rest of the application.

---

# 19. Module Architecture

The module follows a simple layered structure.

```text
CustomerSegment
        ↓
Segment Configuration
        ↓
Attribute Generators
        ↓
generate_customer()
        ↓
generate_customers()
        ↓
Pandas DataFrame
```

This design separates responsibilities.

For example:

```python
generate_age()
```

only generates age.

```python
generate_income()
```

only generates income.

```python
generate_credit_history()
```

only generates credit history.

This is an example of the **Single Responsibility Principle** at a simple educational level.

Each function has one main responsibility.

This makes the code easier to:

* Read
* Understand
* Test
* Modify
* Reuse

---

# 20. Why We Use Functions Instead of One Large Function

We could theoretically write everything inside:

```python
generate_customers()
```

For example:

```python
def generate_customers():

    # generate age
    # generate income
    # generate employment
    # generate late payments
    # generate utilization
    # ...
```

However, this would quickly become difficult to maintain.

Instead, we decompose the problem:

```text
generate_age()
generate_income()
generate_employment_years()
generate_late_payments()
generate_credit_utilization()
generate_credit_history()
generate_credit_mix()
generate_recent_inquiries()
```

Each function represents one piece of business logic.

This is called **modularity**.

The result is a system that is easier to understand and extend.

---

# 21. Relationship Between Probability and Business Rules

One of the most important concepts in this module is the combination of:

```text
Probability
+
Business Logic
```

Probability creates variation.

Business logic keeps the data realistic.

For example:

```text
Age
↓
Normal Distribution
↓
Age = 25
```

Then:

```text
Age = 25
↓
Employment Constraint
↓
Employment Years ≤ 7
```

Another example:

```text
Credit History
↓
Normal Distribution
↓
Generated History = 15 years
```

Then:

```text
Age = 25
↓
Maximum History = 7 years
↓
Final History = 7 years
```

The generator therefore follows the principle:

> Generate probabilistically, then validate against business reality.

This principle will become increasingly important when building the later credit risk modules.

---

# 22. Current Customer Data Model

The current generator produces the following variables:

| Variable               | Description                      | Purpose                            |
| ---------------------- | -------------------------------- | ---------------------------------- |
| `Customer_ID`          | Unique customer identifier       | Customer tracking                  |
| `Segment`              | Customer segment                 | Portfolio segmentation             |
| `Age`                  | Customer age                     | Demographic and lending context    |
| `Employment_Years`     | Years of employment              | Financial stability proxy          |
| `Annual_Income`        | Annual income in USD             | Affordability and lending capacity |
| `Late_Payments`        | Historical late payments         | Payment behavior                   |
| `Credit_Utilization`   | Percentage of credit used        | Credit stress indicator            |
| `Credit_History_Years` | Years of credit history          | Credit maturity                    |
| `Credit_Mix`           | Number of active credit products | Credit diversification             |
| `Recent_Inquiries`     | Recent credit inquiries          | Recent credit-seeking behavior     |

These variables are intentionally limited.

The objective is not to simulate an entire bank database.

The objective is to create a compact but realistic dataset that is sufficient for:

```text
Credit Score
        ↓
Probability of Default
        ↓
Risk Classification
        ↓
Credit Decision
        ↓
Loan Amount
```

This keeps the project manageable while still demonstrating financial and risk analytics concepts.

---

# 23. Future Sandbox Integration

The current version uses predefined segment configurations.

For example:

```python
YOUNG_PROFESSIONAL
ESTABLISHED_PROFESSIONAL
SENIOR_PROFESSIONAL
HIGH_INCOME
CREDIT_BUILDER
```

The future sandbox will allow the user to modify the portfolio.

For example:

```text
Young Professional
[=========---------] 40%

Established Professional
[======------------] 25%

Senior Professional
[====--------------] 15%

High Income
[==----------------] 5%

Credit Builder
[======------------] 15%
```

The user could therefore simulate different portfolio compositions.

For example:

```text
Scenario A
More Young Professionals

Scenario B
More High Income Customers

Scenario C
More Credit Builders

Scenario D
More Senior Professionals
```

The same customer generation engine will then generate the portfolio under the new configuration.

This is one of the reasons the segment configuration is separated from the generation logic.

The architecture is designed so that:

```text
Segment Parameters
        ↓
Can be modified
        ↓
Without rewriting
the generation functions
```

This will be particularly important in **v1.3**, when the Streamlit Sandbox is implemented.

---

# 24. Complete Conceptual Flow

The entire customer generation process can be summarized as:

```text
                 CUSTOMER GENERATOR
                         │
                         ▼
              Select Customer Segment
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
    Segment Parameters            Probability Rules
          │                             │
          └──────────────┬──────────────┘
                         ▼
                 Generate Attributes
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
      Normal          Log-Normal        Beta
        │                │                │
       Age             Income        Utilization
        │
        ├── Business Constraints
        │
        ▼
  Employment Years
        │
        ▼
  Credit History
        │
        ├── Categorical
        │
        ▼
  Late Payments
        │
        ▼
  Credit Mix
        │
        ├── Poisson
        │
        ▼
 Recent Inquiries
        │
        ▼
  Customer Record
        │
        ▼
    DataFrame
        │
        ▼
Credit Risk Analytics Pipeline
```

---

# 25. Key Concepts Learned

By studying and implementing this module, the following concepts are introduced:

### Python

* Functions
* Type hints
* Dictionaries
* Lists
* DataFrames
* Modules
* Imports

### Object-Oriented Programming

* Classes
* Objects
* Dataclasses
* Encapsulation
* Object attributes

### Probability

* Random variables
* Probability distributions
* Normal Distribution
* Log-Normal Distribution
* Beta Distribution
* Categorical Distribution
* Poisson Distribution

### Data Generation

* Synthetic data
* Random number generation
* Reproducibility
* Segment-based simulation

### Data Engineering

* Data validation through business rules
* Modular functions
* DataFrame construction
* Separation of responsibilities

### Financial Analytics

* Customer segmentation
* Credit behavior
* Credit utilization
* Credit history
* Payment behavior
* Credit inquiries

---

# 26. Final Mental Model

The most important way to understand the `customer_generator.py` module is:

```text
Customer Segment
    ↓
Defines the customer's general profile

Probability Distribution
    ↓
Creates realistic variation

Business Rule
    ↓
Prevents unrealistic combinations

Individual Customer
    ↓
Receives a unique combination of attributes

DataFrame
    ↓
Becomes the input for the credit risk pipeline
```

The generator does not try to predict whether a customer will default.

It creates the population that later models will analyze.

Therefore:

> The Customer Generator creates the world.

The next modules analyze that world.

The complete project will eventually follow:

```text
WORLD
Customer Generator
        ↓
MEASUREMENT
Credit Score
        ↓
PREDICTION
Probability of Default
        ↓
RISK
Risk Classification
        ↓
DECISION
Approval / Rejection / Manual Review
        ↓
LENDING
Loan Amount
```

This separation is fundamental to the architecture of the Credit Risk Analytics Suite.

---