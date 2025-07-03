python -m venv entorno
.\entorno\Scripts\activate.ps1
pip install -r dependencias.txt
docker pull postgres:16.9
docker run --name App_Security -e POSTGRES_PASSWORD=123 -d -p 5432:5432 postgres:16.9-bullseye
docker start App_Security
