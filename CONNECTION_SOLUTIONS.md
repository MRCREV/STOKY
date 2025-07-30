# 🌐 STOKY Mobile Connection Solutions

## 🚨 **Problem**: PC Firewall/Network Blocking Mobile Connection

Your computer is blocking incoming connections from your mobile device. Here are several solutions:

## 🔥 **Solution 1: Cloud Tunnel (Recommended)**

### **Using ngrok (Free)**
1. **Download ngrok**: https://ngrok.com/download
2. **Extract to STOKY folder**
3. **Start your backend**:
   ```cmd
   python -m uvicorn app:app --host 127.0.0.1 --port 8000
   ```
4. **In another terminal, run ngrok**:
   ```cmd
   ngrok http 8000
   ```
5. **Copy the https URL** (e.g., `https://abc123.ngrok.io`)
6. **Update mobile app** with this URL

### **Using Cloudflare Tunnel (Free)**
1. **Install cloudflared**: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/
2. **Run**:
   ```cmd
   cloudflared tunnel --url http://localhost:8000
   ```

## 🔥 **Solution 2: USB Debugging (Direct)**

### **Android ADB Port Forwarding**
1. **Enable USB Debugging** on your phone
2. **Connect via USB cable**
3. **Run ADB command**:
   ```cmd
   adb reverse tcp:8000 tcp:8000
   ```
4. **Update mobile app** to use `http://localhost:8000`

## 🔥 **Solution 3: Hotspot Connection**

### **Use Phone as Hotspot**
1. **Enable Mobile Hotspot** on your phone
2. **Connect PC to phone's Wi-Fi**
3. **Find phone's IP** (usually 192.168.43.1)
4. **Update mobile app** to use phone's IP

## 🔥 **Solution 4: Deploy to Cloud (Professional)**

### **Quick Deploy Options**
- **Railway**: https://railway.app (Free tier)
- **Render**: https://render.com (Free tier)
- **Vercel**: https://vercel.com (Free tier)
- **Heroku**: https://heroku.com (Free tier)

## 🎯 **Recommended: ngrok Solution**

**Most reliable and fastest to set up:**

1. **Download ngrok** and put in STOKY folder
2. **Start backend**: `python -m uvicorn app:app --port 8000`
3. **Start ngrok**: `ngrok http 8000`
4. **Get public URL** like `https://abc123.ngrok.io`
5. **Update mobile app** to use this URL

## 📱 **Mobile App Update**

Once you have the new URL, update:
`lib/services/stock_api_service.dart`

```dart
static const String baseUrl = 'https://your-ngrok-url.ngrok.io'; // No port needed
```

## 🚀 **Benefits of Each Solution**

**ngrok**: ✅ Fast, secure, works anywhere
**ADB**: ✅ No internet needed, direct connection
**Hotspot**: ✅ Simple, uses phone's internet
**Cloud**: ✅ Professional, always accessible

**Which solution would you like to try first?**
