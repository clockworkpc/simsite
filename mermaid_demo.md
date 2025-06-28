# Pastebin Architecture Diagram

## Initial Diagram and Adding Storage

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

## Persisting Data

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


## Improve Write Request Performance

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


## Improve Read Request Performance

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

## Handle large files and blobs

### ❌ Encode large files as Base64 and store in SQL DB

```mermaid
graph TD
    client[🧑‍💻 Client]
    web[🌐 Web Server]
    client <-->|GET| web
    client -->|POST| web
    client -->|POST big files| web

    readapi[📝 Read API]
    writeapi[📝 Write API]

    web <-->|READ| readapi
    web -->|WRITE| writeapi
    web -->|WRITE big files| writeapi

    subgraph sqldb[ ✅ RDBMS]
        sqlmaster[(🗄️ SQL Database Master)]
        sqlslave1[(🗄️ SQL Database Slave)]
        sqlslave2[(🗄️ SQL Database Slave)]
        sqlslave3[(🗄️ SQL Database Slave)]
    end

    dbloadbalancer[ ⚖️ DB Load Balancer]

    writeapi -->|WRITE| sqlmaster
    writeapi -->|❌ WRITE base64| sqlmaster
    readapi <-->|READ| dbloadbalancer

    dbloadbalancer <-->|READ| sqlslave1
    dbloadbalancer <-->|READ| sqlslave2
    dbloadbalancer <-->|READ| sqlslave3

    sqlmaster -->|WRITE| sqlslave1
    sqlmaster -->|WRITE| sqlslave2
    sqlmaster -->|WRITE| sqlslave3

    sqlmaster -->|❌WRITE base64| sqlslave1
    sqlmaster -->|❌WRITE base64| sqlslave2
    sqlmaster -->|❌WRITE base64| sqlslave3
```

### ❌ Compress large files with GZip and store in SQL DB

```mermaid
graph TD
    client[🧑‍💻 Client]
    web[🌐 Web Server]
    client <-->|GET| web
    client -->|POST| web
    client -->|POST big files| web

    readapi[📝 Read API]
    writeapi[📝 Write API]

    web <-->|READ| readapi
    web -->|WRITE| writeapi
    web -->|WRITE big files| writeapi

    subgraph sqldb[ ✅ RDBMS]
        sqlmaster[(🗄️ SQL Database Master)]
        sqlslave1[(🗄️ SQL Database Slave)]
        sqlslave2[(🗄️ SQL Database Slave)]
        sqlslave3[(🗄️ SQL Database Slave)]
    end

    dbloadbalancer[ ⚖️ DB Load Balancer]

    writeapi -->|WRITE| sqlmaster
    writeapi -->|❌ WRITE GZIP| sqlmaster
    readapi <-->|READ| dbloadbalancer

    dbloadbalancer <-->|READ| sqlslave1
    dbloadbalancer <-->|READ| sqlslave2
    dbloadbalancer <-->|READ| sqlslave3

    sqlmaster -->|WRITE| sqlslave1
    sqlmaster -->|WRITE| sqlslave2
    sqlmaster -->|WRITE| sqlslave3

    sqlmaster -->|❌WRITE GZIP| sqlslave1
    sqlmaster -->|❌WRITE GZIP| sqlslave2
    sqlmaster -->|❌WRITE GZIP| sqlslave3
```

### ✅ Use Object Store for large files and blobs

```mermaid
graph TD
    client[🧑‍💻 Client]

    subgraph web[🌐 Web Server]
        frontend[🖼️ Front End]
        subgraph backend[🖥️ Back End]
            readapi[📖 Read API]
            writeapi[✏️ Write API]
        end
    end

    client <-->|📄🟣| frontend
    frontend <-->|GET 📄🟣| readapi
    frontend -->|POST 📄🟣| writeapi


    subgraph sqldb[ ✅ RDBMS]
        dbloadbalancer[ ⚖️ DB Load Balancer]
        sqlmaster[(🗄️ SQL Database Master 📄📄📄)]
        sqlslave1[(🗄️ SQL Database Slave 📄📄📄)]
        sqlslave2[(🗄️ SQL Database Slave 📄📄📄)]
        sqlslave3[(🗄️ SQL Database Slave 📄📄📄)]
    end

    writeapi -->|WRITE 📄| sqlmaster

    readapi <-->|READ 📄| dbloadbalancer

    dbloadbalancer <-->|READ 📄| sqlslave1
    dbloadbalancer <-->|READ 📄| sqlslave2
    dbloadbalancer <-->|READ 📄| sqlslave3

    sqlmaster -->|WRITE 📄| sqlslave1
    sqlmaster -->|WRITE 📄| sqlslave2
    sqlmaster -->|WRITE 📄| sqlslave3

    objectstore[🧺 Object Store 🟣🟣🟣]
    writeapi -->|WRITE 🟣| objectstore
    readapi <-->|READ 🟣| objectstore
```

