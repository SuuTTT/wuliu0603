SET FOREIGN_KEY_CHECKS = 0; 
TRUNCATE TABLE DemandProduct;
TRUNCATE TABLE TransportationProduct;
TRUNCATE TABLE Demand;
TRUNCATE TABLE Transportation;
TRUNCATE TABLE WarehouseProduct;
TRUNCATE TABLE Product;
TRUNCATE TABLE User;
TRUNCATE TABLE Warehouse;
TRUNCATE TABLE Grid;
SET FOREIGN_KEY_CHECKS = 1; 


-- Insert sample data into Grid
INSERT INTO Grid (GridID, LeftLongitude, RightLongitude, UpperLatitude, LowerLatitude)
VALUES (1, -120.5, -119.5, 38.5, 37.5),
       (2, -119.5, -118.5, 38.5, 37.5),
       (3, -120.5, -119.5, 37.5, 36.5),
       (4, -119.5, -118.5, 37.5, 36.5);

-- Insert sample data into User
INSERT INTO User (UserID, Longitude, Latitude, Priority)
VALUES (1, -120, 38, 1),
       (2, -119, 38, 2),
       (3, -120, 37, 3),
       (4, -119, 37, 4);

-- Insert sample data into Product
INSERT INTO Product (ProductID, Category, Name, Abbreviation, Unit)
VALUES (1, 'Food', 'Apple', 'Appl', 'Kg'),
       (2, 'Food', 'Banana', 'Bana', 'Kg'),
       (3, 'Drink', 'Water', 'Wat', 'Liter'),
       (4, 'Drink', 'Juice', 'Juic', 'Liter');

-- Insert sample data into Warehouse
INSERT INTO Warehouse (WarehouseID, Longitude, Latitude, CoverageRange)
VALUES (1, -120.1, 38.1, 100),
       (2, -119.1, 38.1, 100),
       (3, -120.1, 37.1, 100),
       (4, -119.1, 37.1, 100);

-- Insert sample data into WarehouseProduct
INSERT INTO WarehouseProduct (WarehouseID, ProductID, Stock, MinStock, MaxStock)
VALUES (1, 1, 1000, 500, 2000),
       (2, 2, 1000, 500, 2000),
       (3, 3, 2000, 1000, 4000),
       (4, 4, 2000, 1000, 4000);

-- Insert sample data into Transportation
INSERT INTO Transportation (TransportID, StartWarehouseID, EndLongitude, EndLatitude, CostTime)
VALUES (1, 1, -119.9, 37.9, 60),
       (2, 2, -120.9, 37.9, 60),
       (3, 3, -119.9, 38.9, 60),
       (4, 4, -120.9, 38.9, 60);

-- Insert sample data into TransportationProduct
INSERT INTO TransportationProduct (TransportID, ProductID, Quantity)
VALUES (1, 1, 100),
       (2, 2, 200),
       (3, 3, 300),
       (4, 4, 400);

-- Insert sample data into Demand
INSERT INTO Demand (DemandID, StartEarliestTime, StartLatestTime, EndEarliestTime, EndLatestTime, UserID)
VALUES (1, '2023-06-02 08:00:00', '2023-06-02 10:00:00', '2023-06-02 12:00:00', '2023-06-02 14:00:00', 1),
       (2, '2023-06-02 09:00:00', '2023-06-02 11:00:00', '2023-06-02 13:00:00', '2023-06-02 15:00:00', 2),
       (3, '2023-06-02 10:00:00', '2023-06-02 12:00:00', '2023-06-02 14:00:00', '2023-06-02 16:00:00', 3),
       (4, '2023-06-02 11:00:00', '2023-06-02 13:00:00', '2023-06-02 15:00:00', '2023-06-02 17:00:00', 4);

-- Insert sample data into DemandProduct
INSERT INTO DemandProduct (DemandID, ProductID, Quantity)
VALUES (1, 1, 50),
       (2, 2, 60),
       (3, 3, 70),
       (4, 4, 80);
