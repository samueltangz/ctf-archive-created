FROM php:7-apache

RUN docker-php-ext-install mysqli && docker-php-ext-enable mysqli

COPY src /var/www/html

RUN chown root /var/www/html -R

RUN chmod 555 /var/www/html -R
