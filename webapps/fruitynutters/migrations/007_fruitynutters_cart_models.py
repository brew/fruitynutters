from dmigrations.mysql import migrations as m
import datetime
migration = m.Migration(sql_up=["""
    CREATE TABLE `cart_cart` (
        `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
        `date_created` date NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    ;
""", """
    CREATE TABLE `cart_cartitem` (
        `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
        `cart_id` integer NOT NULL,
        `product_id` integer NOT NULL,
        `quantity` integer NOT NULL,
        `cart_bundle_id` integer NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    ;
""", """
    ALTER TABLE `cart_cartitem` ADD CONSTRAINT cart_id_refs_id_c970e5a FOREIGN KEY (`cart_id`) REFERENCES `cart_cart` (`id`);
""", """
    ALTER TABLE `cart_cartitem` ADD CONSTRAINT product_id_refs_id_73a2a46b FOREIGN KEY (`product_id`) REFERENCES `catalogue_item` (`id`);
""", """
    CREATE TABLE `cart_cartbundle` (
        `cart_ptr_id` integer NOT NULL PRIMARY KEY
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    ;
""", """
    ALTER TABLE `cart_cartbundle` ADD CONSTRAINT cart_ptr_id_refs_id_5231f7f FOREIGN KEY (`cart_ptr_id`) REFERENCES `cart_cart` (`id`);
""", """
    ALTER TABLE `cart_cartitem` ADD CONSTRAINT cart_bundle_id_refs_cart_ptr_id_7caeda34 FOREIGN KEY (`cart_bundle_id`) REFERENCES `cart_cartbundle` (`cart_ptr_id`);
""", """
    CREATE TABLE `cart_cartbundle_cart_items` (
        `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
        `cartbundle_id` integer NOT NULL,
        `cartitem_id` integer NOT NULL,
        UNIQUE (`cartbundle_id`, `cartitem_id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8
    ;
""", """
    ALTER TABLE `cart_cartbundle_cart_items` ADD CONSTRAINT cartbundle_id_refs_cart_ptr_id_982f798 FOREIGN KEY (`cartbundle_id`) REFERENCES `cart_cartbundle` (`cart_ptr_id`);
""", """
    ALTER TABLE `cart_cartbundle_cart_items` ADD CONSTRAINT cartitem_id_refs_id_5bab7719 FOREIGN KEY (`cartitem_id`) REFERENCES `cart_cartitem` (`id`);
"""], sql_down=["""
    DROP TABLE `cart_cartbundle_cart_items`;
""", """
    ALTER TABLE `cart_cartitem` DROP FOREIGN KEY cart_bundle_id_refs_cart_ptr_id_7caeda34;
""", """
    DROP TABLE `cart_cartbundle`;
""", """
    DROP TABLE `cart_cartitem`;
""", """
    DROP TABLE `cart_cart`;
"""])
