# StateX Microservices Architecture Diagram

## 🏗️ **Current Architecture Overview**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           StateX Microservices Ecosystem                        │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                           🏢 STATEX PLATFORM (Orchestrator)                     │
│                                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐             │
│  │   User Portal   │    │  Submission     │    │  AI Orchestrator│             │
│  │   (Port 8006)   │    │  Service        │    │   (Port 8003)   │             │
│  │                 │    │  (Port 8002)    │    │                 │             │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘             │
│           │                       │                       │                    │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐             │
│  │  AI Workers     │    │  Content        │    │  Logging        │             │
│  │  (Port 8004)    │    │  Service        │    │  Service        │             │
│  │                 │    │  (Port 8009)    │    │  (Port 8007)    │             │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘             │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                    Infrastructure Services                              │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐         │   │
│  │  │PostgreSQL│ │  Redis  │ │RabbitMQ │ │  MinIO  │ │Elasticsearch│     │   │
│  │  │  :5432   │ │  :6379  │ │ :5672   │ │ :9000   │ │   :9200    │     │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘         │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                    Frontend & Gateway                                  │   │
│  │  ┌─────────────────┐              ┌─────────────────┐                  │   │
│  │  │ Website Frontend│              │   API Gateway   │                  │   │
│  │  │   (Port 3000)   │              │   (Port 80/443) │                  │   │
│  │  └─────────────────┘              └─────────────────┘                  │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                        🔧 STANDALONE SERVICES (Independent)                     │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │              StateX Notification Service                                │   │
│  │                    (Port 8005)                                          │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐                      │   │
│  │  │  Email  │ │WhatsApp │ │Telegram │ │LinkedIn │                      │   │
│  │  │   📧    │ │   📱    │ │   ✈️    │ │   💼    │                      │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘                      │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │                    StateX Mailhog                                      │   │
│  │              (Ports 1025, 8025)                                        │   │
│  │                    Email Testing                                       │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                        🤖 AI SERVICES (Separate Repository)                     │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │              StateX AI Platform                                        │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐         │   │
│  │  │   NLP   │ │   ASR   │ │Document │ │Prototype│ │Template │         │   │
│  │  │Service  │ │Service  │ │   AI    │ │Generator│ │Repository│        │   │
│  │  │ :8011   │ │ :8012   │ │ :8013   │ │ :8014   │ │ :8015   │        │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘         │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## 🔄 **Communication Flow**

```
User Request
     │
     ▼
┌─────────────┐
│   Website   │
│  Frontend   │
└─────────────┘
     │
     ▼
┌─────────────┐
│ API Gateway │
└─────────────┘
     │
     ▼
┌─────────────┐    ┌─────────────────┐
│ Submission  │───▶│   Notification  │
│  Service    │    │    Service      │
└─────────────┘    │   (Standalone)  │
     │             └─────────────────┘
     ▼
┌─────────────┐
│    AI       │
│ Orchestrator│
└─────────────┘
     │
     ▼
┌─────────────┐    ┌─────────────────┐
│   AI        │───▶│   Notification  │
│  Workers    │    │    Service      │
└─────────────┘    │   (Standalone)  │
                   └─────────────────┘
```

## 📁 **Repository Structure**

```
statex/
├── statex-platform/              # 🏢 Main orchestration platform
│   ├── docker-compose.yml        # All services together
│   ├── services/                 # Platform microservices
│   │   ├── user-portal/
│   │   ├── submission-service/
│   │   ├── ai-orchestrator/
│   │   ├── ai-workers/
│   │   ├── content-service/
│   │   └── logging-service/
│   └── docs/
│
├── statex-notification-service/  # 🔧 Standalone notification service
│   ├── docker-compose.yml        # Independent deployment
│   ├── app/main.py               # Service implementation
│   ├── test_workflow_simple.py   # Workflow testing
│   └── .env                      # Service configuration
│
├── statex-ai/                    # 🤖 Standalone AI services
│   ├── docker-compose.yml        # Independent deployment
│   └── services/
│       ├── nlp-service/
│       ├── asr-service/
│       ├── document-ai/
│       ├── prototype-generator/
│       └── template-repository/
│
└── statex-website/               # 🌐 Standalone website
    ├── frontend/                 # Next.js frontend
    └── backend/                  # FastAPI backend
```

## 🚀 **Development Workflow**

### **1. Individual Service Development**
```bash
# Work on notification service independently
cd statex-notification-service
docker compose up --build
python3 test_workflow_simple.py --demo

# Work on AI services independently  
cd statex-ai
docker compose up --build

# Work on website independently
cd statex-website/frontend
npm run dev
```

### **2. Platform Integration**
```bash
# Run all services together for integration testing
cd statex-platform
docker compose up --build
```

### **3. Complete Workflow Test**
```bash
# Test the complete user journey
cd statex-notification-service
python3 test_workflow_simple.py --demo
```

## 🎯 **Key Benefits**

### **✅ Independence**
- Services can be developed and updated separately
- No conflicts between development teams
- Faster iteration cycles

### **✅ Orchestration**
- Platform manages all services together
- Centralized configuration and monitoring
- Easy deployment and scaling

### **✅ Flexibility**
- Mix of standalone and platform services
- Technology diversity per service
- Gradual migration capabilities

### **✅ Scalability**
- Scale services independently
- Resource optimization per service
- Load balancing and failover

## 📊 **Current Status**

| Service | Status | Port | Type | Repository |
|---------|--------|------|------|------------|
| Notification Service | ✅ Working | 8005 | Standalone | Independent |
| Mailhog | ✅ Working | 1025/8025 | Standalone | Independent |
| User Portal | ✅ Working | 8006 | Platform | Orchestrated |
| Submission Service | ✅ Working | 8002 | Platform | Orchestrated |
| AI Orchestrator | 🔄 Placeholder | 8003 | Platform | Orchestrated |
| AI Workers | 🔄 Placeholder | 8004 | Platform | Orchestrated |
| Content Service | ✅ Working | 8009 | Platform | Orchestrated |
| Logging Service | ✅ Working | 8007 | Platform | Orchestrated |
| Website Frontend | ✅ Working | 3000 | Platform | Orchestrated |
| API Gateway | ✅ Working | 80/443 | Platform | Orchestrated |

## 🔮 **Next Steps**

1. **Complete AI Services Setup**
   - Deploy statex-ai services
   - Integrate with platform
   - Test complete workflow

2. **Enhanced Monitoring**
   - Prometheus metrics
   - Grafana dashboards
   - Distributed tracing

3. **Production Deployment**
   - Environment-specific configs
   - Security hardening
   - Performance optimization

---

This architecture provides the perfect balance between **independence** and **orchestration**, enabling rapid development while maintaining system coherence and reliability.

