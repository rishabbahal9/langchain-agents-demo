# Langchain agents demo
### AI recipe generator based on ingredients and cuisine

## How to run the app
1. Clone the repository
2. Create .env file with the help of .env.example
3. Run the following commands (Make sure Docker is installed & running)
```bash
docker build --tag langchain-demo . 
``` 

```bash
docker run -d -p 8000:5000 --rm langchain-demo
```
4. Open the browser and go to http://localhost:8000
