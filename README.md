# [Could Computing Demo] Phân tích cảm xúc 

* Tạo container 
```
docker build -t sentimentv1.azurecr.io/demo:v1  .
```

* Chạy container 
```
docker run -p 5000:80 sentimentv1.azurecr.io/demo:v1
```
