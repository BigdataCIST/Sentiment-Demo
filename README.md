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

## 3. Đẩy container image từ local pc lên Azure Container Registry
