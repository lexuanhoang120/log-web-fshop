# Log Web Analysis (`log-web-fshop`)

This repository contains notebooks and utilities for web-log analysis, including user behavior and sequence pattern analysis.

> Note: This document is a summary from the project report: **Web Behavior Analytics, Customer Journey Mapping & Exit-Intent Prediction**.

## Data Source

Raw web logs for this project were collected from:

- https://fptshop.com.vn/

## Visuals

Figures stored in `docs/`:

### Methodology

![Methodology](docs/methodology.png)

### Processing Flow

![Processing Flow](docs/processing-flow.png)

### Data Processing Pipeline

![Data Processing Pipeline](docs/data-processing-pipeline.png)

### Journey Mapping

![Journey Mapping](docs/journey.png)

### Top 15 Group Actions

![Top 15 Group Actions](docs/top-15-group-action.png)

### Top 5 Most Popular Actions

![Top 5 Most Popular Actions](docs/top-5-most-popular-action.png)

### Percentage of Actions

![Percentage of Actions](docs/the-percentage-of-actions.png)

## Project Overview

Conducted an end-to-end web behavior analytics project for a large-scale e-commerce platform to understand customer intent, identify drop-off behavior, and propose real-time personalization opportunities.

The project combined market research, clickstream analysis, customer journey mapping, behavioral segmentation, and exit-intent prediction. The analysis was based on approximately 96M raw web behavior logs collected over a 3-month period and transformed into structured user journeys for session-level analysis and predictive use cases.

## Business Context

The project focused on three key questions:

- Which users are likely to purchase?
- Which users are likely to leave without converting?
- What real-time action should be triggered based on user intent?

Business applications included:

- In-session purchase-intent prediction.
- Exit-risk detection and intervention.
- High-conversion channel/campaign/category identification.
- Personalized offers, exit popups, cross-sell, upsell, and recommendation triggers.
- Targeted intervention to reduce broad promotions and protect margin.

## My Contribution

- Reviewed market research and case studies on clickstream analytics, in-session marketing, purchase intent, exit intent, and UX optimization.
- Defined key analytics directions for conversion analysis, recommendation strategy, clickstream UX improvement, and exit-intent intervention.
- Processed approximately 96M raw logs into around 93M valid labeled logs and approximately 32.5M valid sessions.
- Built a rule-based action-labeling framework to map URLs/events into 20 meaningful actions.
- Built journey mapping from `log -> action -> phase -> session`.
- Classified actions into 5 customer journey phases: Awareness, Consideration, Decision, Consumption, and Loyalty.
- Segmented sessions into Information Seekers, Product Explorers, and Shoppers.
- Built and evaluated a rule-based exit-intent prediction approach versus a random baseline.

## Methodology

### 1. Web Behavior Research

- Conversion optimization: purchase likelihood prediction.
- Recommendation opportunities: cross-sell, upsell, next-best content/product.
- Clickstream analysis: interest points, drop-off points, UX friction.

### 2. Data Cleaning and Preprocessing

- Removed duplicate, invalid, error, service, and irrelevant logs.
- Removed null/unclassified actions.
- Computed action time gaps and reconstructed sessions by inactivity threshold.
- Recomputed session and action durations after cleaning.
- Extracted product category/type, brand, source channel, and campaign features.

Resulting dataset scale:

- Approximately 96M raw logs.
- Around 93M valid labeled logs.
- Approximately 32.5M valid sessions.

### 3. Action Labeling

Mapped raw URLs and event labels to 20 user actions, including:

- Homepage visit
- Product search
- Product listing view
- Product detail view
- Promotion check
- Cart check
- Add to cart
- Installment view
- Payment
- Purchase
- Warranty check
- Order tracking
- Account check

### 4. Journey Mapping

Journey structure:

- `log -> action -> phase -> session`

Journey phases:

- Awareness
- Consideration
- Decision
- Consumption
- Loyalty

### 5. Behavioral Segmentation

- Information Seekers: 25.04% of traffic.
- Product Explorers: 69.65% of traffic.
- Shoppers: 3.87% of traffic.

### 6. Exit-Intent Prediction

- Built journey patterns from historical sessions and identified exit patterns.
- Created step-level records and predicted exit at each step.
- Compared rule-based method against random baseline.

Dataset scale for exit-intent prediction:

- Approximately 32.5M sessions.
- 32.2M training sessions.
- 325K testing sessions.
- 3M exit patterns (1-10 logs).
- 924K evaluated steps from 325K test sessions.

## Key Insights

- Only around 2.8% of approximately 32.5M valid sessions contained purchase-related behavior.
- Most purchase-related actions occurred between the 2nd and 5th action.
- More than 90% of sessions lasted 0-5 minutes.
- More than 50% of average page dwell time was 0-15 seconds; around 90% of sessions had average dwell under 3 minutes.
- Peak traffic windows were 9-11, 14-16, and 19-21 (approximately 54% of traffic).
- Consideration accounted for 77.23% of traffic; Decision accounted for 2.62%.
- Product interest was concentrated in smartphones (approximately 58%) and laptops (approximately 24%).
- Users typically viewed 1-5 products per session (98.7% of product-viewing sessions).
- Search contributed nearly 50% of first-session entries; direct contributed around 20%.
- Session duration by segment: Shoppers 297s, Product Explorers 98s, Information Seekers 0.9s.
- Sessions with 2-5 phases represented 70.8% of purchase sessions.
- Sessions with 6+ phases had the highest purchase-session rate at 58.33%.

## Exit-Intent Prediction Results

Step-level:

- Rule-based precision: 62.9%
- Rule-based recall: 58.9%
- Rule-based F1-score: 60.8%
- Random baseline precision: 35.2%
- Random baseline recall: 50.0%
- Random baseline F1-score: 41.3%

Session-level:

- Rule-based precision: 68.3%
- Rule-based recall: 65.6%
- Rule-based F1-score: 66.9%
- Random baseline precision: 46.4%
- Random baseline recall: 50.0%
- Random baseline F1-score: 48.1%

Stability:

- Two-sample stability checks showed differences below approximately 1.1%.

## Business Recommendations

- Prioritize intervention in the first 0-5 minutes of each session.
- Trigger real-time actions from early high-intent signals (search, repeated product-detail views, cart/payment events).
- Focus interventions on Product Explorers and Shoppers instead of broad promotion to all users.
- Segment by purchase probability: low, medium, high.
- Trigger exit-intent interventions: popup, reminder, sign-up prompt, recommendation, social proof, navigation support.
- Run campaign timing/tests in peak traffic windows: 9-11, 14-16, 19-21.
- Combine current-session behavior with historical activity for stronger intent prediction.
- Use journey data to reduce UX friction in navigation, content placement, and checkout flow.
