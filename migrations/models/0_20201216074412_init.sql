##### upgrade #####
CREATE TABLE IF NOT EXISTS `statistics_data_v2` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `meta_id` INT NOT NULL,
    `d_t` DATETIME(6) NOT NULL,
    `val` INT NOT NULL,
    UNIQUE KEY `uid_statistics__meta_id_961199` (`meta_id`, `d_t`)
) CHARACTER SET utf8mb4 COMMENT='统计数据 ';
CREATE TABLE IF NOT EXISTS `statistics_meta` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `project` INT NOT NULL,
    `title` VARCHAR(64) NOT NULL,
    `belong` VARCHAR(64) NOT NULL,
    `intro` VARCHAR(128) NOT NULL
) CHARACTER SET utf8mb4 COMMENT='meta ';
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(20) NOT NULL,
    `content` LONGTEXT NOT NULL
) CHARACTER SET utf8mb4;
