DROP DATABASE wuliu;
CREATE DATABASE wuliu;
USE wuliu;
CREATE TABLE Grid (
  GridID INT PRIMARY KEY,
  LeftLongitude DOUBLE,
  RightLongitude DOUBLE,
  UpperLatitude DOUBLE,
  LowerLatitude DOUBLE
);
CREATE TABLE User (
  UserID INT PRIMARY KEY,
  Longitude DOUBLE,
  Latitude DOUBLE,
  Priority INT
);
CREATE TABLE Product (
  ProductID INT PRIMARY KEY,
  Category VARCHAR(255),
  Name VARCHAR(255),
  Abbreviation VARCHAR(255),
  Unit VARCHAR(255)
);

CREATE TABLE Warehouse (
  WarehouseID INT PRIMARY KEY,
  Longitude DOUBLE,
  Latitude DOUBLE,
  CoverageRange DOUBLE
);
CREATE TABLE WarehouseProduct (
  WarehouseID INT,
  ProductID INT,
  Stock INT,
  MinStock INT,
  MaxStock INT,
  PRIMARY KEY (WarehouseID, ProductID),
  FOREIGN KEY (WarehouseID) REFERENCES Warehouse(WarehouseID),
  FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);
CREATE TABLE Transportation (
  TransportID INT PRIMARY KEY,
  StartWarehouseID INT,
  EndLongitude DOUBLE,
  EndLatitude DOUBLE,
  CostTime INT,
  FOREIGN KEY (StartWarehouseID) REFERENCES Warehouse(WarehouseID)
);
CREATE TABLE TransportationProduct (
  TransportID INT,
  ProductID INT,
  Quantity INT,
  PRIMARY KEY (TransportID, ProductID),
  FOREIGN KEY (TransportID) REFERENCES Transportation(TransportID),
  FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);
CREATE TABLE Demand (
  DemandID INT PRIMARY KEY,
  StartEarliestTime DATETIME,
  StartLatestTime DATETIME,
  EndEarliestTime DATETIME,
  EndLatestTime DATETIME,
  UserID INT,
  FOREIGN KEY (UserID) REFERENCES User(UserID)
);
CREATE TABLE DemandProduct (
  DemandID INT,
  ProductID INT,
  Quantity INT,
  PRIMARY KEY (DemandID, ProductID),
  FOREIGN KEY (DemandID) REFERENCES Demand(DemandID),
  FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);
