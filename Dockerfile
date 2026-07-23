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
# Stage 2: Unit Testing (HTMLProofer & Link Audit)
# ---------------------------------------------------
FROM builder AS test
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
COPY --from=builder /srv/jekyll/_site /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
