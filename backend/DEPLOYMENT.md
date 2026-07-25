"""
Deploy instructions for production environment
"""

# Production Deployment Guide

## Pre-Deployment Checklist

- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] SSL/TLS certificates obtained
- [ ] OAuth credentials configured
- [ ] S3 bucket configured
- [ ] Backups configured
- [ ] Monitoring setup

## Deployment Options

### Option 1: Docker on AWS ECS

```bash
# Build Docker image
docker build -f Dockerfile.backend -t window-to-russia-backend:latest .

# Push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ECR_URI>
docker tag window-to-russia-backend:latest <ECR_URI>/window-to-russia-backend:latest
docker push <ECR_URI>/window-to-russia-backend:latest

# Deploy to ECS (using CloudFormation or AWS Console)
```

### Option 2: Heroku

```bash
# Login to Heroku
heroku login

# Create app
heroku create window-to-russia-backend

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:standard-0 -a window-to-russia-backend

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key -a window-to-russia-backend
heroku config:set ENVIRONMENT=production -a window-to-russia-backend
# ... set all other variables

# Deploy
git push heroku develop/backend-setup:main
```

### Option 3: DigitalOcean App Platform

```bash
# Push code to repository
git push origin develop/backend-setup

# Create app.yaml
echo "name: window-to-russia-backend" > app.yaml
# ... configure app.yaml

# Deploy using doctl
doctl apps create --spec app.yaml
```

## Environment Configuration

### Production .env

```env
APP_NAME=Window to RUSSIA
DEBUG=False
ENVIRONMENT=production
SERVER_HOST=0.0.0.0
SERVER_PORT=8000

# Database (use managed service)
DATABASE_URL=postgresql://prod_user:secure_password@prod-db.example.com:5432/window_to_russia
DATABASE_POOL_SIZE=30
DATABASE_MAX_OVERFLOW=20

# Redis (use managed service)
REDIS_URL=redis://prod-redis.example.com:6379/0

# JWT
SECRET_KEY=generate-with: python -c "import secrets; print(secrets.token_urlsafe(32))"
ALGORITHM=HS256

# CORS
CORS_ORIGINS=["https://windowtorussia.com","https://app.windowtorussia.com"]

# OAuth Providers (production credentials)
GOOGLE_CLIENT_ID=prod-google-id
GOOGLE_CLIENT_SECRET=prod-google-secret
GOOGLE_REDIRECT_URI=https://api.windowtorussia.com/api/v1/auth/oauth/google/callback
# ... other providers

# AWS S3
AWS_ACCESS_KEY_ID=prod-access-key
AWS_SECRET_ACCESS_KEY=prod-secret-key
AWS_S3_BUCKET_NAME=window-to-russia-prod
AWS_S3_REGION=us-east-1

# Email
SMTP_SERVER=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=sendgrid-api-key

# Logging
LOG_LEVEL=INFO
```

## Infrastructure Requirements

### Database (PostgreSQL)
- Version: 14+
- Instance: db.t3.small or larger
- Storage: 100GB+ (auto-scale)
- Backups: Daily automated
- Replicas: At least 1 standby

### Cache (Redis)
- Version: 7+
- Instance: cache.t3.small or larger
- Eviction policy: allkeys-lru
- Backups: Daily snapshots

### Application Server
- Python 3.11
- Gunicorn: 4 workers per CPU core
- Memory: 2GB+ per worker
- Load balancer: AWS ALB or NGINX

### Storage (S3)
- Bucket: Private
- Versioning: Enabled
- Lifecycle: Delete old versions after 30 days
- CDN: CloudFront distribution

## Deployment Script

```bash
#!/bin/bash
set -e

echo "Starting production deployment..."

# Pull latest code
git pull origin develop/backend-setup

# Build Docker image
docker build -f Dockerfile.backend -t window-to-russia-backend:$(git rev-parse --short HEAD) .

# Push to registry
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REGION=us-east-1
ECR_REGISTRY=$AWS_ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com
REPOSITORY_NAME=window-to-russia-backend

aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ECR_REGISTRY
docker tag window-to-russia-backend:$(git rev-parse --short HEAD) $ECR_REGISTRY/$REPOSITORY_NAME:latest
docker push $ECR_REGISTRY/$REPOSITORY_NAME:latest

# Deploy to ECS
aws ecs update-service \
  --cluster window-to-russia-prod \
  --service backend \
  --force-new-deployment

echo "Deployment complete!"
```

## Monitoring & Logging

### CloudWatch Configuration

```python
# Python logging to CloudWatch
import watchtower
import logging

logging.basicConfig(
    level=logging.INFO,
    handlers=[
        watchtower.CloudWatchLogHandler(
            log_group='window-to-russia-backend',
            stream_name='backend-app'
        )
    ]
)
```

### Performance Monitoring

- **APM**: New Relic or DataDog
- **Error Tracking**: Sentry
- **Uptime Monitoring**: StatusPage.io
- **Metrics**: Prometheus + Grafana

## Security

- [ ] Enable HTTPS/TLS
- [ ] Configure WAF rules
- [ ] Setup DDoS protection (AWS Shield)
- [ ] Enable VPC security groups
- [ ] Regular security audits
- [ ] Dependency scanning (Snyk)
- [ ] Secrets rotation (AWS Secrets Manager)

## Backup & Disaster Recovery

### Database Backups
```bash
# Automated daily backups with AWS RDS
# Retention: 30 days
# Multi-AZ deployment for high availability
```

### Restore Procedure
```bash
# Restore from snapshot
aws rds restore-db-instance-from-db-snapshot \
  --db-instance-identifier window-to-russia-restored \
  --db-snapshot-identifier window-to-russia-snapshot
```

## Post-Deployment Verification

```bash
# Check health
curl https://api.windowtorussia.com/health

# Check API
curl https://api.windowtorussia.com/api/v1/themes/today

# Monitor logs
aws logs tail /aws/ecs/window-to-russia-backend --follow
```

---

**Last Updated:** 2026-07-25
"""
