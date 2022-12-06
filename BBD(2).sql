CREATE TABLE "users" (
  "user_id" INT GENERATED BY DEFAULT AS IDENTITY UNIQUE PRIMARY KEY NOT NULL,
  "first_name" varchar NOT NULL,
  "last_name" varchar NOT NULL,
  "email" varchar UNIQUE NOT NULL,
  "date_of_birth" date NOT NULL,
  "admin_status" boolean NOT NULL
);

CREATE TABLE "posts" (
  "user_id" int NOT NULL,
  "post_title" varchar NOT NULL,
  "post_id" INT GENERATED BY DEFAULT AS IDENTITY UNIQUE PRIMARY KEY NOT NULL,
  "post_body" varchar NOT NULL,
  "burn_status" boolean NOT NULL
);

CREATE TABLE "user_likes" (
  "user_id" int NOT NULL,
  "post_id" int NOT NULL,
  "is_burn" boolean NOT NULL
);

CREATE TABLE "comments" (
  "user_id" int NOT NULL,
  "post_id" int NOT NULL,
  "comment_id" INT GENERATED BY DEFAULT AS IDENTITY UNIQUE PRIMARY KEY NOT NULL,
  "comment_body" varchar NOT NULL
);

ALTER TABLE "user_likes" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("user_id");

ALTER TABLE "user_likes" ADD FOREIGN KEY ("post_id") REFERENCES "posts" ("post_id");

ALTER TABLE "posts" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("user_id");

ALTER TABLE "comments" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("user_id");

ALTER TABLE "comments" ADD FOREIGN KEY ("post_id") REFERENCES "posts" ("post_id");
