##### upgrade #####
CREATE TABLE IF NOT EXISTS "statistics_data" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "meta_id" INT NOT NULL,
    "d_t" TIMESTAMP NOT NULL,
    "val" INT NOT NULL,
    CONSTRAINT "uid_statistics__meta_id_fbfe00" UNIQUE ("meta_id", "d_t")
) /* 统计数据  */;
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" TEXT NOT NULL
);
