--?-------------------------- INITIALIZE ----------------------------
CREATE TABLE "Users" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "first_name" varchar,
    "last_name" varchar,
    "email" varchar,
    "bio" varchar,
    "username" varchar,
    "password" varchar,
    "profile_image_url" varchar,
    "created_on" date,
    "active" bit
);
INSERT INTO Users
VALUES (
        null,
        "admin",
        "adminson",
        "admin@rare.com",
        null,
        null,
        "password",
        null,
        "7/29/2021",
        1
    ) CREATE TABLE "DemotionQueue" (
        "action" varchar,
        "admin_id" INTEGER,
        "approver_one_id" INTEGER,
        FOREIGN KEY(`admin_id`) REFERENCES `Users`(`id`),
        FOREIGN KEY(`approver_one_id`) REFERENCES `Users`(`id`),
        PRIMARY KEY (action, admin_id, approver_one_id)
    );
CREATE TABLE "Subscriptions" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "follower_id" INTEGER,
    "author_id" INTEGER,
    "created_on" date,
    FOREIGN KEY(`follower_id`) REFERENCES `Users`(`id`),
    FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);
CREATE TABLE "Posts" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "user_id" INTEGER,
    "category_id" INTEGER,
    "title" varchar,
    "publication_date" date,
    "image_url" varchar,
    "content" varchar,
    "approved" bit
);

-- INSERT INTO Posts VALUES (null, 1, 1, "YOU WON'T BELIEVE YOUR EYES", "7/29/2021", "https://previews.123rf.com/images/bowie15/bowie151401/bowie15140100076/39843044-shocked-face-guy.jpg", "Rare is making headway in the dumb industry", 1)

INSERT INTO Posts VALUES (null, 1, 1, "IF YOU CLICK THIS, YOU'LL WANNA KISS YOUR DAD", "7/29/2021", "https://previews.123rf.com/images/bowie15/bowie151401/bowie15140100076/39843044-shocked-face-guy.jpg", "namsayin", 1)

CREATE TABLE "Comments" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "post_id" INTEGER,
    "author_id" INTEGER,
    "content" varchar,
    FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
    FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);

INSERT INTO Comments VALUES (null, 2, 1, "boop.")

CREATE TABLE "Reactions" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "label" varchar,
    "image_url" varchar
);
CREATE TABLE "PostReactions" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "user_id" INTEGER,
    "reaction_id" INTEGER,
    "post_id" INTEGER,
    FOREIGN KEY(`user_id`) REFERENCES `Users`(`id`),
    FOREIGN KEY(`reaction_id`) REFERENCES `Reactions`(`id`),
    FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`)
);
CREATE TABLE "Tags" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "label" varchar
);
CREATE TABLE "PostTags" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "post_id" INTEGER,
    "tag_id" INTEGER,
    FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
    FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)
);
CREATE TABLE "Categories" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "label" varchar
);
INSERT INTO Categories ('label')
VALUES ('News');
INSERT INTO Tags ('label')
VALUES ('JavaScript');
INSERT INTO Reactions ('label', 'image_url')
VALUES ('happy', 'https://pngtree.com/so/happy');

--?-------------------------- TEST ----------------------------

SELECT 
    com.id as comment_id,
    com.post_id,
    com.author_id,
    com.content as comment_content,
    pos.id as OP_id,
    pos.user_id,
    pos.category_id,
    pos.title,
    pos.publication_date,
    pos.image_url,
    pos.content as post_content,
    pos.approved
FROM Comments com
JOIN Posts pos 
    ON pos.id = com.post_id
    

SELECT
    com.id as comment_id,
    com.post_id,
    com.author_id,
    com.content as comment_content
FROM Comments com

DELETE FROM Comments WHERE id = 11

SELECT 
            com.id as comment_id,
            com.post_id,
            com.author_id,
            com.content as comment_content,
            pos.id,
            pos.user_id,
            pos.category_id,
            pos.title,
            pos.publication_date,
            pos.image_url,
            pos.content as post_content,
            pos.approved,
            user.id,
            user.first_name,
            user.last_name,
            user.email,
            user.bio,
            user.username,
            user.password,
            user.profile_image_url,
            user.created_on,
            user.active
        FROM Comments com
        JOIN Posts pos 
            ON pos.id = com.post_id
        JOIN Users user
            ON com.author_id = user.id
        