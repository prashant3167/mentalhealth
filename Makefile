BACKUP_ZIP= backup.zip
BACKUP_URL='https://docs.google.com/uc?export=download&id=1C7a7HnYyqIAcvhz2li1gyWiTkXm4PZo'
# https://drive.google.com/file/d/1fyM5oCEHwzaEm7yTNwYZilrJdO8gGE67/view?usp=sharing  # Replace with the actual URL

.PHONY: run feature_engineering model_check_and_build start_frontend stop_frontend start_dagster stop_dagster setup_dashboard start_dashboard clean_resource all

#  Target to run feature engineering
feature_engineering:
	python3 train_model/feature_engineering.py

# Target to check and build the model
model_check_and_build:
	# Key is added for testing; otherwise, it needs to be removed 
	WANDB_API_KEY={WANDB_API_KEY} python3 train_model/train.py --check_model --count $(COUNT) --train_best_model

setup:
	@if [ -f $(BACKUP_ZIP) ]; then \
		echo "Setup already done"; \
	else \
		echo "$(BACKUP_ZIP) not found. Downloading..."; \
		wget --no-check-certificate $(BACKUP_URL) -O $(BACKUP_ZIP); \
		echo "Unzipping $(BACKUP_ZIP)..."; \
		unzip -o $(BACKUP_ZIP); \
	fi

# Start frontend and backend services using Docker Compose
start_frontend: setup
	@echo "Will start the the frontend and backend service"
	docker-compose up --build -d frontend backend
	clear
	@echo "\033[32mUI is available on http://localhost\033[0m"  # Green for UI
	@echo "\033[32mUI username: user and password: password\033[0m"

# Stop frontend and backend services
stop_frontend: 
	docker-compose down

# Start Dagster service using Docker Compose
start_dagster: setup
	docker-compose up --build -d dagster
	@echo -e "\033[34mOrchestrator is available on http://localhost:3000\033[0m"  # Blue for Orchestrator


# Stop Dagster service
stop_dagster:
	docker-compose stop dagster

# Set up the dashboard environment
setup_dashboard: setup
	@echo "Setting up the dashboard environment..."
	pip3 install -r dashboard/requirements.txt

# Start the dashboard
start_dashboard: setup_dashboard
	@echo "Starting the dashboard..."
	docker-compose up --build -d metabase
	clear
	@echo "\033[36mDashboard is available on http://127.0.0.1:3001/public/dashboard/855de8a6-5fd4-4d31-96da-7844bc0ba29e\033[0m"  # Cyan for Dashboard
	@echo "\033[36mDashboard username: fake-admin@example.com and password: fakepassword1\033[0m"

# Clean resources in the resources directory
clean_resource:
	@echo "Cleaning resources..."
	cd resources && rm -rf *
# Start all process
all: setup
	@echo "Starting all resources..."
	docker compose up --build -d
	clear
	@echo "\033[32mUI is available on http://localhost\033[0m"  # Green for UI
	@echo "\033[32mUI username: user and password: password\033[0m"

	@echo "\033[34mOrchestrator is available on http://localhost:3000\033[0m"  # Blue for Orchestrator

	@echo "\033[36mDashboard is available on http://localhost:3001/public/dashboard/855de8a6-5fd4-4d31-96da-7844bc0ba29e\033[0m"  # Cyan for Dashboard
	@echo "\033[36mDashboard username: fake-admin@example.com and password: fakepassword1\033[0m"

# Stop all process
stop:
	docker compose down