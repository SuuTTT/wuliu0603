TRUNCATE TABLE Grid;
TRUNCATE TABLE User;
TRUNCATE TABLE Product;
TRUNCATE TABLE Warehouse;
TRUNCATE TABLE WarehouseProduct;
TRUNCATE TABLE Transportation;
TRUNCATE TABLE TransportationProduct;
TRUNCATE TABLE Demand;
TRUNCATE TABLE DemandProduct;

-- Insert sample data into Grid
INSERT INTO Grid (GridID, LeftLongitude, RightLongitude, UpperLatitude, LowerLatitude)
VALUES (1, -120.5, -119.5, 38.5, 37.5);

-- Insert sample data into User
INSERT INTO User (UserID, Longitude, Latitude, Priority)
VALUES (1, -120, 38, 1);

-- Insert sample data into Product
INSERT INTO Product (ProductID, Category, Name, Abbreviation, Unit)
VALUES (1, 'Food', 'Apple', 'Appl', 'Kg');

-- Insert sample data into Warehouse
INSERT INTO Warehouse (WarehouseID, Longitude, Latitude, CoverageRange)
VALUES (1, -120.1, 38.1, 100);

-- Insert sample data into WarehouseProduct
INSERT INTO WarehouseProduct (WarehouseID, ProductID, Stock, MinStock, MaxStock)
VALUES (1, 1, 1000, 500, 2000);

-- Insert sample data into Transportation
INSERT INTO Transportation (TransportID, StartWarehouseID, EndLongitude, EndLatitude, CostTime)
VALUES (1, 1, -119.9, 37.9, 60);

-- Insert sample data into TransportationProduct
INSERT INTO TransportationProduct (TransportID, ProductID, Quantity)
VALUES (1, 1, 100);

-- Insert sample data into Demand
INSERT INTO Demand (DemandID, StartEarliestTime, StartLatestTime, EndEarliestTime, EndLatestTime, UserID)
VALUES (1, '2023-06-02 08:00:00', '2023-06-02 10:00:00', '2023-06-02 12:00:00', '2023-06-02 14:00:00', 1);

-- Insert sample data into DemandProduct
INSERT INTO DemandProduct (DemandID, ProductID, Quantity)
VALUES (1, 1, 50);
