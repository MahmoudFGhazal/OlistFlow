include .env
export

.PHONY: reset run test logs psql

# Limpa a tabela cities (e o que tiver FK pra ela) e reseta o auto-incremento
reset:
	docker compose exec postgres psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) \
		-c "TRUNCATE TABLE core.cities RESTART IDENTITY CASCADE;"

# Só roda o ETL
run:
	python main.py

# Reseta e já roda o ETL em seguida///
test: reset run

# Atalho pra ver os logs do container do postgres
logs:
	docker compose logs postgres --tail=40

# Abre um psql interativo dentro do container
psql:
	docker compose exec postgres psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)