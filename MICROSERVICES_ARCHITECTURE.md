# StateX Microservices Architecture & Separation Strategy

## Overview

StateX follows a **hybrid microservices architecture** where:
- **Individual microservices** run independently and can be updated separately
- **StateX Platform** orchestrates all services together for development and production
- **Clear separation of concerns** with well-defined interfaces

## Current Architecture

### 🏗️ **Standalone Services** (Independent)
These services run independently and are updated separately:

#### 1. **StateX Notification Service** (`statex-notification-service`)
- **Port**: 8005
- **Purpose**: Centralized notification delivery
- **Channels**: Email, WhatsApp, Telegram, LinkedIn (manual)
- **Status**: ✅ **Fully Functional**
- **Repository**: Independent
- **Updates**: Separate from platform

#### 2. **StateX Mailhog** (`statex-mailhog`)
- **Ports**: 1025 (SMTP), 8025 (Web UI)
- **Purpose**: Email testing and development
- **Status**: ✅ **Running**
- **Repository**: Independent

### 🏢 **Platform Services** (Orchestrated by statex-platform)
These services are managed and orchestrated by the main platform:

#### Infrastructure Services
- **PostgreSQL** (5432) - Primary database
- **Redis** (6379) - Caching and sessions
- **RabbitMQ** (5672, 15672) - Message broker
- **MinIO** (9000, 9001) - Object storage
- **Elasticsearch** (9200) - Search and analytics

#### Core Microservices
- **User Portal** (8006) - User management and authentication
- **Submission Service** (8002) - Form submission and file handling
- **AI Orchestrator** (8003) - AI workflow management (placeholder)
- **AI Workers** (8004) - AI processing (placeholder)
- **Content Service** (8009) - Content management
- **Logging Service** (8007) - Centralized logging

#### Frontend & Gateway
- **Website Frontend** (3000) - Next.js application
- **API Gateway** (80, 443) - Nginx reverse proxy

#### Monitoring
- **Prometheus** (9090) - Metrics collection
- **Grafana** (3000) - Monitoring dashboards

## 🎯 **Separation Strategy**

### **Development Environment**

#### **Individual Service Development**
```bash
# Work on notification service independently
cd statex-notification-service
docker compose up --build

# Work on AI services independently  
cd statex-ai
docker compose up --build

# Work on website independently
cd statex-website
npm run dev
```

#### **Platform Integration**
```bash
# Run all services together for integration testing
cd statex-platform
docker compose up --build
```

### **Service Communication**

#### **1. HTTP API Calls** (Synchronous)
- Services communicate via REST APIs
- Well-defined endpoints and contracts
- JSON payloads with proper error handling

#### **2. Message Broker** (Asynchronous)
- RabbitMQ for event-driven communication
- Loose coupling between services
- Event types: `user.*`, `request.*`, `ai.*`, `notification.*`

#### **3. Shared Infrastructure**
- PostgreSQL for persistent data
- Redis for caching and sessions
- MinIO for file storage
- Elasticsearch for search and analytics

## 🔄 **Workflow Example**

### **Complete User Journey**
1. **User submits contact form** → Website Frontend
2. **Form data processed** → Submission Service
3. **Initial notification sent** → Notification Service (standalone)
4. **AI analysis triggered** → AI Orchestrator (platform)
5. **AI processing** → AI Workers (platform)
6. **Results notification sent** → Notification Service (standalone)

### **Service Dependencies**
```
Website Frontend
    ↓
API Gateway
    ↓
Submission Service → Notification Service (standalone)
    ↓
AI Orchestrator → AI Workers
    ↓
Notification Service (standalone)
```

## 📁 **Repository Structure**

```
statex/
├── statex-platform/              # Main orchestration platform
│   ├── docker-compose.yml        # All services together
│   ├── services/                 # Platform microservices
│   └── docs/                     # Platform documentation
├── statex-notification-service/  # Standalone notification service
│   ├── docker-compose.yml        # Independent deployment
│   ├── app/                      # Service implementation
│   └── test_workflow_simple.py   # Workflow testing
├── statex-ai/                    # Standalone AI services
│   ├── docker-compose.yml        # Independent deployment
│   └── services/                 # AI microservices
└── statex-website/               # Standalone website
    ├── frontend/                 # Next.js frontend
    └── backend/                  # FastAPI backend
```

## 🚀 **Development Workflow**

### **1. Individual Service Development**
```bash
# Work on notification service
cd statex-notification-service
python3 test_workflow_simple.py --demo

# Work on AI services
cd statex-ai
docker compose up --build

# Work on website
cd statex-website/frontend
npm run dev
```

### **2. Integration Testing**
```bash
# Start platform with all services
cd statex-platform
docker compose up --build

# Test complete workflow
cd statex-notification-service
python3 test_workflow_simple.py --demo
```

### **3. Production Deployment**
```bash
# Deploy individual services
cd statex-notification-service
docker compose -f docker-compose.prod.yml up -d

# Deploy platform
cd statex-platform
docker compose -f docker-compose.prod.yml up -d
```

## 🔧 **Configuration Management**

### **Environment Variables**
- **Standalone services**: Own `.env` files
- **Platform services**: Centralized configuration
- **Secrets**: Managed separately (Vault, etc.)

### **Service Discovery**
- **Development**: Direct port mapping
- **Production**: Service mesh or load balancer
- **Health checks**: Built into each service

## 📊 **Monitoring & Observability**

### **Centralized Monitoring**
- **Prometheus**: Metrics collection
- **Grafana**: Dashboards and visualization
- **Elasticsearch**: Log aggregation
- **Health checks**: Service status monitoring

### **Distributed Tracing**
- **Request tracing**: Across service boundaries
- **Performance monitoring**: Response times and throughput
- **Error tracking**: Centralized error reporting

## 🎯 **Benefits of This Architecture**

### **1. Independent Development**
- Teams can work on services separately
- Faster development cycles
- Reduced conflicts and dependencies

### **2. Scalability**
- Scale services independently
- Resource optimization
- Load balancing per service

### **3. Maintainability**
- Clear separation of concerns
- Easier debugging and testing
- Technology diversity per service

### **4. Deployment Flexibility**
- Deploy services independently
- Rollback individual services
- A/B testing per service

## 🔮 **Future Enhancements**

### **1. Service Mesh**
- Istio or Linkerd for advanced traffic management
- Automatic service discovery
- Advanced security policies

### **2. API Gateway Enhancement**
- Rate limiting per service
- Authentication and authorization
- Request/response transformation

### **3. Event Sourcing**
- Complete audit trail
- Event replay capabilities
- Better debugging and monitoring

## 📝 **Best Practices**

### **1. Service Design**
- Single responsibility principle
- Well-defined APIs
- Proper error handling
- Comprehensive logging

### **2. Communication**
- Use HTTP for synchronous calls
- Use message broker for async events
- Implement circuit breakers
- Handle failures gracefully

### **3. Data Management**
- Database per service
- Shared data through APIs
- Eventual consistency
- Proper data migration strategies

### **4. Testing**
- Unit tests per service
- Integration tests across services
- End-to-end workflow testing
- Performance testing

## 🎉 **Current Status**

✅ **Working Components:**
- Notification Service (standalone)
- Platform orchestration
- Basic workflow testing
- Multi-channel notifications

🔄 **In Development:**
- AI services integration
- Advanced workflow orchestration
- Enhanced monitoring

📋 **Next Steps:**
- Complete AI services setup
- Advanced testing scenarios
- Production deployment preparation
- Performance optimization

---

This architecture provides the perfect balance between **independence** and **orchestration**, allowing for rapid development while maintaining system coherence and reliability.

