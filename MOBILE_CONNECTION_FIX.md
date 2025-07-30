# 🔧 STOKY Mobile App - Connection Issue Fix

## 🚨 **Issue Identified**

Your STOKY mobile app is working perfectly, but it can't connect to the backend server because:
- **App Status**: ✅ Running successfully on your phone
- **Backend Status**: ❌ Not running on port 8001
- **Error**: "Connection refused" when trying to reach `http://10.105.22.220:8001`

## 🛠️ **Quick Fix - Start Backend Server**

### **Method 1: Using Command Prompt**
1. **Open Command Prompt** (Run as Administrator)
2. **Navigate to STOKY folder**:
   ```cmd
   cd "C:\Users\LL3922\Desktop\VS Code\private projects\STOKY"
   ```
3. **Start the backend server**:
   ```cmd
   python -m uvicorn app:app --host 0.0.0.0 --port 8001
   ```

### **Method 2: Using the Batch File I Created**
1. **Double-click** the file: `C:\Users\LL3922\Desktop\VS Code\private projects\STOKY\start_server.bat`
2. This will automatically start the server

### **Method 3: Using VS Code Terminal**
1. **Open Terminal** in VS Code (Ctrl + `)
2. **Run**:
   ```bash
   cd "C:\Users\LL3922\Desktop\VS Code\private projects\STOKY"
   python -m uvicorn app:app --host 0.0.0.0 --port 8001
   ```

## ✅ **Expected Results**

When the server starts successfully, you should see:
```
INFO:     Started server process [####]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
```

## 📱 **Test Your Mobile App**

Once the backend is running:

1. **Open STOKY app** on your phone
2. **Go to Search tab** 🔍
3. **Search for stocks** like:
   - **AAPL** (Apple)
   - **GOOGL** (Google)
   - **TSLA** (Tesla)
   - **PETR4.SA** (Petrobras - Brazilian stock)

## 🎯 **Success Indicators**

### **Backend Running**:
- ✅ Terminal shows "Uvicorn running on http://0.0.0.0:8001"
- ✅ You can access `http://10.105.22.220:8001/docs` in browser

### **Mobile App Connected**:
- ✅ Stock search returns results
- ✅ Real-time prices display
- ✅ No more "Connection refused" errors in logs

## 🌐 **Network Configuration**

- **Your Computer IP**: `10.105.22.220`
- **Backend Port**: `8001`
- **Mobile App Target**: `http://10.105.22.220:8001`
- **API Documentation**: `http://10.105.22.220:8001/docs`

## 📋 **Troubleshooting**

### **If Backend Won't Start**:
1. **Check if port 8001 is free**:
   ```cmd
   netstat -ano | findstr :8001
   ```
2. **Try a different port** (update mobile app accordingly):
   ```cmd
   python -m uvicorn app:app --host 0.0.0.0 --port 8002
   ```

### **If Mobile App Still Can't Connect**:
1. **Check Windows Firewall** - Allow Python through firewall
2. **Verify IP address** - Run `ipconfig` to confirm your IP
3. **Check network** - Ensure phone and computer are on same Wi-Fi

## 🚀 **Once Fixed**

Your STOKY mobile app will have:
- 📡 **Real-time stock data** from Yahoo Finance
- 🤖 **AI predictions** with confidence levels
- 💱 **Multi-currency support**
- 📈 **Professional stock analysis**
- 🔍 **Live search functionality**

**Start the backend server and your mobile app will be fully functional! 🎉📱💹**