## Improve Static Content Delivery

### ❌ Add more web servers

```mermaid
graph TD
    client[🧑‍💻 Client]

    subgraph web[🌐 Web Server]
        frontend[🖼️ Front End]
        subgraph backend[🖥️ Back End]
            readapi[📖 Read API]
            writeapi[✏️ Write API]
        end
    end

    client <-->|📄🟣| frontend
    frontend <-->|GET 📄🟣| readapi
    frontend -->|POST 📄🟣| writeapi


    subgraph sqldb[ ✅ RDBMS]
        dbloadbalancer[ ⚖️ DB Load Balancer]
        sqlmaster[(🗄️ SQL Database Master 📄📄📄)]
        sqlslave1[(🗄️ SQL Database Slave 📄📄📄)]
        sqlslave2[(🗄️ SQL Database Slave 📄📄📄)]
        sqlslave3[(🗄️ SQL Database Slave 📄📄📄)]
    end

    writeapi -->|WRITE 📄| sqlmaster

    readapi <-->|READ 📄| dbloadbalancer

    dbloadbalancer <-->|READ 📄| sqlslave1
    dbloadbalancer <-->|READ 📄| sqlslave2
    dbloadbalancer <-->|READ 📄| sqlslave3

    sqlmaster -->|WRITE 📄| sqlslave1
    sqlmaster -->|WRITE 📄| sqlslave2
    sqlmaster -->|WRITE 📄| sqlslave3

    objectstore[🧺 Object Store 🟣🟣🟣]
    writeapi -->|WRITE 🟣| objectstore
    readapi <-->|READ 🟣| objectstore
```

### ❌ Cache static files in client browser

```mermaid
graph TD
    client[🧑‍💻 Client]

    subgraph web[🌐 Web Server]
        frontend[🖼️ Front End]
        subgraph backend[🖥️ Back End]
            readapi[📖 Read API]
            writeapi[✏️ Write API]
        end
    end

    client <-->|📄🟣| frontend
    frontend <-->|GET 📄🟣| readapi
    frontend -->|POST 📄🟣| writeapi


    subgraph sqldb[ ✅ RDBMS]
        dbloadbalancer[ ⚖️ DB Load Balancer]
        sqlmaster[(🗄️ SQL Database Master 📄📄📄)]
        sqlslave1[(🗄️ SQL Database Slave 📄📄📄)]
        sqlslave2[(🗄️ SQL Database Slave 📄📄📄)]
        sqlslave3[(🗄️ SQL Database Slave 📄📄📄)]
    end

    writeapi -->|WRITE 📄| sqlmaster

    readapi <-->|READ 📄| dbloadbalancer

    dbloadbalancer <-->|READ 📄| sqlslave1
    dbloadbalancer <-->|READ 📄| sqlslave2
    dbloadbalancer <-->|READ 📄| sqlslave3

    sqlmaster -->|WRITE 📄| sqlslave1
    sqlmaster -->|WRITE 📄| sqlslave2
    sqlmaster -->|WRITE 📄| sqlslave3

    objectstore[🧺 Object Store 🟣🟣🟣]
    writeapi -->|WRITE 🟣| objectstore
    readapi <-->|READ 🟣| objectstore
```

### ✅ Use CDN for static files

