
```mermaid
graph TD
	%% Subgraph: Global Nodes
	subgraph global [🌐 Global Infrastructure]
        subgraph region_client[🧑‍💻 Clients 🇺🇸 🇪🇺 🇮🇱 🇯🇵]
            us_client[🧑‍💻 Client 🇺🇸]
            eu_client[🧑‍💻 Client 🇪🇺]
            il_client[🧑‍💻 Client 🇮🇱]
            jp_client[🧑‍💻 Client 🇯🇵]
        end
        geodns[🌐 Geo-aware DNS]
        globallb[Global Load Balancer]
	end

    %% Regional Application Stack
    subgraph region_region[Regions - USA, EU, etc]
        subgraph region_origin[💻 Origin 🇺🇸 🇪🇺 🇮🇱 🇯🇵]
            waf[🛡️ WAF / Rate Limiter]
            abuseguard[🚫 Abuse Protection]
            region_cache[🧊 App Cache Layer]
            region_frontend[🖼️ Front End]
            region_read_api[📖 Read API]
            region_write_api[✏️ Write API]
            pastedelete[🗑️ Delete Paste Token Validated]
        end
    end

	%% Analytics Microservice
	subgraph analyticsmicroservice[📊 Analytics Microservice]
		analyticsclient[🧑‍💻 Analytics Client]
		analyticsapiendpoint[📈 Analytics API Endpoint]
		analyticsapiserver[💻 Back End 📊]
		analyticsdb[📒 Analytics DB]

        subgraph etl[🛠️ ETL Pipeline]
            etlextract[📤 Extract: SQL + Object Store]
            etltransform[🔄 Transform: Normalize & Join]
            etlload[📥 Load to Analytics API]
            etljob[⏱️ Daily ETL Job Trigger]
        end

	end

    sqlmaster --> etlextract
    objectstore --> etlextract
    etljob --> etlextract --> etltransform --> etlload --> analyticsapiendpoint

	%% SQL + Object Storage
	subgraph sqldb[✅ Storage]
		storagereverseproxy[🔄 Storage Reverse Proxy]
		objectstore[🧺 Object Store 🟣🟣🟣]
		sqlmaster[(📒 SQL DB Master)]
        sqlslaves[(📒📒📒 SQL DB Slaves)]
		dbloadbalancer[⚖️ Replica Load Balancer]
	end

	%% CDN Layer
	subgraph cdn [🌐 CDN]
		cdnentrypoint[🌐 CDN Entry Point]
		cdnloadbalancer[⚖️ CDN Ingest Load Balancer]
		cdnserver[🔄 CDN Ingest Server]
		cdnworkerpool[🛠️🛠️🛠️ CDN Worker Pool]
        cdnconfig[⚙️ CDN TTL & Cache Rules]
	end

	%% Monitoring
	subgraph observability[🧭 Observability]
        logcollector[📜 Log Collector]
        monitorbackend[📊 Metrics / Dashboards]
	end

	%% Traffic Flow
	region_client -->|GET/POST 📄🟣| geodns
	geodns --> globallb
    globallb -->|Static/Dynamic 📄| cdnentrypoint
    
    cdnentrypoint --> cdnconfig --> cdnloadbalancer --> cdnserver --> cdnworkerpool

    cdnentrypoint -->|Deliver content| region_client

	%% CDN fetches from origin on cache miss
	cdnserver --> region_frontend

	%% Origin App Logic
	region_frontend -->|GET 📄| region_read_api
	region_frontend -->|POST 📄| region_write_api
	region_read_api --> region_cache
	region_cache --> region_read_api

	waf --> region_frontend
	region_write_api --> abuseguard
	abuseguard --> storagereverseproxy

	region_write_api --> pastedelete
	pastedelete --> storagereverseproxy

	region_read_api --> storagereverseproxy
	storagereverseproxy -->|READ/WRITE 🟣| objectstore
	storagereverseproxy -->|WRITE 📄| sqlmaster

	%% DB Replication
	sqlmaster -->|🔁 Replication| sqlslaves

	%% Storage Failover
	storagereverseproxy -->|READ 📄| dbloadbalancer --> sqlslaves

	%% Analytics Flow
	analyticsapiendpoint --> analyticsapiserver
	analyticsapiserver -->|RW 📄| analyticsdb
	analyticsclient <-->|GET 📊| analyticsapiendpoint

	%% Logging
	region_frontend --> logcollector
	logcollector --> monitorbackend
```
