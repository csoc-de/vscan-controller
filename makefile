up:
	@echo "🧹 Bereinige Ordner gvm_socket mit sudo..."
	@if [ -d "gvm_socket" ]; then \
		sudo rm -rf gvm_socket/*; \
		echo "✅ Dateien in gvm_socket gelöscht."; \
	else \
		mkdir -p gvm_socket; \
		echo "ℹ️ Ordner gvm_socket wurde erstellt."; \
	fi
	@echo "🚀 Starte Docker Compose..."
	docker compose up -d

down:
	@echo "🛑 Stoppe Docker Compose..."
	docker compose down

restart: down up
	@echo "✅ Neustart abgeschlossen."

.PHONY: up down restart