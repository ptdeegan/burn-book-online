CREATE TABLE "users" (
  "user_id" int UNIQUE PRIMARY KEY NOT NULL,
  "first_name" varchar NOT NULL,
  "last_name" varchar NOT NULL,
  "email" varchar UNIQUE NOT NULL,
  "date_of_birth" date NOT NULL
);

CREATE TABLE "posts" (
  "post_id" int UNIQUE PRIMARY KEY NOT NULL,
  "post_body" varchar NOT NULL,
  "post_burns" int NOT NULL,
  "post_douses" int NOT NULL,
  "burn_status" boolean NOT NULL
);

CREATE TABLE "user_likes" (
  "user_id" int NOT NULL,
  "post_id" int NOT NULL
);

ALTER TABLE "user_likes" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("user_id");

ALTER TABLE "user_likes" ADD FOREIGN KEY ("post_id") REFERENCES "posts" ("post_id");
