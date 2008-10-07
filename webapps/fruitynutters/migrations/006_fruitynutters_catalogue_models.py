from dmigrations.mysql import migrations as m
import datetime
migration = m.Migration(sql_up=["""
    CREATE TABLE `catalogue_aisle` (
        `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
        `name` varchar(60) NOT NULL,
        `description` longtext NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    ;
""", """
    CREATE TABLE `catalogue_brand` (
        `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
        `name` varchar(60) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    ;
""", """
    CREATE TABLE `catalogue_item` (
        `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
        `name` varchar(60) NOT NULL,
        `aisle_id` integer NOT NULL,
        `brand_id` integer NULL,
        `description` longtext NULL,
        `active` bool NOT NULL,
        `organic` bool NOT NULL,
        `date_created` date NOT NULL,
        `date_updated` date NOT NULL,
        `new_changed` bool NOT NULL,
        `bundle_id` integer NULL,
        `unit_number` integer UNSIGNED NOT NULL,
        `measure_per_unit` double precision NULL,
        `measure_type` varchar(10) NULL,
        `price` numeric(4, 2) NULL,
        `price_change` varchar(30) NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    ;
""", """
    ALTER TABLE `catalogue_item` ADD CONSTRAINT aisle_id_refs_id_74ace8fd FOREIGN KEY (`aisle_id`) REFERENCES `catalogue_aisle` (`id`);
""", """
    ALTER TABLE `catalogue_item` ADD CONSTRAINT brand_id_refs_id_4f32d17c FOREIGN KEY (`brand_id`) REFERENCES `catalogue_brand` (`id`);
""", """
    CREATE TABLE `catalogue_bundle` (
        `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
        `name` varchar(30) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    ;
""", """
    ALTER TABLE `catalogue_item` ADD CONSTRAINT bundle_id_refs_id_7639b2f8 FOREIGN KEY (`bundle_id`) REFERENCES `catalogue_bundle` (`id`);
""", """
    CREATE TABLE `catalogue_bundle_items` (
        `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
        `bundle_id` integer NOT NULL,
        `item_id` integer NOT NULL,
        UNIQUE (`bundle_id`, `item_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    ;
""", """
    ALTER TABLE `catalogue_bundle_items` ADD CONSTRAINT bundle_id_refs_id_2b960828 FOREIGN KEY (`bundle_id`) REFERENCES `catalogue_bundle` (`id`);
""", """
    ALTER TABLE `catalogue_bundle_items` ADD CONSTRAINT item_id_refs_id_363268d5 FOREIGN KEY (`item_id`) REFERENCES `catalogue_item` (`id`);
"""], sql_down=["""
    DROP TABLE `catalogue_bundle_items`;
""", """
    ALTER TABLE `catalogue_item` DROP FOREIGN KEY bundle_id_refs_id_7639b2f8;
""", """
    DROP TABLE `catalogue_bundle`;
""", """
    DROP TABLE `catalogue_item`;
""", """
    DROP TABLE `catalogue_brand`;
""", """
    DROP TABLE `catalogue_aisle`;
"""])
