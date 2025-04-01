
-- CreateEnum
CREATE TYPE "StockStatus" AS ENUM ('EXPIRE', 'AVAILABLE', 'OUT_OF_STOCK');

-- CreateEnum
CREATE TYPE "Payment" AS ENUM ('CASH', 'TRANSFER');

-- CreateEnum
CREATE TYPE "SlipStatus" AS ENUM ('INVALID', 'VALID', 'NO_SLIP');

-- CreateEnum
CREATE TYPE "OrderProcess" AS ENUM ('PENDING', 'DONE', 'COMPLETE', 'CANCEL');

-- CreateEnum
CREATE TYPE "IngredientAge" AS ENUM ('DAY', 'WEEK', 'MONTH', 'YEAR');

-- CreateEnum
CREATE TYPE "MenuStatus" AS ENUM ('ENABLE', 'DISABLE');

-- CreateTable
CREATE TABLE "Shop" (
    "id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "user" TEXT NOT NULL,
    "open" BOOLEAN NOT NULL DEFAULT false,
    "create" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "account" TEXT NOT NULL DEFAULT '',
    "account_eng" TEXT NOT NULL DEFAULT '',

    CONSTRAINT "Shop_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Menu" (
    "id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "price" DOUBLE PRECISION NOT NULL,
    "shop" TEXT NOT NULL,
    "status" "MenuStatus" NOT NULL DEFAULT 'ENABLE',

    CONSTRAINT "Menu_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Recipe" (
    "menu" TEXT NOT NULL,
    "ingredient" TEXT NOT NULL,
    "amount" DOUBLE PRECISION NOT NULL,

    CONSTRAINT "Recipe_pkey" PRIMARY KEY ("menu","ingredient")
);

-- CreateTable
CREATE TABLE "Ingredient" (
    "id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "unit" TEXT NOT NULL,
    "ages" INTEGER NOT NULL,
    "ages_unit" "IngredientAge" NOT NULL,
    "shop" TEXT NOT NULL,

    CONSTRAINT "Ingredient_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Stock" (
    "id" TEXT NOT NULL,
    "add_date" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "expire" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "remain" DOUBLE PRECISION NOT NULL,
    "status" "StockStatus" NOT NULL DEFAULT 'AVAILABLE',
    "ingredient" TEXT NOT NULL,

    CONSTRAINT "Stock_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Receipt" (
    "id" TEXT NOT NULL,
    "date" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "total" DOUBLE PRECISION NOT NULL,
    "shop" TEXT NOT NULL,
    "image" TEXT NOT NULL,

    CONSTRAINT "Receipt_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "ReceiptItem" (
    "id" TEXT NOT NULL,
    "receipt" TEXT NOT NULL,
    "item" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "price" DOUBLE PRECISION NOT NULL,
    "quantity" DOUBLE PRECISION NOT NULL,

    CONSTRAINT "ReceiptItem_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Order" (
    "id" TEXT NOT NULL,
    "customer" TEXT NOT NULL,
    "date" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "payment" "Payment",
    "address" TEXT,
    "total" DOUBLE PRECISION NOT NULL DEFAULT 0,
    "remain" DOUBLE PRECISION NOT NULL DEFAULT 0,
    "process" "OrderProcess" NOT NULL DEFAULT 'PENDING',
    "shop" TEXT NOT NULL,

    CONSTRAINT "Order_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "OrderDetail" (
    "id" TEXT NOT NULL,
    "menu" TEXT NOT NULL,
    "amount" INTEGER NOT NULL,
    "order" TEXT NOT NULL,

    CONSTRAINT "OrderDetail_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Slip" (
    "id" TEXT NOT NULL,
    "receiver" TEXT NOT NULL,
    "sender" TEXT NOT NULL,
    "amount" DOUBLE PRECISION NOT NULL,
    "date" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "ref" TEXT NOT NULL,
    "status" "SlipStatus" NOT NULL DEFAULT 'NO_SLIP',
    "order" TEXT NOT NULL,

    CONSTRAINT "Slip_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "Shop_name_key" ON "Shop"("name");

-- CreateIndex
CREATE UNIQUE INDEX "Shop_user_key" ON "Shop"("user");

-- CreateIndex
CREATE UNIQUE INDEX "Slip_ref_key" ON "Slip"("ref");

-- AddForeignKey
ALTER TABLE "Menu" ADD CONSTRAINT "Menu_shop_fkey" FOREIGN KEY ("shop") REFERENCES "Shop"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Recipe" ADD CONSTRAINT "Recipe_menu_fkey" FOREIGN KEY ("menu") REFERENCES "Menu"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Recipe" ADD CONSTRAINT "Recipe_ingredient_fkey" FOREIGN KEY ("ingredient") REFERENCES "Ingredient"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Ingredient" ADD CONSTRAINT "Ingredient_shop_fkey" FOREIGN KEY ("shop") REFERENCES "Shop"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Stock" ADD CONSTRAINT "Stock_ingredient_fkey" FOREIGN KEY ("ingredient") REFERENCES "Ingredient"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Receipt" ADD CONSTRAINT "Receipt_shop_fkey" FOREIGN KEY ("shop") REFERENCES "Shop"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "ReceiptItem" ADD CONSTRAINT "ReceiptItem_receipt_fkey" FOREIGN KEY ("receipt") REFERENCES "Receipt"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Order" ADD CONSTRAINT "Order_shop_fkey" FOREIGN KEY ("shop") REFERENCES "Shop"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "OrderDetail" ADD CONSTRAINT "OrderDetail_menu_fkey" FOREIGN KEY ("menu") REFERENCES "Menu"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "OrderDetail" ADD CONSTRAINT "OrderDetail_order_fkey" FOREIGN KEY ("order") REFERENCES "Order"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Slip" ADD CONSTRAINT "Slip_order_fkey" FOREIGN KEY ("order") REFERENCES "Order"("id") ON DELETE CASCADE ON UPDATE CASCADE;
