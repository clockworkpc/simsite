# Pastebin Architecture Diagram

## Stage 0: Initial Diagram and Adding Storage

### ✅ Initial Setup

```mermaid
graph TD
    client[🧑‍💻 Client]
    web[🌐 Web Server]
    client <-->|GET| web
    client -->|POST| web
    readwriteapi[📝 Read/Write API]
    web <-->|READ| readwriteapi
    web -->|WRITE| readwriteapi
```

## Stage 1: Persisting Data

### ❌ Using Redis Cache

```mermaid
graph TD
    client[🧑‍💻 Client]
    web[🌐 Web Server]
    client <-->|GET| web
    client -->|POST| web
    readwriteapi[📝 Read/Write API]
    web <-->|READ| readwriteapi
    web -->|WRITE| readwriteapi
    redis[🗃️ Redis Cache]
    readwriteapi <-->|READ| redis
    readwriteapi -->|WRITE| redis
```

### ❌ Use Local Storage

```mermaid
graph TD
    client[🧑‍💻 Client]
    web[🌐 Web Server]
    client <-->|GET| web
    client -->|POST| web
    readwriteapi[📝 Read/Write API]
    web <-->|READ| readwriteapi
    web -->|WRITE| readwriteapi
    localstorage[💾 Local Storage]
    readwriteapi <-->|READ| localstorage
    readwriteapi -->|WRITE| localstorage
```

### ✅ Add SQL database

#### Single SQL Database

```mermaid
graph TD
    client[🧑‍💻 Client]
    web[🌐 Web Server]
    client <-->|GET| web
    client -->|POST| web
    readwriteapi[📝 Read/Write API]
    web <-->|READ| readwriteapi
    web -->|WRITE| readwriteapi
    subgraph sqldb[SQL Database]
        sqlmaster[🗄️ SQL Database Master]
        sqlslave[🗄️ SQL Database Slave]
    end
    sqlmaster -->|WRITE| sqlslave
    readwriteapi -->|WRITE| sqldb
    readwriteapi <-->|READ| sqldb
    sqlmaster
```

#### Relational Database Management System (RDBMS)

##### Master-Slave Replication


## Stage 2: Improve Write Request Performance

### ❌ Add more web servers

```mermaid
graph TD
    client[🧑‍💻 Client]
    loadbalancer[⚖️ Load Balancer]
    web1[🌐 Web Server]
    web2[🌐 Web Server]
    web3[🌐 Web Server]
    client <-->|GET| loadbalancer
    client -->|POST| loadbalancer
    loadbalancer <-->|GET| web1
    loadbalancer -->|POST| web1
    loadbalancer <-->|GET| web2
    loadbalancer -->|POST| web2
    loadbalancer <-->|GET| web3
    loadbalancer -->|POST| web3
    readwriteapi1[📝 Read/Write API]
    readwriteapi2[📝 Read/Write API]
    readwriteapi3[📝 Read/Write API]
    web1 <-->|READ| readwriteapi1
    web1 -->|WRITE| readwriteapi1
    web2 <-->|READ| readwriteapi2
    web2 -->|WRITE| readwriteapi2
    web3 <-->|READ| readwriteapi3
    web3 -->|WRITE| readwriteapi3
    sql[🗄️ SQL Database]
    readwriteapi1 <-->|READ| sql
    readwriteapi1 -->|WRITE| sql
    readwriteapi2 <-->|READ| sql
    readwriteapi2 -->|WRITE| sql
    readwriteapi3 <-->|READ| sql
    readwriteapi3 -->|WRITE| sql
```

### ❌ Add client-side caching

```mermaid
graph TD
    client[🧑‍💻 Client]
    web[🌐 Web Server]
    client <-->|GET| web
    client -->|POST| web
    readwriteapi[📝 Read/Write API]
    web <-->|READ| readwriteapi
    web -->|WRITE| readwriteapi
    sql[🗄️ SQL Database]
    readwriteapi <-->|READ| sql
    readwriteapi -->|WRITE| sql
```

### ✅ Add Read API and Write API

```mermaid
graph TD
    client[🧑‍💻 Client]
    web[🌐 Web Server]
    client <-->|GET| web
    client -->|POST| web
    readapi[📝 Read API]
    writeapi[📝 Write API]
    web <-->|READ| readapi
    web -->|WRITE| writeapi
    sql[🗄️ SQL Database]
    readapi <-->|READ| sql
    writeapi -->|WRITE| sql
```

## Stage 3: Improve Read Request Performance

```mermaid
graph TD
    client[🧑‍💻 Client]
    web[🌐 Web Server]
    client <-->|GET| web
    client -->|POST| web
    readapi[📝 Read API]
    writeapi[📝 Write API]
    web <-->|READ| readapi
    web -->|WRITE| writeapi
    localstorage[💾 Local Storage]
    readapi <-->|READ| localstorage
    writeapi -->|WRITE| localstorage
```

































## Stage 3: 

```mermaid
graph TD
    %% Stage 0
    client[🧑‍💻 Client]
    web[🌐 Web Server]
    client <-->|GET| web
    client -->|POST| web


    client --> |pastebin.com| dns
    dns[📡 DNS]
    write[✍️ Write API]
    read[📖 Read API]
    cdn[🚀 CDN]
    analytics[📊 Analytics]
    sql[🗄️ SQL]
    objectstore[🧺 Object Store]

    dns -->|104.22.68.199| client
    client <-->|GET| cdn
    web .->|POST| write
    web <-->|GET| read
    sql <-->|READ| analytics
    objectstore <-->|READ| analytics
    write -->|WRITE| sql
    write -->|WRITE| objectstore
    read <-->|READ| sql
    read <-->|READ| objectstore
```