```mermaid
graph TD
    subgraph web[🌐 Web Server]
        frontend[🖼️ Front End]
        subgraph backend[🖥️ Back End]
            readapi[📖 Read API]
            writeapi[✏️ Write API]
        end
    end


    subgraph regions [🌐 CDN]
        subgraph regionus[USA Region 🇺🇸]
            clientus[🧑‍💻 Client 🇺🇸]
            cdnus[🇺🇸 CDN USA]
        end
        subgraph regioneu[CDN EU 🇪🇺]
            clienteu[🧑‍💻 Client 🇪🇺]
            cdneu[🇪🇺 CDN EU]
        end
        subgraph regionil[CDN IL 🇮🇱]
            clientil[🧑‍💻 Client 🇮🇱]
            cdnil[🇮🇱 CDN IL]
        end
        subgraph regionjp[CDN JP 🇯🇵]
            clientjp[🧑‍💻 Client 🇯🇵]
            cdnjp[🇯🇵 CDN JP]
        end
    end


    clientus <-->|📄🟣| frontend
    clienteu <-->|📄🟣| frontend
    clientil <-->|📄🟣| frontend
    clientjp <-->|📄🟣| frontend

    clientus <-->|GET 📄🟣| cdnus
    clienteu <-->|GET 📄🟣| cdneu
    clientil <-->|GET 📄🟣| cdnil
    clientjp <-->|GET 📄🟣| cdnjp

    frontend <-->|GET 📄🟣| readapi
    frontend -->|POST 📄🟣| writeapi


    subgraph sqldb[ ✅ RDBMS]
        dbloadbalancer[ ⚖️ DB Load Balancer]
        sqlmaster[(🗄️ SQL Database Master 📄📄📄)]
        sqlslave1[(🗄️ SQL Database Slave 📄📄📄)]
        sqlslave2[(🗄️ SQL Database Slave 📄📄📄)]
        sqlslave3[(🗄️ SQL Database Slave 📄📄📄)]
    end

    writeapi -->|WRITE 📄| sqlmaster

    readapi <-->|READ 📄| dbloadbalancer

    dbloadbalancer <-->|READ 📄| sqlslave1
    dbloadbalancer <-->|READ 📄| sqlslave2
    dbloadbalancer <-->|READ 📄| sqlslave3

    sqlmaster -->|WRITE 📄| sqlslave1
    sqlmaster -->|WRITE 📄| sqlslave2
    sqlmaster -->|WRITE 📄| sqlslave3
    sqlmaster -->|WRITE 📄| cdnus
    sqlmaster -->|WRITE 📄| cdneu
    sqlmaster -->|WRITE 📄| cdnil
    sqlmaster -->|WRITE 📄| cdnjp

    objectstore[🧺 Object Store 🟣🟣🟣]
    writeapi -->|WRITE 🟣| objectstore
    readapi <-->|READ 🟣| objectstore
```

## Usage Stats and Analytics

### ✅ Add Analytics DB

