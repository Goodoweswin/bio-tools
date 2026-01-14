# Bio-Tools 私有化部署指南 (Offline Deployment Guide)

本指南旨在帮助您将 `bio-tools-server-deploy.zip` 部署到私有服务器（如 Ubuntu/CentOS/Windows），实现 **100% 离线运行**。

## 📦 准备工作 (Prerequisites)

1.  **服务器环境**:
    - 操作系统: Linux (推荐 Ubuntu/CentOS), Windows Server, 或 macOS。
    - 网络: 最好能临时连接一次外网（下载 Scipy），或者在本地下载好再上传。
    - **Web 服务器**: Nginx (推荐), Apache, Caddy, 或 IIS。
    - **Python 3**: 用于运行初始化脚本（仅首次需要）。

2.  **部署包**:
    - 请确保您已获取 `bio-tools-server-deploy.zip`。

---

## 🚀 部署步骤 (Step-by-Step)

### 第一步：上传与解压
将 zip 包上传到服务器的 Web 根目录（例如 `/var/www/html` 或 `/opt/biotools`）。

```bash
# 示例 (Linux)
mkdir -p /opt/biotools
cp bio-tools-server-deploy.zip /opt/biotools/
cd /opt/biotools
unzip bio-tools-server-deploy.zip
```

### 第二步：开启离线模式 (一键补全)
**这是最关键的一步**。运行脚本会自动下载缺少的 41MB Scipy 文件，并将配置切换为本地模式。

```bash
# 确保在解压后的目录中
python3 enable_offline_mode.py
```

> **输出示例**:
> ```
> --- Switching to OFFLINE MODE ---
> Downloading scipy-1.11.2... (41MB)
> Download complete.
> Updating pyodide-lock.json to use LOCAL file...
> Updated hash to: ...
> SUCCESS: Project is now configured for fully offline self-hosting.
> ```

**如果不通外网 (Air-Gapped)**:
如果服务器完全断网，脚本会报错。您需要：
1. 在**有网的机器**上运行脚本下载文件。
2. 将生成的 `public/tools/assets/pyodide/scipy-*.whl` 和更新后的 `pyodide-lock.json` 复制到服务器对应目录覆盖。

---

### 第三步：配置 Web 服务器 (Nginx)

将 `public` 文件夹作为静态网站根目录。

**推荐 Nginx 配置 (`/etc/nginx/sites-available/biotools.conf`)**:

```nginx
server {
    listen 80;
    server_name your-server-ip-or-domain.com;

    # 静态文件根目录
    root /opt/biotools/public;
    index index.html;

    # 开启 gzip 压缩 (对 WASM/JS 非常重要)
    gzip on;
    gzip_types text/plain application/json application/javascript text/css application/xml application/wasm;
    gzip_min_length 1000;

    # 缓存控制
    location /tools/assets/ {
        # 依赖包缓存 1 年
        expires 1y;
        add_header Cache-Control "public, no-transform";
    }

    # SPA路由支持 (如果未来需要)
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

### 第四步：启动服务
```bash
# 测试配置
sudo nginx -t
# 重启 Nginx
sudo systemctl reload nginx
```

---

## ✅ 验证
打开浏览器访问您的服务器 IP。
1. 进入 "Statistical Analysis" 工具。
2. 打开浏览器控制台 (F12 -> Network)。
3. 刷新页面，观察 `pyodide.js`, `pandas.whl`, `scipy.whl` 等请求。
4. **成功标志**: 所有请求的状态码应为 **200 (from disk cache)** 或 **200 (server IP)**，**绝不应出现** 指向 `cdn.jsdelivr.net` 或 `pyodide-cdn2.iodide.io` 的请求。

---

## 🛠️ 常见问题

**Q: 为什么 enable_offline_mode.py 报错 SSL Error?**
A: 您的服务器可能也是老旧系统或 SSL 证书未更新。尝试编辑脚本，在 request 中添加 `context=ssl._create_unverified_context()` (脚本中已默认处理，但如果依然报错，请检查网络防火墙)。

**Q: 只有 Web 服务器，没有 Python 怎么办?**
A: 在您的**本地电脑**上解压 zip，运行脚本补全文件，然后将整个完整的文件夹上传到服务器。
