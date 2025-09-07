# StateX Free AI Services Guide

## 🆓 **Complete Guide to Using FREE AI Services**

This guide shows you how to use **100% FREE** AI services for testing your StateX workflow without any API keys or costs.

## 🎯 **Available Free Options**

### **Option 1: Ollama (Local LLM) - RECOMMENDED** ⭐
- **Cost**: 100% FREE
- **API Keys**: None required
- **Quality**: High (uses Llama 2, Mistral, CodeLlama)
- **Speed**: Fast (runs locally)
- **Privacy**: Complete (no data leaves your machine)

### **Option 2: Hugging Face Inference API**
- **Cost**: FREE (50 requests/hour)
- **API Keys**: None required for some models
- **Quality**: Good
- **Speed**: Medium (cloud-based)
- **Privacy**: Data sent to Hugging Face

### **Option 3: Mock AI Service**
- **Cost**: 100% FREE
- **API Keys**: None required
- **Quality**: Realistic simulation
- **Speed**: Instant
- **Privacy**: Complete (local only)

## 🚀 **Quick Start**

### **Step 1: Setup Free AI Services**
```bash
# Run the setup script
./setup_free_ai.sh
```

This will:
- Install Ollama (if not already installed)
- Download free AI models (Llama 2, Mistral, CodeLlama)
- Start the Ollama service
- Verify everything is working

### **Step 2: Test the Workflow**
```bash
# Test with free AI services
python3 test_workflow_free_ai.py --demo
```

## 🔧 **Detailed Setup Instructions**

### **Option 1: Ollama Setup (Recommended)**

#### **Install Ollama:**
```bash
# macOS
curl -fsSL https://ollama.ai/install.sh | sh

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download
```

#### **Start Ollama:**
```bash
# Start the service
ollama serve

# In another terminal, download models
ollama pull llama2:7b
ollama pull mistral:7b
ollama pull codellama:7b
```

#### **Test Ollama:**
```bash
# Test a simple query
ollama run llama2:7b "Hello, how are you?"

# List available models
ollama list
```

### **Option 2: Hugging Face Setup**

#### **No API Key Required:**
Some models on Hugging Face don't require API keys:
- `microsoft/DialoGPT-medium`
- `gpt2`
- `distilbert-base-uncased`

#### **Test Hugging Face:**
```bash
# Test the API
curl -X POST "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium" \
  -H "Content-Type: application/json" \
  -d '{"inputs": "Hello, how are you?"}'
```

### **Option 3: Mock AI Service**

#### **No Setup Required:**
The mock service is built into the workflow script and works immediately.

## 📊 **What Each Service Provides**

### **Ollama (Local LLM)**
- **Models**: Llama 2 7B, Mistral 7B, CodeLlama 7B
- **Use Cases**: Text generation, analysis, coding
- **Quality**: High (same models used by paid services)
- **Speed**: Fast (runs on your machine)
- **Privacy**: Complete (no data leaves your machine)

### **Hugging Face API**
- **Models**: Various open-source models
- **Use Cases**: Text generation, classification, analysis
- **Quality**: Good (depends on model)
- **Speed**: Medium (cloud-based)
- **Privacy**: Data sent to Hugging Face

### **Mock AI Service**
- **Models**: Simulated responses
- **Use Cases**: Testing, development, demos
- **Quality**: Realistic simulation
- **Speed**: Instant
- **Privacy**: Complete (local only)

## 🎮 **How to Use**

### **Interactive Mode:**
```bash
python3 test_workflow_free_ai.py
```
- Enter your own data
- Choose custom project description
- Get personalized analysis

### **Demo Mode:**
```bash
python3 test_workflow_free_ai.py --demo
```
- Uses sample data
- Quick testing
- No input required

### **Default Mode:**
```bash
python3 test_workflow_free_ai.py --default
```
- Uses default test data
- Good for repeated testing

## 📱 **What You'll Receive**

### **Initial Notification:**
```
Hello Sergej!

Thank you for your submission! We've received your project details:
• Text description: 245 characters
• Voice transcript: 156 characters  
• File content: 234 characters

Our FREE AI agents are now analyzing your requirements. We'll contact you via Telegram with the analysis results shortly.

Best regards,
The Statex Team
```

### **AI Analysis Results:**
```
🤖 AI Analysis Complete for Sergej

📋 Project Summary:
User Sergej wants to create a digital solution for their auto business, focusing on automation and customer experience.

🔍 Business Type:
Auto

⚠️ Current Pain Points:
• Manual processes and workflows
• Customer communication challenges
• Data management and tracking
• Integration between systems

💡 Business Opportunities:
• Digital Platform Development - High potential (3-6 months)
• Mobile Application - High potential (2-4 months)
• Process Automation - Medium potential (1-3 months)

🔧 Technical Recommendations:
• Frontend: React/Next.js, TypeScript, Responsive design
• Backend: Node.js/Python, PostgreSQL, RESTful API
• Integrations: Payment processing, SMS/Email, Calendar sync, Analytics

📝 Next Steps:
• Conduct auto market research (1-2 weeks)
• Develop MVP prototype (4-8 weeks)
• Create technical architecture (2-3 weeks)

💰 Budget Estimate:
• Development: $15,000 - $35,000
• Infrastructure: $200 - $500/month
• Maintenance: $1,000 - $2,000/month

🎯 Confidence: 85%
🤖 AI Service: OLLAMA
```

## 🔍 **Service Detection**

The workflow automatically detects which services are available:

1. **Checks Ollama** (port 11434) - If available, uses it
2. **Checks Hugging Face** - If Ollama not available, tries Hugging Face
3. **Falls back to Mock** - If neither available, uses mock service

## 🛠️ **Troubleshooting**

### **Ollama Issues:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
pkill ollama
ollama serve

# Check models
ollama list
```

### **Hugging Face Issues:**
```bash
# Test API
curl -X POST "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium" \
  -H "Content-Type: application/json" \
  -d '{"inputs": "test"}'
```

### **Notification Issues:**
```bash
# Check notification service
curl http://localhost:8005/health

# Check logs
docker logs statex-notification-service-notification-service-1
```

## 🎯 **Best Practices**

### **For Development:**
- Use **Mock AI Service** for quick testing
- Use **Ollama** for realistic AI responses
- Use **Hugging Face** for cloud-based testing

### **For Production:**
- Use **Ollama** for privacy and control
- Use **Hugging Face** for scalability
- Use **Mock** for testing and demos

### **For Testing:**
- Test with all three services
- Compare response quality
- Measure performance differences

## 🚀 **Advanced Usage**

### **Custom Models:**
```bash
# Download custom models
ollama pull llama2:13b  # Larger model
ollama pull mistral:7b-instruct  # Instruction-tuned
ollama pull codellama:13b  # Code-focused
```

### **Custom Prompts:**
Edit the `analyze_with_ollama` function to customize the AI prompts for your specific use case.

### **Custom Models:**
Edit the `analyze_with_huggingface` function to use different Hugging Face models.

## 🎉 **You're Ready!**

With these free AI services, you can:

✅ **Test your workflow** without any costs
✅ **Get real AI analysis** using local models
✅ **Maintain privacy** (data stays on your machine)
✅ **Scale as needed** (add more models or services)
✅ **Develop and iterate** quickly

**Start with the setup script and you'll be running AI-powered workflows in minutes!** 🚀