```mermaid
graph TD

    subgraph analyticsmicroservice[📊 Analytics Microservice]
        analyticsclient[🧑‍💻 Analytics Client]
        analyticsapiendpoint[📈 Analytics API Endpoint]
        analyticsapiserver[🖥️ Back End 📊]
        analyticsdb[🗄️ Analytics DB]
    end

    subgraph web[🌐 Web Server]
        frontend[🖼️ Front End]

        subgraph backend[🖥️ Back End]
            readapi[📖 Read API]
            writeapi[✏️ Write API]
        end

        subgraph cdnworkerpool[🛠️ CDN Worker Pool]
            direction TB
            cdnloadbalancer[⚖️ CDN Load Balancer]
            cdnworker1[🛠️ CDN Worker 1]
            cdnworker2[🛠️ CDN Worker 2]
            cdnworker3[🛠️ CDN Worker 3]
            cdnloadbalancer --> cdnworker1 --> cdnworker2 --> cdnworker3
        end

        objectstore[🧺 Object Store 🟣🟣🟣]
    end

    subgraph sqldb[ ✅ RDBMS]
    sqlreverseproxy[🔄 SQL Reverse Proxy]
        sqlmaster[(🗄️ SQL Database Master 📄📄📄)]
        subgraph sqlslaves[SQL Database Slaves 📄📄📄]
            dbloadbalancer[ ⚖️ DB Replicas Load Balancer]
            sqlslave1[(🗄️ SQL Database Slave)]
            sqlslave2[(🗄️ SQL Database Slave)]
            sqlslave3[(🗄️ SQL Database Slave)]
        end
    end


    subgraph regions [🌐 CDN]
        cdnreverseproxy[🔄 CDN Reverse Proxy]
        subgraph regionus[USA Region 🇺🇸]
            clientus[🧑‍💻 Client 🇺🇸]
            cdnus[🇺🇸 CDN USA]
        end
        subgraph regioneu[EU Region 🇪🇺]
            clienteu[🧑‍💻 Client 🇪🇺]
            cdneu[🇪🇺 CDN EU]
        end
        subgraph regionil[Israel Region 🇮🇱]
            clientil[🧑‍💻 Client 🇮🇱]
            cdnil[🇮🇱 CDN IL]
        end
        subgraph regionjp[Japan Region 🇯🇵]
            clientjp[🧑‍💻 Client 🇯🇵]
            cdnjp[🇯🇵 CDN JP]
        end
    end


    frontend <-->|GET 📄🟣| readapi
    frontend -->|POST 📄🟣| writeapi

    writeapi -->|WRITE 📄| sqlreverseproxy --> sqlmaster
    readapi <-->|READ 📄| sqlreverseproxy

    dbloadbalancer <-->|RW 📄| sqlslave1
    dbloadbalancer <-->|RW 📄| sqlslave2
    dbloadbalancer <-->|RW 📄| sqlslave3

    sqlmaster -->|WRITE 📄| dbloadbalancer

    readapi -->|WRITE 🟣📄| cdnworkerpool
    cdnworkerpool -->|WRITE 🟣📄| cdnreverseproxy
    sqlmaster -->|WRITE 📄| sqlreverseproxy --> |WRITE 📄| analyticsapiendpoint --> analyticsapiserver --> |RW 📄| analyticsdb
    analyticsclient <-->|GET 📊| analyticsapiendpoint <--> analyticsapiserver

    objectstore[🧺 Object Store 🟣🟣🟣]
    writeapi -->|WRITE 🟣| objectstore
    readapi <-->|READ 🟣| objectstore


    clientus <-->|GET 📄🟣| cdnus
    clienteu <-->|GET 📄🟣| cdneu
    clientil <-->|GET 📄🟣| cdnil
    clientjp <-->|GET 📄🟣| cdnjp

    cdnreverseproxy -->|WRITE 📄🟣| cdnus
    cdnreverseproxy -->|WRITE 📄🟣| cdneu
    cdnreverseproxy -->|WRITE 📄🟣| cdnil
    cdnreverseproxy -->|WRITE 📄🟣| cdnjp
```

## Delays in DNS Resolution

