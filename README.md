# [Could Computing Demo] Phân tích cảm xúc 

* Tạo container 
```
docker build -t sentimentv1.azurecr.io/demo:v1  .
```

* Chạy container 
```
docker run -p 5000:80 sentimentv1.azurecr.io/demo:v1
```

* Truy cập vào web 
```
http://localhost:5000/
```

* Giao diện thu được
![sentiment_demo](https://user-images.githubusercontent.com/103992475/226181376-4de17df5-7819-41fa-9071-2120da10d865.png)
