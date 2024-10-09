from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "username" VARCHAR(15) NOT NULL,
    "tg_id" BIGINT NOT NULL,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "car" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "brand" VARCHAR(255) NOT NULL,
    "model" VARCHAR(255) NOT NULL,
    "year" INT NOT NULL,
    "engine" VARCHAR(255) NOT NULL,
    "mileage" BIGINT NOT NULL,
    "image" VARCHAR(255),
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "notes" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_date" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "price" VARCHAR(40),
    "title" VARCHAR(255),
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "purchases" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "image" TEXT,
    "text" TEXT,
    "price" VARCHAR(40),
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "reminders" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "total_date" DATE NOT NULL,
    "text" TEXT NOT NULL,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "service" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "type" VARCHAR(2) NOT NULL,
    "date" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "car_id" INT NOT NULL REFERENCES "car" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
