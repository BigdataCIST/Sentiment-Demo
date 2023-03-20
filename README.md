# [Could Computing Demo] Phân tích cảm xúc 

## 1. Tạo container image tại local computer
* Tạo container 
```
docker build -t sentimentv1.azurecr.io/demo:v1  .
```

* Chạy container 
```
docker run -p 5000:500 sentimentv1.azurecr.io/demo:v1
```

* Truy cập vào web 
```
http://localhost:5000/
```
## 2. Tạo Azure Container Registry trên Azure 

* **Azure CLI:** là một cross-platform command-line tool có thể được cài đặt trên các máy tính cá nhân. Sử dụng Azure CLI để kết nối tới Azure và thực thi các lệnh quản trị (execute administrative commands) trên Azure resources. [Cài đặt Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux?pivots=apt)

* Login vào Azure Container Registry từ local 
```
docker login --username [username on ACR] --password [password on ACR] [Login server]
```

* Push container image lên ACR 
```
docker push sentimentv1.azurecr.io/demo:v1
```

## 3. Đẩy container image từ local pc lên Azure Container Registry

