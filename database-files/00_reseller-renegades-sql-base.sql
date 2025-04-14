DROP DATABASE IF EXISTS reThread;
CREATE DATABASE reThread;
USE reThread;

CREATE TABLE Location (
    location_id int PRIMARY KEY NOT NULL,
    city VARCHAR(100),
    state VARCHAR(100),
    zip VARCHAR(20),
    university VARCHAR(100)
);

CREATE TABLE Demographic (
    demographic_id int PRIMARY KEY NOT NULL,
    age VARCHAR(50),
    gender VARCHAR(20),
    location_id INT REFERENCES Location(location_id)
);

CREATE TABLE User (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    role VARCHAR(50),
    location_id INT REFERENCES Location(location_id),
    demographic_id INT REFERENCES Demographic(demographic_id)
);


CREATE TABLE `Group` (
    group_id int PRIMARY KEY NOT NULL,
    created_by INT REFERENCES User(user_id) ON DELETE SET NULL,
    name VARCHAR(100),
    type VARCHAR(50)
);

CREATE TABLE Tag (
    tag_id int PRIMARY KEY NOt NULL,
    tag_name VARCHAR(100)
);

CREATE TABLE Listing (
    listing_id int PRIMARY KEY NOT NULL,
    title VARCHAR(255),
    description TEXT,
    price DECIMAL(10,2),
    `condition` VARCHAR(100),
    brand VARCHAR(100),
    size VARCHAR(10),
    material VARCHAR(100),
    color VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    seller_id INT REFERENCES User(user_id) ON DELETE CASCADE,
    group_id INT REFERENCES `Group`(group_id)
);

