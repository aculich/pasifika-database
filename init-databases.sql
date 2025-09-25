-- Create databases for NodeGoat
CREATE DATABASE IF NOT EXISTS nodegoat_cms CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS nodegoat_home CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS nodegoat_content CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS nodegoat_temp CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create users
CREATE USER IF NOT EXISTS '1100CC_cms'@'%' IDENTIFIED BY 'nodegoat_password';
CREATE USER IF NOT EXISTS '1100CC_home'@'%' IDENTIFIED BY 'nodegoat_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON nodegoat_cms.* TO '1100CC_cms'@'%';
GRANT ALL PRIVILEGES ON nodegoat_home.* TO '1100CC_home'@'%';
GRANT ALL PRIVILEGES ON nodegoat_content.* TO '1100CC_cms'@'%';
GRANT ALL PRIVILEGES ON nodegoat_content.* TO '1100CC_home'@'%';
GRANT ALL PRIVILEGES ON nodegoat_temp.* TO '1100CC_cms'@'%';
GRANT ALL PRIVILEGES ON nodegoat_temp.* TO '1100CC_home'@'%';

FLUSH PRIVILEGES;
