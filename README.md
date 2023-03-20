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
## 2. Tạo Azure Container Registry trên Azure và push image từ local lên ACR

* **Azure CLI:** là một cross-platform command-line tool có thể được cài đặt trên các máy tính cá nhân. Sử dụng Azure CLI để kết nối tới Azure và thực thi các lệnh quản trị (execute administrative commands) trên Azure resources. [Cài đặt Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux?pivots=apt)

* Login vào Azure Container Registry từ local 

  * Lưu ý: Thông tin để login in ACR lấy trong Access keys của ACR cần login
```
docker login --username [username on ACR] --password [password on ACR] [Login server]
```

* Push container image lên ACR 
```
docker push sentimentv1.azurecr.io/demo:v1
```

## 3. Tạo App Service trên Azure
* Vào App Services trên Azure để tạo app với ***Instance Details*** chọn là *Docker Container*
* App sau khi tạo trên Azure 
![FlaskApp](https://user-images.githubusercontent.com/103992475/226247328-e630c793-e1fe-454f-a022-466dab0da694.png)

* Truy cập vào web app theo url:
```
https://sentimentflaskapp.azurewebsites.net/
```

* Kết quả thu được
![SentimentApp](https://user-images.githubusercontent.com/103992475/226247710-4f63beb6-3ccc-4e15-8824-94e738a1e757.png)