### ✅ Add Geo-aware DNS Provider
```mermaid
graph TD
    subgraph regions [🌐 Regions]

        %% Clients
        clientus[🧑‍💻 Client 🇺🇸]
        clienteu[🧑‍💻 Client 🇪🇺]
        clientil[🧑‍💻 Client 🇮🇱]
        clientjp[🧑‍💻 Client 🇯🇵]

        %% Geo-aware DNS
        geodns[🌐 Geo-aware DNS]

        %% Global Load Balancer
        globallb[🧭 Global Load Balancer]

        %% DNS Routing
        clientus --> geodns
        clienteu --> geodns
        clientil --> geodns
        clientjp --> geodns

        geodns -->|🇺🇸| globallb
        geodns -->|🇪🇺| globallb
        geodns -->|🇮🇱| globallb
        geodns -->|🇯🇵| globallb

        %% CDN Routing
        clientus <-->|GET 📄🟣| cdnus
        clienteu <-->|GET 📄🟣| cdneu
        clientil <-->|GET 📄🟣| cdnil
        clientjp <-->|GET 📄🟣| cdnjp

        %% Regional Subgraphs
        subgraph regionus[🇺🇸 Region - USA]
            cdnus[🍱 CDN 🇺🇸]
            dnsuspop[🛰️ DNS PoP 🇺🇸]
            subgraph uswebserver[🖥️ Web Server 🇺🇸]
                usreadapi[📖 Read API 🇺🇸]
                uswriteapi[✏️ Write API 🇺🇸]
            end
        end

        subgraph regioneu[🇪🇺 Region - Europe]
            cdneu[🍱 CDN 🇪🇺]
            dnseupop[🛰️ DNS PoP 🇪🇺]
            subgraph euwebserver[🖥️ Web Server 🇪🇺]
                eureadapi[📖 Read API 🇪🇺]
                euwriteapi[✏️ Write API 🇪🇺]
            end            
        end

        subgraph regionil[🇮🇱 Region - Israel]
            cdnil[🍱 CDN 🇮🇱]
            dnsilpop[🛰️ DNS PoP 🇮🇱]
            subgraph ilwebserver[🖥️ Web Server 🇮🇱]
                ilreadapi[📖 Read API 🇮🇱]
                ilwriteapi[✏️ Write API 🇮🇱]
            end
        end

        subgraph regionjp[🇯🇵 Region - Japan]
            cdnjp[🍱 CDN 🇯🇵]
            dnsjppop[🛰️ DNS PoP 🇯🇵]
            subgraph jpwebserver[🖥️ Web Server 🇯🇵]
                jpreadapi[📖 Read API 🇯🇵]
                jpwriteapi[✏️ Write API 🇯🇵]
            end
        end
    end

    subgraph analyticsmicroservice[📊 Analytics Microservice]
        analyticsclient[🧑‍💻 Analytics Client]
        analyticsapiendpoint[📈 Analytics API Endpoint]
        analyticsapiserver[🖥️ Back End 📊]
        analyticsdb[🗄️ Analytics DB]
    end

    subgraph web[🌐 Web Server]
        frontend[🖼️ Front End]

        subgraph backend[🖥️ Back End]
            readapi[📖 Read API]
            writeapi[✏️ Write API]
        end
    end

    subgraph sqldb[✅ Storage]
        storagereverseproxy[🔄 Storage Reverse Proxy]
        objectstore[🧺 Object Store 🟣🟣🟣]
        sqlmaster[(🗄️ SQL Database Master 📄📄📄)]
        subgraph sqlslaves[SQL Database Slaves 📄📄📄]
            dbloadbalancer[⚖️ DB Replicas Load Balancer]
            sqlslave1[(🗄️ SQL Database Slave)]
            sqlslave2[(🗄️ SQL Database Slave)]
            sqlslave3[(🗄️ SQL Database Slave)]
        end
    end

    subgraph cdn [🌐 CDN]
        cdnreverseproxy[🔄 CDN Reverse Proxy]
        cdnserver[🔄 CDN Server]
        subgraph cdnworkerpool[🛠️ CDN Worker Pool]
            cdnworker1[🛠️ CDN Worker 1]
            cdnworker2[🛠️ CDN Worker 2]
            cdnworker3[🛠️ CDN Worker 3]
        end
        cdnserver --> cdnworker1 --> cdnworker2 --> cdnworker3
    end

    %% Web Server ↔ Backend
    frontend <-->|GET 📄🟣| readapi
    frontend -->|POST 📄🟣| writeapi

    %% API → Storage
    writeapi -->|WRITE 📄| storagereverseproxy --> sqlmaster
    readapi <-->|READ 📄| storagereverseproxy

    %% SQL Replication
    dbloadbalancer <-->|RW 📄| sqlslave1
    dbloadbalancer <-->|RW 📄| sqlslave2
    dbloadbalancer <-->|RW 📄| sqlslave3
    sqlmaster -->|WRITE 📄| dbloadbalancer

    %% CDN Data Ingest
    cdnworkerpool -->|WRITE 🟣📄| cdnserver
    cdnserver -->|WRITE 📄🟣| cdnloadbalancer
    cdnserver -->|WRITE 📄🟣| cdnloadbalancer
    cdnserver -->|WRITE 📄🟣| cdnloadbalancer
    cdnserver -->|WRITE 📄🟣| cdnloadbalancer

    %% Analytics pipeline
    sqlmaster -->|WRITE 📄| storagereverseproxy --> |WRITE 📄| analyticsapiendpoint --> analyticsapiserver --> |RW 📄| analyticsdb
    analyticsclient <-->|GET 📊| analyticsapiendpoint <--> analyticsapiserver

    %% Object Store access
    writeapi -->|WRITE 🟣| storagereverseproxy --> objectstore
    readapi <-->|READ 🟣| objectstore
```
