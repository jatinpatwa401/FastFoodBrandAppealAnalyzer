# **Frontend Documentation**

## Laravel Installation for Windows
### `Step1: Install WAMP (version 3.2.0)`
* Requirement for WAMP:- Microsoft Visual C++ Redistributable.
* For running WAMP server, free port 80 usually occupied by Skype.
* WAMP further installs the following:
1. PHP 7.3.12
2. Apache 2.4.41
3. phpMyAdmin 4.9.2
* We have to explicitly install MySQL (version 8.0.18) by customizing installation.

### `Step 2:`
* Install composer from https://getcomposer.org/  
* Start wampserver.
* Create a database locally named cs226 utf8_general_ci in url: http://localhost/phpmyadmin/
  * During Login, under username and password. Change the server to MySQL from MariaDB.
* Import Dump20191204.sql in the visualisation/database/ directory.
* Download composer https://getcomposer.org/download/.
* Pull Laravel/php project from git provider https://github.com/yogesh696ksingh/Fast-Food-Chain-Analysis.git.
* Rename .env.example file to .env inside your project root and fill the database information.
  * Windows wont let you do it, so you have to open your console cd to your project root directory and run:
  ```
  mv .env.example .env
  ```
* Open the console and cd your project root directory.
* Run only one of the following commands:
  ```
  composer install
  ```
  or
  ```
  php composer.phar install
  ```
* Run the following commands:
  ```
  php artisan key:generate
  php artisan migrate
  php artisan serve
  ```
You can now access your project at localhost:8000! :)

**Note**: *Setup a MySQL database in .env file* </br>
// .env </br>
DB_CONNECTION=mysql </br>
DB_HOSY=127.0.0.1 </br>
DB_PORT=3306 </br>
DB_DATABASE=laravel </br>
DB_USERNAME=root 