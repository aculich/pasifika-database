FROM php:8.1-apache

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpng-dev \
    libjpeg-dev \
    libfreetype6-dev \
    libzip-dev \
    libxml2-dev \
    libcurl4-openssl-dev \
    libonig-dev \
    libpq-dev \
    unzip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install PHP extensions
RUN docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install -j$(nproc) \
        gd \
        mbstring \
        mysqli \
        pdo_mysql \
        pdo_pgsql \
        curl \
        zip \
        xml \
        intl \
        bcmath

# Enable Apache modules
RUN a2enmod rewrite headers deflate

# Set working directory
WORKDIR /var/1100CC

# Copy 1100CC files
COPY 1100CC/ /var/1100CC/

# Copy NodeGoat files
COPY nodegoat/APP/nodegoat/ /var/1100CC/APP/nodegoat/
COPY nodegoat/APP/SETTINGS/nodegoat/ /var/1100CC/APP/SETTINGS/nodegoat/
COPY nodegoat/APP/STORAGE/nodegoat/ /var/1100CC/APP/STORAGE/nodegoat/

# Set permissions
RUN chown -R www-data:www-data /var/1100CC \
    && chmod -R 755 /var/1100CC

# Configure Apache
COPY apache-config.conf /etc/apache2/sites-available/000-default.conf

# Expose port
EXPOSE 80

# Start Apache
CMD ["apache2-foreground"]
