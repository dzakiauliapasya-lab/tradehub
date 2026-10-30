-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 30, 2026 at 12:28 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tradehub`
--

--
-- Dumping data for table `carts`
--

INSERT INTO `carts` (`id`, `user_id`, `created_at`, `updated_at`) VALUES
(1, 2, '2026-10-29 15:59:41', '2026-10-29 15:59:41');

--
-- Dumping data for table `cart_items`
--

INSERT INTO `cart_items` (`id`, `cart_id`, `product_id`, `quantity`, `created_at`, `updated_at`) VALUES
(2, 1, 1, 1, '2026-10-29 16:10:03', '2026-10-29 16:10:03'),
(3, 1, 3, 1, '2026-10-29 16:12:10', '2026-10-29 16:12:10');

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `parent_id`, `name`, `slug`, `description`, `created_at`) VALUES
(1, NULL, 'Elektronik', 'elektronik', 'Gadget, laptop, dan perangkat elektronik', '2026-10-24 14:41:39'),
(2, NULL, 'Fashion', 'fashion', 'Pakaian, sepatu, dan aksesoris', '2026-10-24 14:41:39'),
(3, NULL, 'Rumah Tangga', 'rumah-tangga', 'Perabot dan perlengkapan rumah', '2026-10-24 14:41:39'),
(4, NULL, 'Hobi & Koleksi', 'hobi-koleksi', 'Buku, mainan, dan barang koleksi', '2026-10-24 14:41:39'),
(5, NULL, 'Olahraga', 'olahraga', 'Perlengkapan olahraga dan outdoor', '2026-10-24 14:41:39');

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `order_number`, `buyer_id`, `shipping_name`, `shipping_phone`, `shipping_address`, `subtotal`, `shipping_cost`, `total_amount`, `payment_method`, `payment_status`, `status`, `notes`, `created_at`, `updated_at`) VALUES
(1, 'TH-20261029-957AE8C4', 2, 'Sari Pembeli', '081234567890', 'Jl. Melati No. 10, Stabat, Langkat', 400000.00, 15000.00, 415000.00, 'Transfer Bank', 'paid', 'completed', 'string', '2026-10-29 16:23:13', '2026-10-30 01:57:28');

--
-- Dumping data for table `order_items`
--

INSERT INTO `order_items` (`id`, `order_id`, `product_id`, `store_id`, `product_name`, `price`, `quantity`, `subtotal`, `created_at`) VALUES
(1, 1, 2, 1, 'Boneka Miku', 400000.00, 1, 400000.00, '2026-10-29 16:23:13');

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `store_id`, `category_id`, `name`, `slug`, `description`, `price`, `stock`, `condition_type`, `status`, `created_at`, `updated_at`) VALUES
(1, 1, 1, 'iPhone 12 128GB Bekas Mulus', 'iphone-12-128gb-bekas-mulus-2b22a3', 'Fullset, baterai 89%', 4500000.00, 3, 'used', 'active', '2026-10-29 15:27:52', '2026-10-29 15:27:52'),
(2, 1, 4, 'Boneka Miku', 'boneka-miku-78fc42', 'Masih mulus dan wangi', 400000.00, 0, 'used', 'sold_out', '2026-10-29 15:34:13', '2026-10-29 16:23:13'),
(3, 1, 2, 'Baju furina fullset', 'baju-furina-fullset-a37fc4', 'baru pakai sekali bekas cosplayer', 6000000.00, 1, 'used', 'active', '2026-10-29 15:37:46', '2026-10-29 15:37:46');

--
-- Dumping data for table `product_images`
--

INSERT INTO `product_images` (`id`, `product_id`, `image_url`, `is_primary`, `sort_order`, `created_at`) VALUES
(1, 1, 'https://www.tokopedia.com/irmacell-1/iphone-12-128gb-ibox-bh-90-black?utm_source=google&utm_medium=organic&utm_campaign=pdp', 1, 0, '2026-10-29 15:27:52'),
(2, 2, 'https://shopee.co.id/-PRE-ORDER-Boneka-Hatsune-Miku-Vocaloid-Cotton-Doll-Soft-Plush-i.69882285.19125850589', 1, 0, '2026-10-29 15:34:13'),
(3, 3, 'https://shopee.co.id/Genshin-Impact-Furina-De-Fontaine-Women-Cosplay-Costume-Cos-Game-Anime-Party-Uniform-Hallowen-Play-Role-Clothes-Clothing-i.816523638.24336598616', 1, 0, '2026-10-29 15:37:46');

--
-- Dumping data for table `reviews`
--

INSERT INTO `reviews` (`id`, `user_id`, `product_id`, `order_item_id`, `rating`, `comment`, `created_at`, `updated_at`) VALUES
(1, 2, 2, 1, 5, 'masih mulus kayak baru', '2026-10-30 02:02:07', '2026-10-30 02:02:07');

--
-- Dumping data for table `stores`
--

INSERT INTO `stores` (`id`, `user_id`, `name`, `slug`, `description`, `address`, `logo_url`, `status`, `created_at`, `updated_at`) VALUES
(1, 1, 'Budi Gadget Store', 'budi-gadget-store-cd34f2', 'Jual gadget bekas & baru', 'Stabat, Sumatera Utara', NULL, 'active', '2026-10-29 15:00:00', '2026-10-30 02:26:24'),
(2, 4, 'benerin.id', 'benerin-id-18e954', 'Segala part dan komponen part pc atau laptop beserta aksesoris', 'Banda Aceh, Sumatera', NULL, 'active', '2026-10-30 11:01:54', '2026-10-30 11:04:55');

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password_hash`, `phone`, `address`, `role`, `is_active`, `created_at`, `updated_at`) VALUES
(1, 'Budi Penjual', 'budi@gmail.com', '$2b$12$CTeGfsSWCsaPKPQarPsjCOBooUlFCuzFS4KQoSb4u08Y5sblBGHHW', 'string', NULL, 'seller', 1, '2026-10-27 12:33:31', '2026-10-27 12:33:31'),
(2, 'string', 'sari@gmail.com', '$2b$12$4W4VtVFPmFcg3EDqnPrrS.mPS/riFhjXuqz9R.mJ4M1.Sc5sUWO7O', 'string', 'Jl. Mawar No. 5, Stabat', 'buyer', 1, '2026-10-29 14:36:34', '2026-10-29 14:45:32'),
(3, 'admin', 'admin@tradehub.com', '$2b$12$nM0d5PYEvi7cHrRQ/l51tud0tpqqn7iy4BOcrDL6Gyvz0FpAOsVoS', 'Iphone 18 PRO MAX', NULL, 'admin', 1, '2026-10-30 02:06:51', '2026-10-30 02:07:05'),
(4, 'rex', 'rex@gmail.com', '$2b$12$kdtlQ6Za8gHHcEhdStl4l.QHK7Sw0GlpcTXYQC.n2c3ulGub/cl8m', 'Poco F7', NULL, 'seller', 1, '2026-10-30 02:11:01', '2026-10-30 02:11:01');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
