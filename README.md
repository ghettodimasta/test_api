# Test Work
## Install
1. pip install -r requirements.txt
2. connect postgres in post.py
3. python tables.py
4. python main.py
## Curl commands
1. To create product use:  
    curl --header "Content-Type: application/json" \  
      --request POST \  
      --data '{"name":"some_test_phone","description":"test_desc_with_curl","parametrs":{"camera": "12px", "color": "red"}}' \  
      http://localhost:5000/CreateProduct  

2. To get product by id use:  
    curl --header "Content-Type: application/json" \  
      --request POST \  
      --data '{"id":"21494"}' \  
      http://localhost:5000/GetParams  

3. To get filtered products name use:  
    curl --header "Content-Type: application/json" \   
      --request POST \  
      --data '{"name":"iph","param_key":"arch","param_value": "arm"}' \  
      http://localhost:5000/GetProducts  
      **NOTE!** *You can use either a name parameter, or a key parameter and a value parameter  if you try to use them together, you will take an error!*
