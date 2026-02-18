# Gym API — FastAPI + PostgreSQL (Docker)

##  Como rodar o projeto

### 1️Clonar o repositório

```bash
git clone https://github.com/BrennoSantos12/gym-api.git
cd gym-api
```

---

### 2️Criar arquivo `.env` na raiz do projeto

Crie um arquivo chamado `.env`:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/academia
SECRET_KEY=sua_chave_secreta_aqui
```

> Dentro do Docker o banco não é `localhost`, é `db`.

---

### 3️Subir os containers

```bash
docker compose up -d --build
```

---

### 4️Rodar as migrations

```bash
docker compose exec api alembic upgrade head
```
---

### Rodar os seeders

```bash
docker compose exec api python -m app.seeds.run
```

---

## 📚 Acessar a API

Swagger:

```
http://localhost:8000/docs
```

---

## 🛑 Parar containers

```bash
docker compose down
```
