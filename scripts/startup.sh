#!/bin/bash
set -e  # Exit on any error

# Logging function
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a /var/log/startup.log
}

log "Starting Quote App deployment"

# Update and install dependencies
log "Installing system dependencies..."
apt-get update
apt-get install -yq python3 python3-pip python3-venv git netcat-openbsd wget curl

# Create application directory
log "Creating application directory..."
mkdir -p /opt/quote-app
cd /opt/quote-app

# Create the Flask application files
log "Creating Flask application files..."
cat > app.py << 'PYTHON_APP'
${APP_PY_CONTENT}
PYTHON_APP

# Create database test script
cat > test_db.py << 'TEST_SCRIPT'
${TEST_DB_CONTENT}
TEST_SCRIPT

# Create requirements.txt
cat > requirements.txt << 'REQUIREMENTS'
${REQUIREMENTS_CONTENT}
REQUIREMENTS

# Create templates directory and files
log "Creating templates..."
mkdir -p templates
cat > templates/base.html << 'BASE_TEMPLATE'
${BASE_TEMPLATE_CONTENT}
BASE_TEMPLATE

cat > templates/index.html << 'INDEX_TEMPLATE'
${INDEX_TEMPLATE_CONTENT}
INDEX_TEMPLATE

cat > templates/browse.html << 'BROWSE_TEMPLATE'
${BROWSE_TEMPLATE_CONTENT}
BROWSE_TEMPLATE

cat > templates/authors.html << 'AUTHORS_TEMPLATE'
${AUTHORS_TEMPLATE_CONTENT}
AUTHORS_TEMPLATE

# Download and prepare the Cloud SQL Auth Proxy
log "Downloading Cloud SQL Auth Proxy..."
wget -q https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.15.2/cloud-sql-proxy.linux.amd64 -O cloud-sql-proxy
chmod +x cloud-sql-proxy

# Set database environment variables
log "Setting up environment variables..."
CONNECTION_NAME="${CONNECTION_NAME}"
export DB_HOST="127.0.0.1"
export DB_PORT="5432"
export DB_USER="${DB_USER}"
export DB_PASS="${DB_PASS}"
export DB_NAME="${DB_NAME}"

log "Cloud SQL Connection Name: $CONNECTION_NAME"

# Set up Python virtual environment
log "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
log "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create systemd service for Cloud SQL Auth Proxy
log "Creating Cloud SQL Auth Proxy service..."
cat > /etc/systemd/system/cloud-sql-proxy.service << 'PROXY_SERVICE'
[Unit]
Description=Google Cloud SQL Auth Proxy
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/quote-app
ExecStart=/opt/quote-app/cloud-sql-proxy ${CONNECTION_NAME} --port=5432 --quiet
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
PROXY_SERVICE

# Create systemd service for the application
log "Creating Flask application service..."
cat > /etc/systemd/system/quote-app.service << 'APP_SERVICE'
[Unit]
Description=Quote of the Day Flask Application
After=network.target cloud-sql-proxy.service
Requires=cloud-sql-proxy.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/quote-app
Environment=DB_HOST=127.0.0.1
Environment=DB_PORT=5432
Environment=DB_USER=${DB_USER}
Environment=DB_PASS=${DB_PASS}
Environment=DB_NAME=${DB_NAME}
ExecStart=/opt/quote-app/venv/bin/python app.py
Restart=always
RestartSec=30
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
APP_SERVICE

# Enable and start services
log "Starting services..."
systemctl daemon-reload
systemctl enable cloud-sql-proxy.service
systemctl enable quote-app.service

# Start Cloud SQL proxy first
systemctl start cloud-sql-proxy.service
sleep 15

# Wait for proxy to be ready
log "Waiting for Cloud SQL Auth Proxy..."
for i in {1..30}; do
    if nc -z 127.0.0.1 5432; then
        log "Cloud SQL Auth Proxy is ready!"
        break
    fi
    log "Attempt $i: Waiting for proxy..."
    sleep 2
done

# Test database connection
log "Testing database connection..."
if python3 test_db.py; then
    log "Database connection test PASSED"
else
    log "Database connection test FAILED"
fi

# Start the Flask application
systemctl start quote-app.service

# Wait for app to be ready
log "Waiting for Flask application..."
for i in {1..30}; do
    if curl -f http://localhost/api/health > /dev/null 2>&1; then
        log "Flask application is ready!"
        break
    fi
    log "Attempt $i: Waiting for Flask app..."
    sleep 3
done

log "Quote app deployment completed successfully!"
