```markdown
graph TD
  %% Global Infra
  subgraph infra [🌐 Global Infra]
    USER[🧑‍💻 Customers]
    DNS[🌐 DNS]
    LB[⚖️ Load Balancer]
  end

  %% Credit Scoring Flow
  subgraph scoring [📊 Credit Scoring]
    WAF[🛡️ WAF]
    AUTH[🔐 Auth]
    GATEWAY[📌 Gateway]
    PROFILE[👤 Profile]
    HISTORY[📜 History]
    ENGINE[🧠 Scoring]
    APPROVE[✅ Approve]
    WRITE[📒 Ledger]
    STREAM[📡 Events]
  end

  %% ML & Analytics
  subgraph ml [🧠 ML & Analytics]
    HIST[🗄️ Hist Data]
    FEAT[📊 Features]
    TRAIN[🔁 Train]
    SERVE[🚀 Serve]
    EXPLAIN[🔍 Explain]
  end

  %% DB
  subgraph db [🗄️ Storage]
    MASTER[(📒 Master DB)]
    REPLICA[(📒📒 Replicas)]
    DBLB[⚖️ DB LB]
  end

  %% Monitoring
  subgraph mon [📈 Monitoring]
    LOG[📜 Logs]
    DASH[📊 Dashboard]
  end

  %% Flow
  USER --> DNS --> LB --> WAF --> AUTH --> GATEWAY
  GATEWAY --> PROFILE & HISTORY & ENGINE
  ENGINE --> SERVE & EXPLAIN & APPROVE
  APPROVE --> WRITE --> MASTER -->|🔁| REPLICA
  DBLB --> REPLICA
  WRITE --> STREAM --> FEAT --> TRAIN --> SERVE
  HIST --> FEAT

  ENGINE --> LOG
  APPROVE --> LOG
  LOG --> DASH
```

```markdown
graph TD
	%% Subgraph: Global Nodes
	subgraph global [🌐 Global Infrastructure]
        subgraph clients[🧑‍💻 Customers 🇺🇸 🇪🇺 🇮🇱 🇯🇵]
            us_customer[🧑‍💻 Customer 🇺🇸]
            eu_customer[🧑‍💻 Customer 🇪🇺]
            il_customer[🧑‍💻 Customer 🇮🇱]
            jp_customer[🧑‍💻 Customer 🇯🇵]
        end
        geodns[🌐 Geo-aware DNS]
        globallb[⚖️ Global Load Balancer]
	end

    %% Regional Application Stack
    subgraph regions[Regions - USA, EU, etc]
        subgraph credit_scoring[📊 Credit Scoring & Approval 🇺🇸 🇪🇺 🇮🇱 🇯🇵]
            waf[🛡️ WAF / Rate Limiter]
            authservice[🔐 Auth Service]
            scoring_gateway[📌 Scoring Gateway]
            credit_profile_service[👤 Credit Profile Service]
            transaction_history_service[📜 Transaction History Service]
            scoring_engine[🧠 Scoring Engine]
            approval_engine[✅ Approval Engine]
            db_write[📒 Credit Ledger]
            event_stream[📡 Event Streaming Platform]
        end
    end

	%% ML & Analytics
	subgraph ml_analytics[🧠 ML & Analytics]
		historical_data_store[🗄️ Historical Credit Data]
		feature_store[📊 Feature Store]
		model_training[🔁 Model Training]
		model_serving[🚀 Model Serving]
		explainability_service[🔍 Explainability Service]
	end

    %% Storage Layer
	subgraph storage[✅ Data Storage]
		credit_db_master[(📒 Credit DB Master)]
        credit_db_replicas[(📒📒📒 DB Replicas)]
		db_load_balancer[⚖️ Replica Load Balancer]
	end

	%% Monitoring
	subgraph observability[🧭 Observability]
        logcollector[📜 Log Collector]
        monitoring_dashboard[📊 Monitoring Dashboard]
	end

	%% Traffic Flow
	clients -->|Credit Application 📝| geodns
	geodns --> globallb
    globallb -->|Route Request| waf

    waf --> authservice
    authservice --> scoring_gateway

    scoring_gateway --> credit_profile_service
    scoring_gateway --> transaction_history_service
    scoring_gateway --> scoring_engine

    scoring_engine --> model_serving
    scoring_engine --> explainability_service
    scoring_engine --> approval_engine

    approval_engine --> db_write
    db_write --> credit_db_master
    credit_db_master -->|Replication 🔁| credit_db_replicas
    db_load_balancer --> credit_db_replicas

    db_write --> event_stream
    event_stream --> feature_store

    feature_store --> model_training
    model_training --> model_serving
    historical_data_store --> feature_store

	%% Logging and Monitoring
	approval_engine --> logcollector
	scoring_engine --> logcollector
	logcollector --> monitoring_dashboard
```

<div style="page-break-after: always;"></div>

## Detailed Explanation of the Design and Decisions

 1. **Global Infrastructure:**
 - Ensures low latency and geographic redundancy for credit scoring operations.

 2. **Application Stack:**
 - WAF protects against abuse and enforces rate limits.
 - Auth Service ensures identity is verified before sensitive data is accessed.
 - Scoring Gateway routes input data to appropriate microservices for profile, transaction history, and scoring logic.
 - Scoring Engine integrates real-time features and calls model_serving for prediction.
 - Approval Engine makes automated credit decisions based on model output and business rules.
 - Event Stream captures all activities for downstream analytics and compliance.

 3. **ML & Analytics:**
 - Historical Data is processed into a Feature Store.
 - Model Training occurs continuously and updates the models used by Model Serving.
 - Explainability Service provides transparency into automated decisions to satisfy regulatory and user-facing requirements.

 4. **Storage Layer:**
 - High availability and data integrity are preserved through a master-replica DB setup and load balancing.

 5. **Monitoring and Observability:**
 - Logs and dashboards provide visibility into system performance, fairness metrics, and potential model drift.

<div style="page-break-after: always;"></div>

## Questions and Answers

### 1. What components would you include for assessing creditworthiness?

- **Credit Profile Service** to gather static information like identity, income, employment.
- **Transaction History Service** to assess payment behavior and obligations.
- **Scoring Engine** powered by real-time features and ML models.
- **Approval Engine** combining score, thresholds, and rules to decide outcomes.
- **Explainability Service** for transparency into decisions.

### 2. How do you handle the large volume of historical and real-time data?

- Use a **Feature Store** to serve both real-time and batch features efficiently.
- **Event streaming** allows fast ingestion of application and transaction events.
- Separate pipelines for training (batch) and inference (real-time) allow scalable and performant data flow.

### 3. What are the considerations for accuracy, fairness, and explainability?

- Use **balanced datasets** and fairness-aware modeling techniques (e.g., reweighing, adversarial debiasing).
- Regularly **audit model output** by demographic slices.
- Provide **model interpretability** via SHAP/LIME integrated in the Explainability Service.
- **Human-in-the-loop reviews** for borderline or adverse decisions.
