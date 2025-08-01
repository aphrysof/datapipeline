

## Data Engineering Pipeline

### 1. Build the Airflow Docker Image

Navigate to the `aiwflow-db` directory and run:

```bash
docker build -t airflow-trino -f Dockerfile . --no-cache
```

This command builds a custom Airflow image, extending the official Airflow Docker image. The `Dockerfile` copies the `requirements.txt` file, allowing you to specify additional Python packages for Airflow. NB: Everytime you add package you need to rebuild the docker image.

### 2. Generate Airflow Configuration

Run:

```bash
docker compose run airflow-cli airflow config list
```

This generates the Airflow configuration file, which will be available in the `config` folder.

### 3. Initialize Airflow

Run:

```bash
docker compose up airflow-init
```

This step creates an admin user (`airflow`/`airflow`) for Airflow.

### 4. Start Trino Database Containers

Navigate to the `trino-db` directory and start the containers:

```bash
docker compose up -d
```

### 5. Initialize JDBC Catalog Tables in PostgreSQL

Connect to the PostgreSQL container:

```bash
docker exec -it trinio-db-iceberg_postgres-1 psql -U etl -d iceberg
```

Execute the following SQL statements to create the necessary tables:

```sql
CREATE TABLE iceberg_tables (
    catalog_name VARCHAR(255) NOT NULL,
    table_namespace VARCHAR(255) NOT NULL,
    table_name VARCHAR(255) NOT NULL,
    metadata_location VARCHAR(1000),
    previous_metadata_location VARCHAR(1000),
    PRIMARY KEY (catalog_name, table_namespace, table_name)
);

CREATE TABLE iceberg_namespace_properties (
    catalog_name VARCHAR(255) NOT NULL,
    namespace VARCHAR(255) NOT NULL,
    property_key VARCHAR(255),
    property_value VARCHAR(1000),
    PRIMARY KEY (catalog_name, namespace, property_key)
);
```

### 6. Restart Containers

After creating the tables, restart the Trino containers to apply changes.

### 7. Start Airflow Containers

Once Trino is running, start the Airflow containers. Airflow uses the Trino network for communication.

---

**Note:** Always start the Trino containers before Airflow to ensure proper network configuration.


