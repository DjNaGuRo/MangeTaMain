FROM postgres:18-alpine3.22

# Set maintainer info
LABEL maintainer="guyrostan_nana@yahoo.fr"
LABEL description="Custom PostgreSQL image with MangeTaMain data"

# Create a non-root user for database operations
RUN addgroup -g 1001 -S postgres_app && \
    adduser -u 1001 -S postgres_app -G postgres_app

# Set environment variables with secure defaults
ENV POSTGRES_DB=mangetamain \
    POSTGRES_USER=postgres \
    POSTGRES_PASSWORD=postgres \
    PGDATA=/var/lib/postgresql/

# Create necessary directories
RUN mkdir -p /var/lib/postgresql/ && \
    mkdir -p /docker-entrypoint-initdb.d && \
    chown -R postgres:postgres /var/lib/postgresql && \
    chmod 700 /var/lib/postgresql/

# Copy initialization scripts
COPY init-scripts/ /docker-entrypoint-initdb.d/

# Copy your existing database data (if you have a backup)
COPY --chown=postgres:postgres ../../data/postgresDB/ /var/lib/postgresql/

# Expose PostgreSQL port
EXPOSE 5432

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD pg_isready -U $POSTGRES_USER -d $POSTGRES_DB

# Use the official postgres entrypoint
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["postgres"]