CREATE TABLE SearchQuery (
    query_id SERIAL PRIMARY KEY,
    keyword VARCHAR(255),
    user_id INT REFERENCES User(user_id) ON DELETE CASCADE,
    location_id INT REFERENCES Location(location_id),
    group_id INT REFERENCES `Group`(group_id),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Transaction (
    transaction_id int PRIMARY KEY NOT NULL,
    listing_id INT REFERENCES Listing(listing_id),
    method VARCHAR(50),
    buyer_id INT REFERENCES User(user_id),
    seller_id INT REFERENCES User(user_id),
    status VARCHAR(50),
    payment VARCHAR(50),
    price DECIMAL(10,2),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Review (
    review_id int PRIMARY KEY NOT NULL,
    reviewer_id INT REFERENCES User(user_id),
    reviewee_id INT REFERENCES User(user_id),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    rating INT
);

CREATE TABLE Verification (
    verification_id int PRIMARY KEY NOT NULL,
    user_id INT REFERENCES User(user_id) ON DELETE CASCADE,
    method VARCHAR(100),
    status VARCHAR(50),
    verified_at TIMESTAMP
);

CREATE TABLE FlaggedContent (
    flag_id int PRIMARY KEY NOT NULL,
    content_type VARCHAR(50),
    content_id INT,
    flagged_by INT REFERENCES User(user_id),
    reason TEXT,
    severity VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Dispute (
    dispute_id int PRIMARY KEY NOT NULL,
    seller_id INT REFERENCES User(user_id),
    buyer_id INT REFERENCES User(user_id),
    listing_id INT REFERENCES Listing(listing_id),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolution TEXT
);

CREATE TABLE UserGroup (
    user_id INT REFERENCES User(user_id) ON DELETE CASCADE,
    group_id INT REFERENCES `Group`(group_id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, group_id)
);

CREATE TABLE ListingPhoto (
    photo_id int PRIMARY KEY NOT NULL,
    listing_id INT REFERENCES Listing(listing_id) ON DELETE CASCADE,
    tag_label VARCHAR(100),
    url TEXT
);

CREATE TABLE ListingTag (
    listing_id INT REFERENCES Listing(listing_id) ON DELETE CASCADE,
    tag_id INT REFERENCES Tag(tag_id) ON DELETE CASCADE,
    PRIMARY KEY (listing_id, tag_id)
);

CREATE TABLE SavedItems (
    user_id INT REFERENCES User(user_id) ON DELETE CASCADE,
    list_id INT REFERENCES Listing(listing_id) ON DELETE CASCADE,
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, list_id)
);

CREATE TABLE CartItem (
    user_id INT REFERENCES User(user_id) ON DELETE CASCADE,
    list_id INT REFERENCES Listing(listing_id) ON DELETE CASCADE,
    quantity INT,
    added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, list_id)
);

CREATE TABLE PriceHistory (
    listing_id INT REFERENCES Listing(listing_id) ON DELETE CASCADE,
    price DECIMAL(10,2),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ListingAnalytics (
    listing_id INT PRIMARY KEY REFERENCES Listing(listing_id) ON DELETE CASCADE,
    views INT DEFAULT 0,
    shares INT DEFAULT 0,
    saves INT DEFAULT 0
);

CREATE TABLE Message (
    message_id int AUTO_INCREMENT PRIMARY KEY,
    sender_id INT REFERENCES User(user_id),
    recipient_id INT REFERENCES User(user_id),
    listing_id INT REFERENCES Listing(listing_id),
    content TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE TrendReport (
    report_id int PRIMARY KEY NOT NULL,
    exported_format VARCHAR(20),
    title VARCHAR(255),
    summary TEXT,
    filters JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INT REFERENCES User(user_id)
);

CREATE TABLE SearchTrend (
    search_trend_id int PRIMARY KEY NOT NULL,
    usage_count INT,
    trend_date DATE,
    location_id INT REFERENCES Location(location_id),
    group_id INT REFERENCES `Group`(group_id),
    keyword VARCHAR(255)
);

CREATE TABLE TagTrend (
    tag_trend_id int PRIMARY KEY NOT NULL,
    usage_count INT,
    trend_date DATE,
    location_id INT REFERENCES Location(location_id),
    group_id INT REFERENCES `Group`(group_id),
    tag_id INT REFERENCES Tag(tag_id)
);

CREATE TABLE UserAnalytics (
    user_id int PRIMARY KEY,
    total_views INT,
    total_saves INT,
    avg_rating FLOAT,

    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

-- EXAMPLE DATA --
INSERT INTO Location VALUES (1, 'North Judithbury', 'DC', '97031', 'Rhodes PLC University');
INSERT INTO Location VALUES (2, 'New Roberttown', 'IL', '30996', 'Guzman, Hoffman and Baldwin University');
INSERT INTO Location VALUES (3, 'Robinsonshire', 'AL', '21427', 'Henderson, Ramirez and Lewis University');
INSERT INTO Location VALUES (4, 'Curtisfurt', 'MI', '45583', 'Baker, Williams and Stevens University');
INSERT INTO Location VALUES (5, 'South Christianport', 'SC', '81571', 'Ray-Bush University');
INSERT INTO Location VALUES (6, 'Lake Jeremyport', 'IN', '13739', 'Ramirez-Reid University');
INSERT INTO Location VALUES (7, 'Franciscostad', 'TN', '35494', 'Zuniga, Wong and Lynch University');
INSERT INTO Location VALUES (8, 'New Jessica', 'NH', '50236', 'Mayo-Bowman University');
INSERT INTO Location VALUES (9, 'Lake Mark', 'WI', '07832', 'Underwood LLC University');
INSERT INTO Location VALUES (10, 'Adamsborough', 'OK', '94599', 'Lewis-Porter University');
INSERT INTO Location VALUES (11, 'New York City', 'NY', '10012', 'New York University');
INSERT INTO Demographic VALUES (1, '18', 'nonbinary', 2);
INSERT INTO Demographic VALUES (2, '25', 'male', 5);
INSERT INTO Demographic VALUES (3, '21', 'nonbinary', 3);
INSERT INTO Demographic VALUES (4, '20', 'nonbinary', 9);
INSERT INTO Demographic VALUES (5, '19', 'male', 7);
INSERT INTO Demographic VALUES (6, '24', 'male', 2);
INSERT INTO Demographic VALUES (7, '18', 'nonbinary', 9);
INSERT INTO Demographic VALUES (8, '35', 'female', 4);
INSERT INTO Demographic VALUES (9, '32', 'nonbinary', 4);
INSERT INTO Demographic VALUES (10, '18', 'male', 5);
INSERT INTO Demographic VALUES (11, '28', 'female', 7);
INSERT INTO Demographic VALUES (12, '24', 'female', 3);
INSERT INTO Demographic VALUES (13, '20', 'female', 2);
INSERT INTO Demographic VALUES (14, '29', 'female', 2);
INSERT INTO Demographic VALUES (15, '26', 'male', 10);
INSERT INTO Demographic VALUES (16, '35', 'male', 8);
INSERT INTO Demographic VALUES (17, '20', 'nonbinary', 7);
INSERT INTO Demographic VALUES (18, '29', 'nonbinary', 5);
INSERT INTO Demographic VALUES (19, '20', 'male', 4);
INSERT INTO Demographic VALUES (20, '27', 'male', 4);
INSERT INTO Demographic VALUES (21, '21', 'female', 4);
INSERT INTO Demographic VALUES (22, '32', 'nonbinary', 5);
INSERT INTO Demographic VALUES (23, '23', 'female', 6);
INSERT INTO Demographic VALUES (24, '24', 'nonbinary', 6);
INSERT INTO Demographic VALUES (25, '20', 'nonbinary', 5);
INSERT INTO Demographic VALUES (26, '35', 'nonbinary', 3);
INSERT INTO Demographic VALUES (27, '23', 'female', 4);
INSERT INTO Demographic VALUES (28, '26', 'nonbinary', 7);
INSERT INTO Demographic VALUES (29, '25', 'nonbinary', 9);
INSERT INTO Demographic VALUES (30, '19', 'male', 6);
INSERT INTO Demographic VALUES (31, '28', 'female', 1);
INSERT INTO Demographic VALUES (32, '20', 'male', 5);
INSERT INTO Demographic VALUES (33, '28', 'male', 10);
INSERT INTO Demographic VALUES (34, '30', 'nonbinary', 8);
INSERT INTO Demographic VALUES (35, '22', 'female', 8);
INSERT INTO Demographic VALUES (36, '25', 'nonbinary', 3);
INSERT INTO Demographic VALUES (37, '35', 'female', 9);
INSERT INTO Demographic VALUES (38, '31', 'nonbinary', 10);
INSERT INTO Demographic VALUES (39, '29', 'male', 7);
INSERT INTO Demographic VALUES (40, '34', 'female', 3);
INSERT INTO User (name, role, location_id, demographic_id) VALUES
('Maria Thomas', 'Buyer', 2, 4),
('Patrick Ryan', 'Admin', 3, 11),
('Jessica Silva', 'Admin', 10, 5),
('Zachary Taylor', 'Admin', 7, 39),
('Peter Callahan Jr.', 'Shopper', 9, 17),
('Michael Carlson', 'Shopper', 1, 8),
('Kyle Mcdonald', 'Buyer', 5, 22),
('Juan Dunlap', 'Seller', 5, 28),
('Ashley Dyer', 'Analyst', 8, 1),
('Patricia Peterson', 'Shopper', 9, 12),
('Christopher Smith', 'Shopper', 2, 20),
('Michelle Stanton', 'Seller', 10, 13),
('Katie Rodriguez', 'Shopper', 6, 11),
('Sarah Romero', 'Shopper', 9, 1),
('James Martin', 'Buyer', 6, 32),
('Tammy Sellers', 'Analyst', 2, 24),
('Katherine Rodriguez', 'Seller', 4, 4),
('William Roman', 'Buyer', 10, 6),
('David Bradley', 'Shopper', 8, 5),
('Nicholas Cabrera', 'Admin', 3, 9),
('Kim Martinez', 'Analyst', 9, 11),
('Theresa Martin', 'Admin', 9, 39),
('Lisa Brandt', 'Seller', 4, 35),
('Nicole Vaughn', 'Analyst', 5, 26),
('Jennifer Powers', 'Admin', 8, 34),
('Steven Hayes', 'Seller', 2, 16),
('Austin Smith', 'Buyer', 2, 22),
('Leah Smith', 'Seller', 10, 36),
('Amy Jones', 'Buyer', 10, 15),
('Gary Palmer', 'Seller', 2, 4),
('John Ryan', 'Analyst', 2, 3),
('Sonya Johnston', 'Seller', 2, 33),
('John Russell', 'Seller', 5, 32),
('Matthew Gomez', 'Shopper', 9, 9),
('Scott Brown', 'Seller', 10, 31),
('Maria Brown', 'Seller', 8, 27),
('Rebecca Rodriguez', 'Admin', 2, 7),
('Joshua Taylor', 'Admin', 6, 28),
('Joel Baxter', 'Buyer', 8, 4),
('Robert Chase', 'Analyst', 1, 26);
INSERT INTO Tag VALUES (1, 'vintage');
INSERT INTO Tag VALUES (2, 'Y2K');
INSERT INTO Tag VALUES (3, 'streetwear');
INSERT INTO Tag VALUES (4, 'minimalist');
INSERT INTO Tag VALUES (5, 'boho');
INSERT INTO Tag VALUES (6, 'designer');
INSERT INTO Tag VALUES (7, 'trendy');
INSERT INTO Tag VALUES (8, 'cottagecore');
INSERT INTO Tag VALUES (9, 'dark academia');
INSERT INTO Tag VALUES (10, 'preppy');
INSERT INTO Tag VALUES (11, 'edgy');
INSERT INTO Tag VALUES (12, 'grunge');
INSERT INTO Tag VALUES (13, 'professional');
INSERT INTO Tag VALUES (14, 'athleisure');
INSERT INTO Tag VALUES (15, 'eco-friendly');
INSERT INTO Tag VALUES (16, 'gender-neutral');
INSERT INTO Tag VALUES (17, '90s');
INSERT INTO Tag VALUES (18, 'coastal');
INSERT INTO Tag VALUES (19, 'mod');
INSERT INTO Tag VALUES (20, 'retro');
INSERT INTO `Group` (group_id, created_by, name, type) VALUES (1, 2, 'closet clearout', 'private');
INSERT INTO `Group` (group_id, created_by, name, type) VALUES (2, 3, 'clean girl', 'public');
INSERT INTO `Group` (group_id, created_by, name, type) VALUES (3, 4, 'streetwear gems', 'invite-only');
INSERT INTO `Group` (group_id, created_by, name, type) VALUES (4, 5, 'designer archive', 'public');
INSERT INTO `Group` (group_id, created_by, name, type) VALUES (5, 1, 'model off-duty', 'public');
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (1, 'Urban Outfitters Mini Skirt', 'Worn a few times but still in excellent condition!', 125.86, 'Fair', 'Urban', 'M', 'Denim', 'Brown', 3, 5);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (2, 'Yeezy Slides', 'Selling because it doesn’t fit me anymore.', 90.62, 'Fair', 'Yeezy', '6', 'Wool', 'Brown', 5, 5);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (3, 'Prada Nylon Shoulder Bag', 'Super comfy and flattering fit.', 132.98, 'New', 'Prada', 'M', 'Denim', 'Brown', 34, 1);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (4, 'Brandy Melville Hoodie', 'Super comfy and flattering fit.', 221.09, 'Good', 'Brandy', 'XL', 'Wool', 'Black', 36, 4);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (5, 'Lululemon Align Pants', 'Perfect for fall/winter layering.', 62.16, 'Good', 'Lululemon', 'L', 'Polyester', 'Beige', 38, 4);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (6, 'North Face Puffer Jacket', 'Minor wear on the sole, otherwise like new.', 193.71, 'Like New', 'North', 'M', 'Cotton', 'Navy', 2, 2);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (7, 'Balenciaga Triple S', 'Perfect for fall/winter layering.', 164.45, 'New', 'Balenciaga', '6', 'Cotton', 'Brown', 25, 3);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (8, 'Vintage Levi’s 501 Jeans', 'Selling because it doesn’t fit me anymore.', 139.51, 'Like New', 'Vintage', '8', 'Polyester', 'Black', 10, 3);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (9, 'Zara Faux Leather Blazer', 'Worn a few times but still in excellent condition!', 231.5, 'Fair', 'Zara', '6', 'Polyester', 'Grey', 6, 5);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (10, 'Vintage Levi’s 501 Jeans', 'Minor wear on the sole, otherwise like new.', 46.38, 'Fair', 'Vintage', 'S', 'Silk', 'Olive', 4, 4);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (11, 'Gucci Marmont Mini Bag', 'Selling because it doesn’t fit me anymore.', 83.54, 'Good', 'Gucci', '8', 'Luon Blend', 'Brown', 21, 3);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (12, 'Aritzia Super Puff', 'Rare colorway. Hard to find!', 69.9, 'Like New', 'Aritzia', 'M', 'Leather', 'Brown', 38, 1);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (13, 'Gucci Marmont Mini Bag', 'Super comfy and flattering fit.', 53.63, 'Fair', 'Gucci', '6', 'Polyester', 'Black', 35, 3);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (14, 'North Face Puffer Jacket', 'Great deal – retails for double!', 87.45, 'Good', 'North', 'S', 'Cotton', 'White', 20, 5);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (15, 'Nike Air Force 1s', 'Selling because it doesn’t fit me anymore.', 211.44, 'Good', 'Nike', 'M', 'Cotton', 'Grey', 16, 3);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (16, 'Brandy Melville Hoodie', 'Minor wear on the sole, otherwise like new.', 26.5, 'Good', 'Brandy', 'XL', 'Leather', 'White', 2, 4);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (17, 'Aritzia Super Puff', 'Minor wear on the sole, otherwise like new.', 190.8, 'Like New', 'Aritzia', 'S', 'Polyester', 'Black', 9, 1);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (18, 'Lululemon Align Pants', 'Worn a few times but still in excellent condition!', 210.14, 'Like New', 'Lululemon', 'M', 'Denim', 'Brown', 26, 3);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (19, 'Zara Faux Leather Blazer', 'Size runs small, fits more like an XS.', 152.74, 'New', 'Zara', 'XS', 'Cotton', 'White', 29, 2);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (20, 'Zara Faux Leather Blazer', 'Perfect for fall/winter layering.', 43.79, 'Fair', 'Zara', 'XS', 'Denim', 'Olive', 28, 4);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (21, 'Ralph Lauren Cable Knit Sweater', 'Worn a few times but still in excellent condition!', 104.94, 'Fair', 'Ralph', 'M', 'Wool', 'White', 12, 3);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (22, 'Thrifted Y2K Tank Top', 'Great deal – retails for double!', 222.6, 'New', 'Thrifted', 'L', 'Luon Blend', 'Beige', 32, 4);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (23, 'Balenciaga Triple S', 'Great deal – retails for double!', 29.33, 'Good', 'Balenciaga', '8', 'Denim', 'Navy', 13, 5);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (24, 'Urban Outfitters Mini Skirt', 'DM for more pics or to bundle with other items!', 248.61, 'New', 'Urban', '8', 'Leather', 'Grey', 23, 4);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (25, 'Balenciaga Triple S', 'Great deal – retails for double!', 95.85, 'Good', 'Balenciaga', '8', 'Wool', 'White', 2, 3);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (26, 'Birkenstock Boston Clogs', 'Selling because it doesn’t fit me anymore.', 21.89, 'Good', 'Birkenstock', 'XS', 'Leather', 'Navy', 34, 3);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (27, 'Shein Corset Top', 'Selling because it doesn’t fit me anymore.', 243.89, 'New', 'Shein', 'L', 'Luon Blend', 'White', 18, 5);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (28, 'Nike Air Force 1s', 'Selling because it doesn’t fit me anymore.', 150.29, 'Fair', 'Nike', '6', 'Leather', 'Brown', 12, 2);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (29, 'Urban Outfitters Mini Skirt', 'Size runs small, fits more like an XS.', 89.73, 'Good', 'Urban', 'XS', 'Luon Blend', 'Grey', 23, 5);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (30, 'Shein Corset Top', 'No flaws. Just cleaning out my closet!', 147.33, 'Like New', 'Shein', '10', 'Silk', 'Beige', 12, 4);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (31, 'Nike Air Force 1s', 'Super comfy and flattering fit.', 28.2, 'Like New', 'Nike', 'XS', 'Silk', 'Navy', 1, 3);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (32, 'Birkenstock Boston Clogs', 'Selling because it doesn’t fit me anymore.', 204.51, 'Good', 'Birkenstock', 'M', 'Leather', 'Brown', 21, 1);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (33, 'Lululemon Align Pants', 'No flaws. Just cleaning out my closet!', 152.85, 'Like New', 'Lululemon', 'S', 'Leather', 'Olive', 24, 1);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (34, 'Prada Nylon Shoulder Bag', 'DM for more pics or to bundle with other items!', 107.96, 'New', 'Prada', '6', 'Wool', 'Beige', 9, 2);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (35, 'Yeezy Slides', 'DM for more pics or to bundle with other items!', 240.76, 'Good', 'Yeezy', 'M', 'Luon Blend', 'Olive', 40, 3);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (36, 'Urban Outfitters Mini Skirt', 'DM for more pics or to bundle with other items!', 153.4, 'Like New', 'Urban', '8', 'Wool', 'Grey', 19, 2);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (37, 'Adidas Campus 00s', 'Worn a few times but still in excellent condition!', 237.97, 'Fair', 'Adidas', 'XS', 'Denim', 'Olive', 21, 5);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (38, 'Urban Outfitters Mini Skirt', 'DM for more pics or to bundle with other items!', 147.9, 'Fair', 'Urban', 'M', 'Wool', 'Grey', 5, 2);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (39, 'Prada Nylon Shoulder Bag', 'Perfect for fall/winter layering.', 54.45, 'New', 'Prada', '6', 'Polyester', 'Black', 17, 2);
INSERT INTO Listing (listing_id, title, description, price, `condition`, brand, size, material, color, seller_id, group_id) VALUES (40, 'Urban Outfitters Mini Skirt', 'Super comfy and flattering fit.', 97.36, 'New', 'Urban', 'XS', 'Cotton', 'Navy', 29, 4);
INSERT INTO SavedItems VALUES (15, 19, '2025-01-16 18:21:39');
INSERT INTO SavedItems VALUES (19, 30, '2025-01-31 11:56:20');
INSERT INTO SavedItems VALUES (5, 15, '2025-02-16 13:51:09');
INSERT INTO SavedItems VALUES (17, 38, '2025-02-03 18:01:47');
INSERT INTO SavedItems VALUES (13, 28, '2025-01-15 13:49:39');
INSERT INTO SavedItems VALUES (8, 35, '2025-01-31 09:29:41');
INSERT INTO SavedItems VALUES (15, 10, '2025-01-01 12:28:11');
INSERT INTO SavedItems VALUES (18, 10, '2025-03-21 07:49:47');
INSERT INTO SavedItems VALUES (5, 4, '2025-03-29 11:29:57');
INSERT INTO SavedItems VALUES (11, 20, '2025-04-02 05:57:03');
INSERT INTO SavedItems VALUES (39, 37, '2025-02-26 13:22:00');
INSERT INTO SavedItems VALUES (19, 29, '2025-01-07 08:06:45');
INSERT INTO SavedItems VALUES (8, 30, '2025-02-14 22:45:26');
INSERT INTO SavedItems VALUES (20, 26, '2025-02-25 22:39:57');
INSERT INTO SavedItems VALUES (18, 33, '2025-02-24 21:33:47');
INSERT INTO SavedItems VALUES (35, 32, '2025-03-30 03:56:21');
INSERT INTO SavedItems VALUES (29, 6, '2025-01-14 19:43:18');
INSERT INTO SavedItems VALUES (39, 3, '2025-02-15 07:50:01');
INSERT INTO SavedItems VALUES (28, 21, '2025-02-21 08:54:50');
INSERT INTO SavedItems VALUES (39, 17, '2025-02-08 09:54:15');
INSERT INTO SavedItems VALUES (2, 6, '2025-03-24 13:17:28');
INSERT INTO SavedItems VALUES (15, 37, '2025-01-23 06:53:46');
INSERT INTO SavedItems VALUES (38, 2, '2025-02-13 15:41:16');
INSERT INTO SavedItems VALUES (18, 37, '2025-01-29 22:20:27');
INSERT INTO SavedItems VALUES (3, 12, '2025-02-21 13:56:13');
INSERT INTO SavedItems VALUES (31, 34, '2025-01-28 14:52:08');
INSERT INTO SavedItems VALUES (29, 18, '2025-01-14 20:47:38');
INSERT INTO SavedItems VALUES (12, 38, '2025-01-12 13:56:00');
INSERT INTO SavedItems VALUES (28, 32, '2025-02-02 05:15:22');
INSERT INTO SavedItems VALUES (6, 31, '2025-03-01 17:34:29');
INSERT INTO SavedItems VALUES (23, 27, '2025-02-26 01:01:22');
INSERT INTO SavedItems VALUES (22, 21, '2025-03-27 06:36:12');
INSERT INTO SavedItems VALUES (7, 11, '2025-01-25 03:31:48');
INSERT INTO SavedItems VALUES (22, 27, '2025-04-02 00:17:27');
INSERT INTO SavedItems VALUES (32, 19, '2025-03-01 01:10:03');
INSERT INTO SavedItems VALUES (26, 36, '2025-03-20 03:49:32');
INSERT INTO SavedItems VALUES (3, 30, '2025-02-22 20:45:33');
INSERT INTO SavedItems VALUES (6, 21, '2025-04-08 04:22:09');
INSERT INTO SavedItems VALUES (17, 21, '2025-04-06 21:15:09');
INSERT INTO SavedItems VALUES (8, 26, '2025-03-27 00:06:15');
INSERT INTO SavedItems VALUES (33, 1, '2025-01-16 14:53:10');
INSERT INTO SavedItems VALUES (35, 30, '2025-01-08 17:45:52');
INSERT INTO Transaction VALUES (1, 21, 'Drop-off', 28, 21, 'Pending', 'Cash', 191.18, '2025-03-13 03:12:51');
INSERT INTO Transaction VALUES (2, 31, 'Pickup', 5, 6, 'Completed', 'Cash', 28.35, '2025-03-12 07:44:38');
INSERT INTO Transaction VALUES (3, 24, 'Pickup', 9, 36, 'Canceled', 'PayPal', 116.72, '2025-03-16 08:13:50');
INSERT INTO Transaction VALUES (4, 8, 'Drop-off', 27, 23, 'Pending', 'PayPal', 19.77, '2025-01-07 06:55:35');
INSERT INTO Transaction VALUES (5, 19, 'Shipping', 39, 20, 'Completed', 'PayPal', 106.41, '2025-01-30 19:04:25');
INSERT INTO Transaction VALUES (6, 10, 'Pickup', 31, 15, 'Pending', 'PayPal', 79.84, '2025-03-29 08:47:28');
INSERT INTO Transaction VALUES (7, 18, 'Shipping', 37, 15, 'Canceled', 'PayPal', 126.58, '2025-03-14 00:49:11');
INSERT INTO Transaction VALUES (8, 36, 'Drop-off', 2, 39, 'Canceled', 'Cash', 15.5, '2025-03-14 05:42:28');
INSERT INTO Transaction VALUES (9, 18, 'Shipping', 20, 22, 'Completed', 'Venmo', 175.27, '2025-03-28 04:54:25');
INSERT INTO Transaction VALUES (10, 37, 'Pickup', 26, 5, 'Canceled', 'PayPal', 194.64, '2025-01-15 22:18:43');
INSERT INTO Transaction VALUES (11, 6, 'Shipping', 34, 14, 'Pending', 'Cash', 74.77, '2025-01-27 17:42:20');
INSERT INTO Transaction VALUES (12, 24, 'Drop-off', 20, 21, 'Canceled', 'Venmo', 177.84, '2025-03-13 06:06:38');
INSERT INTO Transaction VALUES (13, 10, 'Pickup', 11, 40, 'Canceled', 'Venmo', 61.7, '2025-03-19 06:58:23');
INSERT INTO Transaction VALUES (14, 28, 'Shipping', 32, 39, 'Pending', 'Cash', 50.96, '2025-03-03 01:08:32');
INSERT INTO Transaction VALUES (15, 33, 'Shipping', 8, 23, 'Completed', 'Cash', 138.86, '2025-02-24 02:47:18');
INSERT INTO Transaction VALUES (16, 38, 'Drop-off', 32, 34, 'Pending', 'Venmo', 51.9, '2025-02-18 11:16:28');
INSERT INTO Transaction VALUES (17, 39, 'Pickup', 4, 1, 'Pending', 'Venmo', 155.8, '2025-01-23 00:42:31');
INSERT INTO Transaction VALUES (18, 17, 'Pickup', 19, 21, 'Completed', 'Cash', 151.93, '2025-01-06 00:45:53');
INSERT INTO Transaction VALUES (19, 12, 'Drop-off', 9, 25, 'Canceled', 'Venmo', 105.05, '2025-02-06 03:02:48');
INSERT INTO Transaction VALUES (20, 23, 'Drop-off', 5, 26, 'Completed', 'Cash', 13.56, '2025-04-07 21:42:48');
INSERT INTO Transaction VALUES (21, 5, 'Shipping', 21, 37, 'Canceled', 'Cash', 144.8, '2025-04-11 12:52:04');
INSERT INTO Transaction VALUES (22, 27, 'Shipping', 19, 8, 'Completed', 'Cash', 42.66, '2025-03-17 03:29:30');
INSERT INTO Transaction VALUES (23, 40, 'Pickup', 30, 24, 'Pending', 'Venmo', 56.23, '2025-01-23 20:48:21');
INSERT INTO Transaction VALUES (24, 38, 'Pickup', 26, 34, 'Pending', 'Cash', 151.7, '2025-02-20 19:58:03');
INSERT INTO Transaction VALUES (25, 15, 'Pickup', 22, 11, 'Canceled', 'PayPal', 31.67, '2025-02-20 13:02:17');
INSERT INTO Transaction VALUES (26, 33, 'Shipping', 13, 23, 'Canceled', 'PayPal', 164.86, '2025-03-28 15:47:00');
INSERT INTO Transaction VALUES (27, 16, 'Shipping', 7, 10, 'Completed', 'Venmo', 124.46, '2025-02-11 15:58:14');
INSERT INTO Transaction VALUES (28, 5, 'Shipping', 12, 32, 'Canceled', 'PayPal', 95.29, '2025-02-25 10:53:04');
INSERT INTO Transaction VALUES (29, 37, 'Drop-off', 40, 21, 'Pending', 'Venmo', 93.55, '2025-04-06 09:09:31');
INSERT INTO Transaction VALUES (30, 31, 'Shipping', 29, 20, 'Canceled', 'Venmo', 76.87, '2025-02-08 20:53:55');
INSERT INTO Transaction VALUES (31, 5, 'Shipping', 20, 30, 'Completed', 'Venmo', 80.06, '2025-01-24 19:31:54');
INSERT INTO Transaction VALUES (32, 19, 'Drop-off', 5, 6, 'Canceled', 'PayPal', 83.05, '2025-01-27 08:32:24');
INSERT INTO Transaction VALUES (33, 38, 'Shipping', 36, 3, 'Canceled', 'PayPal', 45.77, '2025-01-15 09:06:27');
INSERT INTO Transaction VALUES (34, 39, 'Pickup', 31, 33, 'Completed', 'Cash', 29.67, '2025-03-29 18:40:17');
INSERT INTO Transaction VALUES (35, 22, 'Drop-off', 6, 33, 'Completed', 'Venmo', 57.07, '2025-02-03 12:38:13');
INSERT INTO Transaction VALUES (36, 29, 'Drop-off', 29, 34, 'Canceled', 'Venmo', 79.14, '2025-03-28 10:22:06');
INSERT INTO Transaction VALUES (37, 19, 'Shipping', 25, 27, 'Canceled', 'PayPal', 19.95, '2025-01-18 01:08:04');
INSERT INTO Transaction VALUES (38, 22, 'Pickup', 5, 22, 'Canceled', 'PayPal', 83.45, '2025-03-04 01:23:13');
INSERT INTO Transaction VALUES (39, 17, 'Shipping', 39, 10, 'Completed', 'PayPal', 136.09, '2025-03-09 11:07:09');
INSERT INTO Transaction VALUES (40, 23, 'Pickup', 20, 26, 'Canceled', 'PayPal', 188.22, '2025-01-13 14:38:16');
INSERT INTO Transaction VALUES (41, 20, 'Drop-off', 36, 25, 'Pending', 'Venmo', 137.32, '2025-02-26 09:11:10');
INSERT INTO Transaction VALUES (42, 34, 'Drop-off', 6, 28, 'Pending', 'Venmo', 78.89, '2025-02-28 05:53:57');
INSERT INTO Transaction VALUES (43, 12, 'Shipping', 14, 22, 'Completed', 'Venmo', 200.0, '2025-01-31 14:01:39');
INSERT INTO Transaction VALUES (44, 10, 'Pickup', 5, 19, 'Canceled', 'PayPal', 168.67, '2025-02-03 19:19:22');
INSERT INTO Transaction VALUES (45, 34, 'Drop-off', 3, 22, 'Completed', 'PayPal', 81.58, '2025-03-12 04:40:32');
INSERT INTO Transaction VALUES (46, 11, 'Pickup', 12, 40, 'Canceled', 'Cash', 18.3, '2025-04-09 18:58:25');
INSERT INTO Transaction VALUES (47, 24, 'Drop-off', 16, 29, 'Pending', 'PayPal', 158.92, '2025-02-13 13:02:30');
INSERT INTO Transaction VALUES (48, 15, 'Shipping', 35, 16, 'Pending', 'Venmo', 79.89, '2025-01-24 13:35:24');
INSERT INTO Transaction VALUES (49, 37, 'Shipping', 29, 30, 'Pending', 'PayPal', 110.22, '2025-02-09 00:38:11');
INSERT INTO Transaction VALUES (50, 11, 'Pickup', 13, 39, 'Pending', 'Venmo', 131.82, '2025-01-27 23:12:47');
INSERT INTO Transaction VALUES (51, 24, 'Drop-off', 36, 7, 'Canceled', 'Venmo', 64.16, '2025-02-15 23:16:14');
INSERT INTO Transaction VALUES (52, 11, 'Drop-off', 18, 29, 'Completed', 'Cash', 27.43, '2025-04-06 22:18:32');
INSERT INTO Transaction VALUES (53, 15, 'Pickup', 29, 23, 'Pending', 'Venmo', 85.33, '2025-01-06 02:29:32');
INSERT INTO Transaction VALUES (54, 24, 'Pickup', 16, 25, 'Pending', 'Venmo', 15.36, '2025-03-12 01:53:58');
INSERT INTO Transaction VALUES (55, 7, 'Pickup', 22, 10, 'Completed', 'Cash', 184.31, '2025-03-13 15:15:02');
INSERT INTO Transaction VALUES (56, 31, 'Shipping', 9, 31, 'Canceled', 'Venmo', 182.11, '2025-04-01 18:16:08');
INSERT INTO Transaction VALUES (57, 2, 'Pickup', 17, 14, 'Canceled', 'PayPal', 125.69, '2025-01-26 04:46:39');
INSERT INTO Transaction VALUES (58, 28, 'Pickup', 8, 19, 'Pending', 'Venmo', 19.07, '2025-01-17 17:47:35');
INSERT INTO Transaction VALUES (59, 27, 'Pickup', 40, 30, 'Completed', 'Cash', 123.38, '2025-01-13 18:24:30');
INSERT INTO Transaction VALUES (60, 2, 'Pickup', 33, 37, 'Canceled', 'Venmo', 65.34, '2025-03-02 01:23:57');
INSERT INTO Transaction VALUES (61, 1, 'Pickup', 40, 23, 'Canceled', 'Cash', 45.59, '2025-03-19 07:33:35');
INSERT INTO Transaction VALUES (62, 6, 'Pickup', 34, 24, 'Canceled', 'PayPal', 106.39, '2025-04-03 22:44:27');
INSERT INTO Transaction VALUES (63, 33, 'Shipping', 36, 2, 'Pending', 'Venmo', 130.78, '2025-03-21 18:26:38');
INSERT INTO Transaction VALUES (64, 24, 'Shipping', 17, 2, 'Completed', 'Cash', 55.81, '2025-03-21 12:05:54');
INSERT INTO Transaction VALUES (65, 7, 'Pickup', 38, 22, 'Completed', 'Cash', 113.74, '2025-01-15 07:42:11');
INSERT INTO Transaction VALUES (66, 12, 'Drop-off', 30, 31, 'Completed', 'Venmo', 21.99, '2025-01-25 08:03:54');
INSERT INTO Transaction VALUES (67, 30, 'Pickup', 3, 19, 'Completed', 'Venmo', 178.3, '2025-03-03 13:27:21');
INSERT INTO Transaction VALUES (68, 21, 'Shipping', 20, 33, 'Canceled', 'Cash', 58.13, '2025-01-15 09:38:02');
INSERT INTO Transaction VALUES (69, 13, 'Pickup', 19, 23, 'Canceled', 'Cash', 61.91, '2025-03-29 09:01:59');
INSERT INTO Transaction VALUES (70, 24, 'Drop-off', 28, 26, 'Pending', 'Cash', 74.42, '2025-04-01 10:56:24');
INSERT INTO Transaction VALUES (71, 12, 'Drop-off', 24, 32, 'Pending', 'Venmo', 148.15, '2025-04-11 11:04:20');
INSERT INTO Transaction VALUES (72, 6, 'Pickup', 28, 39, 'Canceled', 'Cash', 71.03, '2025-03-08 21:33:18');
INSERT INTO Transaction VALUES (73, 6, 'Shipping', 21, 19, 'Pending', 'PayPal', 146.36, '2025-01-25 22:04:57');
INSERT INTO Transaction VALUES (74, 11, 'Shipping', 29, 23, 'Completed', 'PayPal', 175.31, '2025-02-05 08:00:34');
INSERT INTO Transaction VALUES (75, 23, 'Shipping', 40, 28, 'Canceled', 'Venmo', 24.26, '2025-01-26 01:20:13');
INSERT INTO CartItem VALUES
(10, 7, 1, '2025-03-25 21:53:33'),
(19, 25, 3, '2025-03-18 19:32:51'),
(27, 16, 1, '2025-01-06 16:02:45'),
(21, 37, 3, '2025-02-08 07:35:54'),
(21, 13, 1, '2025-03-29 07:10:17'),
(32, 33, 2, '2025-03-25 09:51:40'),
(32, 20, 2, '2025-03-17 12:06:21'),
(2, 6, 2, '2025-01-01 20:44:19'),
(33, 30, 1, '2025-02-11 17:01:20'),
(14, 38, 2, '2025-02-09 23:01:30'),
(4, 4, 2, '2025-02-24 01:10:51'),
(32, 39, 3, '2025-01-13 03:34:05'),
(31, 19, 3, '2025-01-20 18:11:56'),
(1, 7, 2, '2025-02-06 07:17:45'),
(9, 17, 3, '2025-03-13 00:43:08'),
(24, 26, 2, '2025-03-05 07:11:59'),
(3, 26, 1, '2025-02-08 06:25:57'),
(37, 36, 1, '2025-03-30 20:20:22'),
(24, 36, 2, '2025-01-23 03:04:07'),
(5, 25, 3, '2025-02-20 22:39:19'),
(29, 36, 2, '2025-04-06 01:09:38'),
(40, 40, 1, '2025-03-02 20:34:08'),
(9, 7, 2, '2025-03-17 11:11:24'),
(24, 22, 3, '2025-03-18 05:23:15'),
(24, 10, 1, '2025-01-23 04:21:36'),
(39, 33, 2, '2025-03-09 13:26:46'),
(33, 3, 1, '2025-03-10 08:22:07'),
(3, 9, 3, '2025-03-30 21:47:05'),
(22, 31, 3, '2025-02-03 12:02:11'),
(30, 10, 3, '2025-02-27 18:11:36'),
(33, 9, 2, '2025-01-17 10:58:22'),
(40, 21, 1, '2025-01-27 00:14:30'),
(26, 40, 3, '2025-03-02 19:33:04'),
(20, 38, 2, '2025-01-23 21:16:30'),
(33, 33, 3, '2025-02-16 07:49:46'),
(32, 37, 2, '2025-03-01 07:10:26'),
(31, 2, 2, '2025-01-23 17:01:17'),
(22, 8, 2, '2025-02-05 13:02:57'),
(38, 20, 3, '2025-03-14 11:43:56'),
(2, 39, 2, '2025-01-28 10:46:42'),
(17, 38, 3, '2025-04-10 04:36:59'),
(15, 4, 3, '2025-03-17 10:22:12'),
(31, 11, 3, '2025-03-23 05:08:07');
INSERT INTO UserGroup VALUES (2, 3);
INSERT INTO UserGroup VALUES (30, 5);
INSERT INTO UserGroup VALUES (28, 5);
INSERT INTO UserGroup VALUES (25, 2);
INSERT INTO UserGroup VALUES (16, 4);
INSERT INTO UserGroup VALUES (23, 2);
INSERT INTO UserGroup VALUES (18, 2);
INSERT INTO UserGroup VALUES (8, 1);
INSERT INTO UserGroup VALUES (27, 5);
INSERT INTO UserGroup VALUES (2, 2);
INSERT INTO UserGroup VALUES (14, 1);
INSERT INTO UserGroup VALUES (7, 5);
INSERT INTO UserGroup VALUES (3, 4);
INSERT INTO UserGroup VALUES (39, 1);
INSERT INTO UserGroup VALUES (16, 1);
INSERT INTO UserGroup VALUES (26, 4);
INSERT INTO UserGroup VALUES (15, 5);
INSERT INTO UserGroup VALUES (9, 5);
INSERT INTO UserGroup VALUES (19, 2);
INSERT INTO UserGroup VALUES (37, 3);
INSERT INTO UserGroup VALUES (37, 5);
INSERT INTO UserGroup VALUES (21, 2);
INSERT INTO UserGroup VALUES (20, 2);
INSERT INTO UserGroup VALUES (34, 2);
INSERT INTO UserGroup VALUES (18, 1);
INSERT INTO UserGroup VALUES (36, 5);
INSERT INTO UserGroup VALUES (12, 4);
INSERT INTO UserGroup VALUES (36, 4);
INSERT INTO UserGroup VALUES (4, 3);
INSERT INTO UserGroup VALUES (25, 5);
INSERT INTO UserGroup VALUES (21, 4);
INSERT INTO UserGroup VALUES (27, 2);
INSERT INTO UserGroup VALUES (20, 4);
INSERT INTO UserGroup VALUES (12, 5);
INSERT INTO UserGroup VALUES (31, 2);
INSERT INTO UserGroup VALUES (15, 3);
INSERT INTO UserGroup VALUES (10, 4);
INSERT INTO UserGroup VALUES (4, 5);
INSERT INTO UserGroup VALUES (27, 4);
INSERT INTO UserGroup VALUES (9, 4);
INSERT INTO UserGroup VALUES (16, 3);
INSERT INTO UserGroup VALUES (14, 3);
INSERT INTO UserGroup VALUES (6, 4);
INSERT INTO UserGroup VALUES (24, 1);
INSERT INTO UserGroup VALUES (35, 2);
INSERT INTO UserGroup VALUES (5, 2);
INSERT INTO UserGroup VALUES (38, 5);
INSERT INTO UserGroup VALUES (14, 4);
INSERT INTO UserGroup VALUES (20, 1);
INSERT INTO UserGroup VALUES (14, 2);
INSERT INTO UserGroup VALUES (8, 4);
INSERT INTO UserGroup VALUES (16, 5);
INSERT INTO UserGroup VALUES (21, 3);
INSERT INTO UserGroup VALUES (25, 4);
INSERT INTO UserGroup VALUES (35, 3);
INSERT INTO UserGroup VALUES (20, 3);
INSERT INTO UserGroup VALUES (24, 5);
INSERT INTO UserGroup VALUES (32, 4);
INSERT INTO UserGroup VALUES (7, 4);
INSERT INTO UserGroup VALUES (24, 3);
INSERT INTO UserGroup VALUES (27, 1);
INSERT INTO UserGroup VALUES (37, 2);
INSERT INTO UserGroup VALUES (10, 1);
INSERT INTO UserGroup VALUES (17, 5);
INSERT INTO UserGroup VALUES (10, 2);
INSERT INTO UserGroup VALUES (22, 2);
INSERT INTO UserGroup VALUES (36, 3);
INSERT INTO UserGroup VALUES (17, 4);
INSERT INTO UserGroup VALUES (11, 3);
INSERT INTO UserGroup VALUES (11, 2);
INSERT INTO UserGroup VALUES (35, 4);
INSERT INTO UserGroup VALUES (3, 1);
INSERT INTO UserGroup VALUES (4, 1);
INSERT INTO UserGroup VALUES (15, 1);
INSERT INTO UserGroup VALUES (14, 5);
INSERT INTO UserGroup VALUES (30, 3);
INSERT INTO UserGroup VALUES (40, 4);
INSERT INTO UserGroup VALUES (32, 1);
INSERT INTO UserGroup VALUES (1, 5);
INSERT INTO UserGroup VALUES (1, 1);
INSERT INTO UserGroup VALUES (34, 3);
INSERT INTO UserGroup VALUES (2, 5);
INSERT INTO UserGroup VALUES (28, 2);
INSERT INTO UserGroup VALUES (7, 1);
INSERT INTO UserGroup VALUES (16, 2);
INSERT INTO UserGroup VALUES (40, 5);
INSERT INTO UserGroup VALUES (17, 3);
INSERT INTO UserGroup VALUES (18, 4);
INSERT INTO Message (sender_id, recipient_id, listing_id, content, timestamp) VALUES
(27, 35, 3, 'Any flexibility on price?', '2025-03-13 12:38:39'),
(24, 35, 39, 'Hey! Just messaged you about the listing :)', '2025-04-01 03:24:53'),
(6, 7, 16, 'Hey! Just messaged you about the listing :)', '2025-04-09 02:03:34'),
(23, 11, 40, 'Hi! Is this still available?', '2025-03-19 01:53:06'),
(37, 26, 22, 'Any flexibility on price?', '2025-01-25 01:17:21'),
(28, 7, 1, 'Can you hold this for me until tomorrow?', '2025-01-06 22:26:05'),
(17, 15, 33, 'I''m nearby and can pick up today!', '2025-02-16 23:30:47'),
(34, 36, 38, 'I''m nearby and can pick up today!', '2025-03-14 07:49:15'),
(37, 15, 29, 'I''m interested! Is it true to size?', '2025-04-05 21:54:40'),
(26, 30, 38, 'I''m nearby and can pick up today!', '2025-03-28 14:59:33'),
(33, 10, 23, 'Hi! Is this still available?', '2025-02-04 11:35:59'),
(31, 7, 19, 'Can I see more photos?', '2025-04-03 03:42:49'),
(6, 8, 10, 'I''m interested! Is it true to size?', '2025-03-09 21:59:57'),
(20, 22, 30, 'Any flexibility on price?', '2025-03-08 20:18:59'),
(14, 34, 31, 'I''m interested! Is it true to size?', '2025-02-01 18:01:43'),
(31, 7, 29, 'I''m nearby and can pick up today!', '2025-02-20 05:26:33'),
(29, 21, 5, 'Can you ship this item?', '2025-01-18 13:15:24'),
(3, 8, 2, 'Are there any flaws or damages?', '2025-02-25 08:31:10'),
(22, 7, 11, 'I love this — would you do a bundle deal?', '2025-01-06 07:55:42'),
(16, 34, 12, 'When was this originally purchased?', '2025-03-17 01:31:35'),
(11, 22, 36, 'Can I see more photos?', '2025-01-10 15:23:26'),
(30, 15, 26, 'Hey! Just messaged you about the listing :)', '2025-02-01 15:12:12'),
(12, 28, 26, 'Hi! Is this still available?', '2025-02-11 14:47:49'),
(40, 13, 29, 'Is this from a smoke-free home?', '2025-02-12 23:34:14'),
(28, 25, 1, 'I''m nearby and can pick up today!', '2025-02-13 17:05:53'),
(14, 18, 5, 'Is this from a smoke-free home?', '2025-02-10 03:26:10'),
(7, 35, 12, 'I''m interested! Is it true to size?', '2025-02-22 06:01:13'),
(21, 13, 30, 'Can you hold this for me until tomorrow?', '2025-03-21 12:26:30'),
(17, 32, 34, 'Hey! Just messaged you about the listing :)', '2025-04-10 16:03:50'),
(21, 39, 25, 'Is this from a smoke-free home?', '2025-01-04 21:27:02'),
(26, 38, 8, 'I''m interested! Is it true to size?', '2025-01-02 17:28:03'),
(23, 30, 40, 'Would you accept a lower price?', '2025-04-03 01:27:11'),
(20, 40, 38, 'Can you hold this for me until tomorrow?', '2025-01-26 16:37:42'),
(9, 21, 8, 'Where are you located for pickup?', '2025-02-03 15:10:24'),
(20, 8, 12, 'I''m interested! Is it true to size?', '2025-01-02 15:26:37'),
(10, 33, 25, 'Can I see more photos?', '2025-02-13 10:50:38'),
(39, 9, 37, 'Can I see more photos?', '2025-02-19 00:13:28'),
(28, 12, 32, 'Hey! Just messaged you about the listing :)', '2025-03-01 07:32:43'),
(35, 12, 36, 'Would you accept a lower price?', '2025-02-23 11:21:25'),
(32, 19, 9, 'Would you accept a lower price?', '2025-03-24 07:04:58'),
(21, 29, 40, 'Hi! Is this still available?', '2025-03-15 02:30:09'),
(23, 1, 32, 'Would you accept a lower price?', '2025-03-09 17:06:09'),
(13, 25, 36, 'When was this originally purchased?', '2025-03-31 03:05:08'),
(32, 27, 32, 'Can I see more photos?', '2025-02-18 22:23:56'),
(29, 32, 11, 'Can you hold this for me until tomorrow?', '2025-02-12 08:55:40'),
(37, 2, 15, 'Can you ship this item?', '2025-04-01 14:58:13'),
(3, 18, 15, 'When was this originally purchased?', '2025-02-28 16:05:53'),
(19, 11, 30, 'Is this from a smoke-free home?', '2025-03-19 02:51:53'),
(32, 36, 33, 'Can you hold this for me until tomorrow?', '2025-01-20 20:48:32'),
(37, 8, 18, 'Any flexibility on price?', '2025-01-02 10:14:31'),
(35, 24, 35, 'Are there any flaws or damages?', '2025-04-10 07:49:36'),
(3, 29, 35, 'Where are you located for pickup?', '2025-03-14 16:02:13'),
(28, 7, 16, 'Can you ship this item?', '2025-02-24 21:22:11'),
(3, 29, 17, 'I''m interested! Is it true to size?', '2025-02-27 22:59:55'),
(6, 29, 8, 'Any flexibility on price?', '2025-01-21 23:48:13'),
(16, 14, 38, 'I''m nearby and can pick up today!', '2025-04-04 13:03:49'),
(23, 40, 28, 'Would you accept a lower price?', '2025-01-13 09:30:08'),
(40, 9, 14, 'Are there any flaws or damages?', '2025-03-07 07:11:43'),
(14, 4, 37, 'I''m interested! Is it true to size?', '2025-02-23 16:30:19'),
(35, 18, 39, 'When was this originally purchased?', '2025-03-05 03:14:54');
INSERT INTO Review VALUES (1, 11, 21, 'Not as described but refunded me.', '2025-02-23 18:22:38', 3);
INSERT INTO Review VALUES (2, 19, 37, 'Super friendly and easy to work with!', '2025-02-20 17:01:58', 5);
INSERT INTO Review VALUES (3, 7, 9, 'Exactly what I needed — 10/10.', '2025-02-28 00:28:03', 4);
INSERT INTO Review VALUES (4, 4, 18, 'Bundle deal was appreciated!', '2025-02-06 13:49:17', 2);
INSERT INTO Review VALUES (5, 9, 16, 'Rude but responsive buyer.', '2025-01-30 02:43:16', 3);
INSERT INTO Review VALUES (6, 16, 26, 'Flaked on meetup :(', '2025-04-11 10:45:46', 2);
INSERT INTO Review VALUES (7, 37, 18, 'Honest seller, would buy again.', '2025-02-16 15:53:19', 4);
INSERT INTO Review VALUES (8, 25, 29, 'Item arrived as described.', '2025-01-12 00:35:20', 1);
INSERT INTO Review VALUES (9, 26, 33, 'Not as described but refunded me.', '2025-03-20 11:14:06', 3);
INSERT INTO Review VALUES (10, 24, 30, 'Flaked on meetup :(', '2025-03-04 01:22:38', 3);
INSERT INTO Review VALUES (11, 38, 1, 'Bundle deal was appreciated!', '2025-01-28 04:07:07', 1);
INSERT INTO Review VALUES (12, 30, 23, 'Bundle deal was appreciated!', '2025-01-05 22:37:48', 1);
INSERT INTO Review VALUES (13, 35, 26, 'Wouldn’t recommend — item was dirty.', '2025-04-07 13:55:31', 4);
INSERT INTO Review VALUES (14, 14, 32, 'Super friendly and easy to work with!', '2025-02-27 09:37:02', 3);
INSERT INTO Review VALUES (15, 19, 22, 'Very professional, thank you!', '2025-02-20 09:00:50', 5);
INSERT INTO Review VALUES (16, 9, 37, 'Bundle deal was appreciated!', '2025-03-23 06:39:26', 4);
INSERT INTO Review VALUES (17, 22, 4, 'Great seller, fast shipping!', '2025-03-20 13:34:03', 1);
INSERT INTO Review VALUES (18, 30, 2, 'Item arrived as described.', '2025-03-17 09:29:32', 2);
INSERT INTO Review VALUES (19, 29, 30, 'Great seller, fast shipping!', '2025-01-07 20:35:54', 4);
INSERT INTO Review VALUES (20, 13, 9, 'Great communication and quick pickup.', '2025-02-06 21:04:07', 3);
INSERT INTO Review VALUES (21, 11, 18, 'Item arrived as described.', '2025-03-08 15:16:27', 3);
INSERT INTO Review VALUES (22, 17, 6, 'Took a while to respond but item was fine.', '2025-02-13 04:17:15', 2);
INSERT INTO Review VALUES (23, 4, 26, 'Honest seller, would buy again.', '2025-04-03 09:05:12', 3);
INSERT INTO Review VALUES (24, 15, 28, 'Honest seller, would buy again.', '2025-03-11 14:43:03', 1);
INSERT INTO Review VALUES (25, 7, 1, 'Wouldn’t recommend — item was dirty.', '2025-04-09 12:15:30', 4);
INSERT INTO Review VALUES (26, 5, 9, 'Cute item, slightly overpriced though.', '2025-02-28 07:00:33', 2);
INSERT INTO Review VALUES (27, 34, 29, 'Great seller, fast shipping!', '2025-02-03 00:11:42', 1);
INSERT INTO Review VALUES (28, 22, 8, 'Bundle deal was appreciated!', '2025-02-05 04:09:15', 4);
INSERT INTO Review VALUES (29, 9, 31, 'Item arrived as described.', '2025-02-27 01:07:58', 2);
INSERT INTO Review VALUES (30, 25, 6, 'Not as described but refunded me.', '2025-01-19 22:51:47', 1);
INSERT INTO Review VALUES (31, 7, 21, 'Took a while to respond but item was fine.', '2025-04-02 09:59:52', 3);
INSERT INTO Review VALUES (32, 9, 25, 'Exactly what I needed — 10/10.', '2025-01-25 20:15:46', 2);
INSERT INTO Review VALUES (33, 10, 5, 'Very professional, thank you!', '2025-02-20 05:24:17', 5);
INSERT INTO Review VALUES (34, 1, 40, 'Honest seller, would buy again.', '2025-02-05 13:09:37', 2);
INSERT INTO Review VALUES (35, 29, 23, 'Not as described but refunded me.', '2025-03-07 04:09:38', 2);
INSERT INTO Review VALUES (36, 10, 27, 'Cute item, slightly overpriced though.', '2025-01-18 08:10:02', 4);
INSERT INTO Review VALUES (37, 14, 6, 'Great communication and quick pickup.', '2025-02-13 03:46:35', 1);
INSERT INTO Review VALUES (38, 9, 8, 'Cute item, slightly overpriced though.', '2025-03-10 23:44:26', 4);
INSERT INTO Review VALUES (39, 23, 28, 'Took a while to respond but item was fine.', '2025-02-13 08:47:00', 2);
INSERT INTO Review VALUES (40, 16, 18, 'Honest seller, would buy again.', '2025-03-01 15:07:15', 1);
INSERT INTO Review VALUES (41, 16, 36, 'Cute item, slightly overpriced though.', '2025-03-23 15:32:39', 5);
INSERT INTO Review VALUES (42, 39, 19, 'Exactly what I needed — 10/10.', '2025-03-06 08:02:59', 1);
INSERT INTO Review VALUES (43, 20, 14, 'Very professional, thank you!', '2025-03-14 04:09:56', 5);
INSERT INTO Review VALUES (44, 33, 13, 'Not as described but refunded me.', '2025-02-20 14:17:38', 4);
INSERT INTO Review VALUES (45, 19, 4, 'Exactly what I needed — 10/10.', '2025-02-27 02:22:39', 2);
INSERT INTO Review VALUES (46, 32, 25, 'Item arrived as described.', '2025-04-01 01:16:52', 2);
INSERT INTO Review VALUES (47, 32, 39, 'Item arrived as described.', '2025-01-23 20:54:05', 5);
INSERT INTO Review VALUES (48, 1, 24, 'Great communication and quick pickup.', '2025-04-02 08:51:33', 3);
INSERT INTO Review VALUES (49, 9, 25, 'Bundle deal was appreciated!', '2025-01-11 10:09:09', 5);
INSERT INTO Review VALUES (50, 27, 24, 'Very professional, thank you!', '2025-01-14 19:53:21', 2);
INSERT INTO Review VALUES (51, 31, 5, 'Great seller, fast shipping!', '2025-04-02 16:42:11', 5);
INSERT INTO Review VALUES (52, 5, 1, 'Super friendly and easy to work with!', '2025-02-07 18:38:23', 2);
INSERT INTO Review VALUES (53, 3, 4, 'Exactly what I needed — 10/10.', '2025-04-08 04:23:37', 4);
INSERT INTO Review VALUES (54, 33, 19, 'Honest seller, would buy again.', '2025-01-24 06:22:57', 5);
INSERT INTO Review VALUES (55, 27, 28, 'Not as described but refunded me.', '2025-03-16 02:42:26', 4);
INSERT INTO Review VALUES (56, 6, 35, 'Very professional, thank you!', '2025-02-27 22:26:18', 5);
INSERT INTO Review VALUES (57, 10, 18, 'Item arrived as described.', '2025-03-22 05:13:09', 3);
INSERT INTO Review VALUES (58, 6, 33, 'Great communication and quick pickup.', '2025-01-11 11:56:49', 2);
INSERT INTO Review VALUES (59, 10, 35, 'Took a while to respond but item was fine.', '2025-01-30 06:40:42', 4);
INSERT INTO Review VALUES (60, 38, 5, 'Super friendly and easy to work with!', '2025-01-27 16:10:06', 4);
INSERT INTO Review VALUES (61, 16, 4, 'Wouldn’t recommend — item was dirty.', '2025-02-08 21:26:59', 1);
INSERT INTO Review VALUES (62, 28, 8, 'Flaked on meetup :(', '2025-03-08 12:57:26', 5);
INSERT INTO Review VALUES (63, 39, 4, 'Super friendly and easy to work with!', '2025-03-21 10:58:19', 2);
INSERT INTO Review VALUES (64, 8, 1, 'Not as described but refunded me.', '2025-03-30 20:26:14', 2);
INSERT INTO Review VALUES (65, 1, 11, 'Flaked on meetup :(', '2025-01-28 19:28:22', 3);
INSERT INTO Review VALUES (66, 34, 17, 'Rude but responsive buyer.', '2025-03-03 10:27:13', 3);
INSERT INTO Review VALUES (67, 9, 18, 'Not as described but refunded me.', '2025-02-05 00:31:24', 1);
INSERT INTO Review VALUES (68, 2, 22, 'Exactly what I needed — 10/10.', '2025-01-16 16:36:31', 4);
INSERT INTO Review VALUES (69, 18, 34, 'Item arrived as described.', '2025-04-05 16:17:29', 3);
INSERT INTO Review VALUES (70, 37, 5, 'Flaked on meetup :(', '2025-03-06 14:09:56', 4);
INSERT INTO Review VALUES (71, 33, 24, 'Great seller, fast shipping!', '2025-02-04 08:03:38', 4);
INSERT INTO Review VALUES (72, 37, 11, 'Took a while to respond but item was fine.', '2025-03-02 20:36:55', 2);
INSERT INTO Review VALUES (73, 17, 7, 'Great communication and quick pickup.', '2025-01-12 06:21:46', 5);
INSERT INTO Review VALUES (74, 8, 15, 'Not as described but refunded me.', '2025-01-01 21:57:59', 5);
INSERT INTO Review VALUES (75, 1, 3, 'Bundle deal was appreciated!', '2025-03-29 18:43:14', 1);
INSERT INTO ListingTag VALUES (29, 3);
INSERT INTO ListingTag VALUES (19, 8);
INSERT INTO ListingTag VALUES (18, 11);
INSERT INTO ListingTag VALUES (21, 18);
INSERT INTO ListingTag VALUES (6, 5);
INSERT INTO ListingTag VALUES (10, 8);
INSERT INTO ListingTag VALUES (25, 5);
INSERT INTO ListingTag VALUES (14, 3);
INSERT INTO ListingTag VALUES (27, 14);
INSERT INTO ListingTag VALUES (22, 18);
INSERT INTO ListingTag VALUES (30, 14);
INSERT INTO ListingTag VALUES (4, 7);
INSERT INTO ListingTag VALUES (27, 13);
INSERT INTO ListingTag VALUES (38, 1);
INSERT INTO ListingTag VALUES (37, 13);
INSERT INTO ListingTag VALUES (31, 1);
INSERT INTO ListingTag VALUES (23, 10);
INSERT INTO ListingTag VALUES (25, 14);
INSERT INTO ListingTag VALUES (35, 18);
INSERT INTO ListingTag VALUES (39, 8);
INSERT INTO ListingTag VALUES (32, 8);
INSERT INTO ListingTag VALUES (18, 14);
INSERT INTO ListingTag VALUES (32, 1);
INSERT INTO ListingTag VALUES (25, 11);
INSERT INTO ListingTag VALUES (26, 6);
INSERT INTO ListingTag VALUES (30, 5);
INSERT INTO ListingTag VALUES (40, 18);
INSERT INTO ListingTag VALUES (2, 13);
INSERT INTO ListingTag VALUES (38, 19);
INSERT INTO ListingTag VALUES (2, 3);
INSERT INTO ListingTag VALUES (28, 5);
INSERT INTO ListingTag VALUES (30, 6);
INSERT INTO ListingTag VALUES (4, 9);
INSERT INTO ListingTag VALUES (14, 15);
INSERT INTO ListingTag VALUES (21, 11);
INSERT INTO ListingTag VALUES (25, 9);
INSERT INTO ListingTag VALUES (27, 9);
INSERT INTO ListingTag VALUES (6, 16);
INSERT INTO ListingTag VALUES (2, 18);
INSERT INTO ListingTag VALUES (4, 12);
INSERT INTO ListingTag VALUES (15, 3);
INSERT INTO ListingTag VALUES (3, 1);
INSERT INTO ListingTag VALUES (16, 7);
INSERT INTO ListingTag VALUES (2, 20);
INSERT INTO ListingTag VALUES (9, 16);
INSERT INTO ListingTag VALUES (8, 19);
INSERT INTO ListingTag VALUES (17, 12);
INSERT INTO ListingTag VALUES (11, 20);
INSERT INTO ListingTag VALUES (39, 4);
INSERT INTO ListingTag VALUES (11, 10);
INSERT INTO ListingTag VALUES (7, 19);
INSERT INTO ListingTag VALUES (2, 10);
INSERT INTO ListingTag VALUES (26, 7);
INSERT INTO ListingTag VALUES (5, 19);
INSERT INTO ListingTag VALUES (16, 4);
INSERT INTO ListingTag VALUES (20, 20);
INSERT INTO ListingTag VALUES (3, 12);
INSERT INTO ListingTag VALUES (35, 14);
INSERT INTO ListingTag VALUES (24, 3);
INSERT INTO ListingTag VALUES (33, 11);
INSERT INTO ListingTag VALUES (1, 14);
INSERT INTO ListingTag VALUES (32, 4);
INSERT INTO ListingTag VALUES (28, 12);
INSERT INTO ListingTag VALUES (28, 6);
INSERT INTO ListingTag VALUES (34, 9);
INSERT INTO ListingTag VALUES (31, 15);
INSERT INTO ListingTag VALUES (28, 19);
INSERT INTO ListingTag VALUES (16, 3);
INSERT INTO ListingTag VALUES (18, 15);
INSERT INTO ListingTag VALUES (16, 15);
INSERT INTO ListingTag VALUES (37, 20);
INSERT INTO ListingTag VALUES (2, 16);
INSERT INTO ListingTag VALUES (21, 6);
INSERT INTO ListingTag VALUES (32, 7);
INSERT INTO ListingTag VALUES (23, 9);
INSERT INTO ListingTag VALUES (22, 9);
INSERT INTO ListingTag VALUES (39, 9);
INSERT INTO ListingTag VALUES (36, 1);
INSERT INTO ListingTag VALUES (34, 7);
INSERT INTO ListingTag VALUES (6, 8);
INSERT INTO ListingTag VALUES (27, 16);
INSERT INTO ListingTag VALUES (36, 8);
INSERT INTO ListingTag VALUES (31, 16);
INSERT INTO ListingTag VALUES (29, 1);
INSERT INTO ListingTag VALUES (6, 10);
INSERT INTO ListingTag VALUES (15, 13);
INSERT INTO ListingTag VALUES (16, 10);
INSERT INTO ListingTag VALUES (38, 12);
INSERT INTO ListingTag VALUES (31, 18);
INSERT INTO ListingTag VALUES (34, 12);
INSERT INTO ListingTag VALUES (28, 18);
INSERT INTO ListingTag VALUES (22, 12);
INSERT INTO ListingTag VALUES (30, 9);
INSERT INTO ListingTag VALUES (20, 9);
INSERT INTO ListingTag VALUES (15, 4);
INSERT INTO ListingTag VALUES (13, 11);
INSERT INTO ListingTag VALUES (8, 18);
INSERT INTO ListingTag VALUES (12, 7);
INSERT INTO ListingTag VALUES (14, 16);
INSERT INTO ListingTag VALUES (18, 19);
INSERT INTO ListingTag VALUES (34, 20);
INSERT INTO ListingTag VALUES (19, 4);
INSERT INTO ListingTag VALUES (13, 10);
INSERT INTO ListingTag VALUES (15, 12);
INSERT INTO ListingTag VALUES (12, 10);
INSERT INTO ListingTag VALUES (1, 18);
INSERT INTO ListingTag VALUES (9, 9);
INSERT INTO ListingTag VALUES (3, 2);
INSERT INTO ListingTag VALUES (36, 10);
INSERT INTO ListingTag VALUES (7, 1);
INSERT INTO ListingTag VALUES (37, 10);
INSERT INTO ListingTag VALUES (29, 11);
INSERT INTO ListingTag VALUES (12, 2);
INSERT INTO ListingTag VALUES (17, 16);
INSERT INTO ListingTag VALUES (8, 3);
INSERT INTO ListingTag VALUES (26, 16);
INSERT INTO ListingTag VALUES (4, 5);
INSERT INTO ListingTag VALUES (10, 19);
INSERT INTO ListingTag VALUES (20, 3);
INSERT INTO ListingTag VALUES (36, 14);
INSERT INTO ListingTag VALUES (39, 20);
INSERT INTO ListingTag VALUES (40, 8);
INSERT INTO ListingTag VALUES (34, 13);
INSERT INTO ListingTag VALUES (29, 15);
INSERT INTO ListingTag VALUES (20, 19);
INSERT INTO ListingTag VALUES (28, 10);
INSERT INTO ListingTag VALUES (4, 20);
INSERT INTO ListingTag VALUES (7, 7);
INSERT INTO ListingTag VALUES (14, 9);
INSERT INTO ListingTag VALUES (6, 6);
INSERT INTO ListingTag VALUES (16, 6);
INSERT INTO ListingTag VALUES (36, 3);
INSERT INTO ListingTag VALUES (11, 1);
INSERT INTO ListingTag VALUES (27, 15);
INSERT INTO ListingTag VALUES (39, 16);
INSERT INTO ListingTag VALUES (19, 2);