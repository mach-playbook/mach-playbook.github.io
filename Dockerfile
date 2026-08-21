# Exact Ruby version matching GitHub Actions pages-deploy.yml (Ruby 3.4)
FROM ruby:3.4-slim AS builder

# Install build dependencies required for compiling native gem extensions and node.js
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    libvips-dev \
    curl \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /srv/jekyll

# Copy dependency definition files for Docker caching
COPY Gemfile Gemfile.lock* ./

# Install Ruby gems (including Chirpy theme and html-proofer)
RUN gem install bundler && \
    bundle config set --local path 'vendor/bundle' && \
    bundle install

# Copy entire application source code
COPY . .

# Environment variable matching GitHub Actions production environment
ENV JEKYLL_ENV=production

# 1. Build the static site artifact exactly as GitHub Pages CI/CD does
RUN bundle exec jekyll build -d _site

# ---------------------------------------------------
# Stage 2: Unit Testing (HTMLProofer & Site Integrity Validation)
# ---------------------------------------------------
FROM builder AS test
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-bs4 && \
    python3 scripts/test-site-integrity.py && \
    rm -rf /var/lib/apt/lists/*
RUN bundle exec htmlproofer _site \
    --disable-external \
    --ignore-urls "/^http:\/\/127.0.0.1/,/^http:\/\/0.0.0.0/,/^http:\/\/localhost/"

# ---------------------------------------------------
# Stage 3: Local Development Server (Jekyll Server)
# ---------------------------------------------------
FROM builder AS dev
EXPOSE 4000
CMD ["bundle", "exec", "jekyll", "serve", "--host", "0.0.0.0", "--force_polling"]

# ---------------------------------------------------
# Stage 4: Production Replica Web Server (Nginx)
# ---------------------------------------------------
FROM nginx:alpine AS prod
RUN printf 'server {\n\
    listen 80;\n\
    server_name localhost;\n\
    root /usr/share/nginx/html;\n\
    index index.html;\n\
    gzip on;\n\
    gzip_vary on;\n\
    gzip_min_length 256;\n\
    gzip_proxied any;\n\
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript image/svg+xml;\n\
    location / {\n\
        try_files $uri $uri/ /index.html =404;\n\
    }\n\
    location ~* \\.(?:css|js|jpg|jpeg|gif|png|ico|svg|webp|woff|woff2|ttf|eot)$ {\n\
        expires 1y;\n\
        add_header Cache-Control "public, max-age=31536000, immutable";\n\
    }\n\
}\n' > /etc/nginx/conf.d/default.conf

COPY --from=builder /srv/jekyll/_site /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
