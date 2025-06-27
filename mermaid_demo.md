# Pastebin Architecture Diagram

## Stage 0: Initial Diagram and Adding Storage

### ✅ Initial Setup

```mermaid
graph TD
    client[🧑‍💻 Client]
    web[🌐 Web Server]
    client -->|POST| web
    client <-->|GET | web

    readwriteapi[📝 Read/Write API]
    web -->|WRITE| readwriteapi
    web <-->|READ| readwriteapi

    webmemory[🧠 Web Server Memory]
    readwriteapi -->|WRITE| webmemory
    readwriteapi -->|READ| webmemory
```

## Stage 1: Persisting Data

<div style="display: flex; gap: 1em;">

  <div style="flex: 1; border: 1px solid #ccc; padding: 1em;">
    
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
    redis[❌ 🗃️ Redis Cache]
    readwriteapi <-->|READ| redis
    readwriteapi -->|WRITE| redis
```
  </div>
  <div style="flex: 1; border: 1px solid #ccc; padding: 1em;">
    
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
    localstorage[❌ 💾 Local Storage]
    readwriteapi <-->|READ| localstorage
    readwriteapi -->|WRITE| localstorage
```
  </div>
</div>


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
    sql[❌ 🗄️ SQL DB]
    readwriteapi -->|WRITE| sql
    readwriteapi <-->|READ| sql
```

#### Relational Database Management System (RDBMS)


##### Master-Master Replication

```mermaid
graph TD
    client[🧑‍💻 Client]
    web[🌐 Web Server]
    client <-->|GET| web
    client -->|POST| web

    readwriteapi[📝 Read/Write API]
    web <-->|READ| readwriteapi
    web -->|WRITE| readwriteapi

    subgraph sqldb[✅ RDBMS]
        loadbalancer[❌ ⚖️ DB Load Balancer]
        sql1[(🗄️ DB Master 1)]
        sql2[(🗄️ DB Master 2)]
    end

    readwriteapi <-->|R/W| loadbalancer
    readwriteapi <-->|R/W| loadbalancer
    loadbalancer <-->|R/W| sql1
    loadbalancer <-->|R/W| sql2
```

##### Master-Slave Replication

```mermaid
graph TD
    client[🧑‍💻 Client]
    web[🌐 Web Server]
    client <-->|GET| web
    client -->|POST| web

    readwriteapi[📝 Read/Write API]
    web <-->|READ| readwriteapi
    web -->|WRITE| readwriteapi

    subgraph sqldb[ ✅ RDBMS]
        sqlmaster[(🗄️ SQL Database Master)]
        sqlslave[(🗄️ SQL Database Slave)]
    end

    readwriteapi -->|WRITE| sqlmaster
    readwriteapi <-->|READ| sqlslave
    sqlmaster -->|WRITE| sqlslave
```


## Stage 2: Improve Write Request Performance

### ❌ Add more web servers

```mermaid
graph TD
    client[🧑‍💻 Client]
    loadbalancer[❌ ⚖️ Load Balancer]
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

    dbloadbalancer[❌ ⚖️ DB Load Balancer]

    subgraph sql[RDBMS]
        sqlmaster[(🗄️ SQL Database Master)]
        sqlslave[(🗄️ SQL Database Slave)]
    end

    sqlmaster -->|WRITE| sqlslave

    readwriteapi1 <-->|READ| dbloadbalancer
    readwriteapi1 -->|WRITE| dbloadbalancer
    readwriteapi2 <-->|READ| dbloadbalancer
    readwriteapi2 -->|WRITE| dbloadbalancer
    readwriteapi3 <-->|READ| dbloadbalancer
    readwriteapi3 -->|WRITE| dbloadbalancer
    dbloadbalancer -->|WRITE| sqlmaster
    dbloadbalancer <-->|READ| sqlslave

```

### ❌ Add client-side caching

```mermaid
graph TD
    client[🧑‍💻 Client]
    cache[❌ 🗃️ Client Cache]
    web[🌐 Web Server]
    client <-->|GET| web
    client -->|POST| web
    client <-->|R/W| cache

    readwriteapi[📝 Read/Write API]
    web <-->|READ| readwriteapi
    web -->|WRITE| readwriteapi

    subgraph sql[ RDBMS]
        sqlmaster[(🗄️ SQL Database Master)]
        sqlslave[(🗄️ SQL Database Slave)]
    end

    readwriteapi <-->|READ| sql
    readwriteapi -->|WRITE| sql
    sqlmaster -->|WRITE| sqlslave
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

    subgraph sqldb[ ✅ RDBMS]
        sqlmaster[(🗄️ SQL Database Master)]
        sqlslave[(🗄️ SQL Database Slave)]
    end

    writeapi -->|WRITE| sqlmaster
    readapi <-->|READ| sqlslave
    sqlmaster -->|WRITE| sqlslave
```


## Stage 3: Improve Read Request Performance

### ❌ Add SQL Master for Read API

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

    subgraph sqldb[ ✅ RDBMS]
        sqlmaster[(🗄️ SQL Database Master)]
        sqlslave[(🗄️ SQL Database Slave)]
    end

    writeapi -->|WRITE| sqlmaster
    readapi <-->|❌ READ| sqlmaster
    sqlmaster -->|WRITE| sqlslave
```

### ❌ Use file system for Read API

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

    subgraph sqldb[ ✅ RDBMS]
        sqlmaster[(🗄️ SQL Database Master)]
        sqlslave[(🗄️ SQL Database Slave)]
    end

    filesystem[📂 File System]

    sqlmaster -->|WRITE| filesystem
    writeapi -->|WRITE| sqlmaster
    readapi <-->|❌ READ| filesystem
    sqlmaster -->|WRITE| sqlslave
```

### ✅ Add SQL Replicas for Read API
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

    subgraph sqldb[ ✅ RDBMS]
        sqlmaster[(🗄️ SQL Database Master)]
        sqlslave1[(🗄️ SQL Database Slave)]
        sqlslave2[(🗄️ SQL Database Slave)]
        sqlslave3[(🗄️ SQL Database Slave)]
    end

    dbloadbalancer[ ⚖️ DB Load Balancer]

    writeapi -->|WRITE| sqlmaster
    readapi <-->|READ| dbloadbalancer


    dbloadbalancer <-->|READ| sqlslave1
    dbloadbalancer <-->|READ| sqlslave2
    dbloadbalancer <-->|READ| sqlslave3

    sqlmaster -->|WRITE| sqlslave1
    sqlmaster -->|WRITE| sqlslave2
    sqlmaster -->|WRITE| sqlslave3
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

