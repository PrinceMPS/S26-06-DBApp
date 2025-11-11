CREATE DATABASE Hotel_Management;
USE Hotel_Management;


CREATE TABLE guest(
    guest_id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    contact_number VARCHAR(15) NOT NULL,
    email_address VARCHAR(35) NOT NULL,
    nationality VARCHAR(20) NOT NULL,
    PRIMARY KEY (guest_id)
);

CREATE TABLE RoomType (
    room_type_id INT PRIMARY KEY AUTO_INCREMENT,
    type_name VARCHAR(50) NOT NULL,
    rate_per_type DECIMAL(10,2) NOT NULL,
    capacity INT NOT NULL
);

CREATE TABLE room(
    room_id INT PRIMARY KEY AUTO_INCREMENT,
    room_type_id  INT NOT NULL,
    availability_status ENUM('Booked', 'Vacant') DEFAULT 'Vacant' NOT NULL,
    housekeeping_status ENUM('For Cleaning', 'Under Maintainance', 'Ready') DEFAULT 'Ready' NOT NULL,
   
   
   -- Foreign Key
    FOREIGN KEY (room_type_id) REFERENCES roomtype(room_type_id)
);

CREATE TABLE employee(
    employee_id INT NOT NULL AUTO_INCREMENT,
	first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    emp_position ENUM ('frontdesk','housekeeping','admin') NOT NULL,
    shift ENUM('Morning', 'Afternoon', 'Night') NOT NULL,
    emp_status ENUM('Active', 'Leave-vacation', 'Leave-sick', 'Leave-maternity') DEFAULT 'Active' NOT NULL,
    PRIMARY KEY (employee_id)
);


CREATE TABLE housekeeping_item(
    housekeeping_item_id INT NOT NULL AUTO_INCREMENT,
	item_name VARCHAR(20) NOT NULL,
    cost_per_unit DECIMAL(10,2) NOT NULL,
    current_stock INT NOT NULL,
    minimum_stock INT NOT NULL,
	max_stock_storage INT NOT NULL,
    PRIMARY KEY (housekeeping_item_id)
);

CREATE TABLE booking (
    booking_id INT NOT NULL AUTO_INCREMENT,
    guest_id INT NOT NULL,
    room_id INT NOT NULL,
    booking_date DATE NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    
    PRIMARY KEY (booking_id),
    
    -- Foreign Keys
    FOREIGN KEY (guest_id) REFERENCES guest(guest_id),
    FOREIGN KEY (room_id) REFERENCES room(room_id)
);

CREATE TABLE payment (
    payment_id INT NOT NULL AUTO_INCREMENT,
    booking_id INT NOT NULL,
    amount_paid DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(20) NOT NULL,
    payment_date DATE NOT NULL,
    
    PRIMARY KEY (payment_id),
    
    -- Foreign Keys
    FOREIGN KEY (booking_id) REFERENCES booking(booking_id)
);

CREATE TABLE GuestStay(
    transaction_id INT NOT NULL AUTO_INCREMENT,
    booking_id INT NOT NULL,
    employee_id INT NOT NULL,
    check_in_time_date DATETIME,
    expected_check_out_time_date DATETIME,
    actual_check_out_time_date DATETIME,
    remarks VARCHAR(100),

    PRIMARY KEY (transaction_id),
    
    -- Foreign Keys
    FOREIGN KEY (booking_id) REFERENCES booking(booking_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
);



CREATE TABLE housekeeping_item_issuance (
    issuance_id INT NOT NULL AUTO_INCREMENT,
	housekeeping_item_id  INT NOT NULL,
    employee_id INT NOT NULL,
    quantity_issued INT NOT NULL,
    date_issued DATETIME DEFAULT CURRENT_TIMESTAMP,
    issuance_status ENUM('pending','issued'),
    remarks TEXT,

    PRIMARY KEY (issuance_id),

    -- Foreign Keys
    FOREIGN KEY (housekeeping_item_id ) REFERENCES housekeeping_item(housekeeping_item_id ),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
);

-- Guests
INSERT INTO guest (first_name, last_name, contact_number, email_address, nationality) VALUES
('Maria', 'Santos', '09171234567', 'maria.santos@gmail.com', 'Filipino'),
('John', 'Doe', '09981234567', 'john.doe@yahoo.com', 'American'),
('Akira', 'Tanaka', '09185553333', 'akira.tanaka@gmail.com', 'Japanese'),
('Anna', 'Cruz', '09190001111', 'anna.cruz@gmail.com', 'Filipino');

-- Room Types
INSERT INTO RoomType (type_name, rate_per_type, capacity) VALUES
('Standard', 1500.00, 2),
('Deluxe', 2500.00, 3),
('Suite', 4000.00, 4);

-- Rooms
INSERT INTO room (room_type_id, availability_status, housekeeping_status) VALUES
( 1, 'Vacant', 'Ready'),
( 1, 'Booked', 'Ready'),
( 2, 'Vacant', 'Ready');

-- Employees
INSERT INTO employee (first_name, last_name, emp_position, shift, emp_status) VALUES
('Carla', 'Reyes', 'frontdesk', 'Morning', 'Active'),
('Mark', 'Villanueva', 'housekeeping', 'Afternoon', 'Active'),
('Susan', 'Lim', 'admin', 'Morning', 'Active'),
('Rico', 'Lopez', 'housekeeping', 'Night', 'Leave-sick');

-- Housekeeping Items
INSERT INTO housekeeping_item (item_name, cost_per_unit, current_stock, minimum_stock, max_stock_storage) VALUES
('Towel', 150.00, 40, 10, 100),
('Soap', 20.00, 200, 50, 300),
('Shampoo', 35.00, 150, 30, 200),
('Toothpaste', 25.00, 100, 20, 150),
('Bedsheet', 500.00, 25, 10, 50);

-- Bookings
INSERT INTO booking (guest_id, room_id, booking_date, start_date, end_date) VALUES
(1, 2, '2025-11-01', '2025-11-03', '2025-11-05'),  -- Maria booked Room 2
(2, 3, '2025-11-05', '2025-11-06', '2025-11-08'),  -- John booked Room 3
(3, 1, '2025-11-08', '2025-11-09', '2025-11-10');  -- Akira booked Room 1

-- Payments
INSERT INTO payment (booking_id, amount_paid, payment_method, payment_date) VALUES
(1, 3000.00, 'Credit Card', '2025-11-01'),
(2, 5000.00, 'Cash', '2025-11-05'),
(3, 1500.00, 'Debit Card', '2025-11-08');

-- Guest Stay
INSERT INTO GuestStay (booking_id, employee_id, check_in_time_date, expected_check_out_time_date, actual_check_out_time_date, remarks) VALUES
(1, 1, '2025-11-03 14:00:00', '2025-11-05 12:00:00', '2025-11-05 11:30:00', 'Smooth check-out'),
(2, 1, '2025-11-06 15:00:00', '2025-11-08 12:00:00', NULL, 'Guest still checked in'),
(3, 1, '2025-11-09 13:30:00', '2025-11-10 12:00:00', '2025-11-10 12:05:00', 'On-time check-out');

-- Housekeeping Item Issuance
INSERT INTO housekeeping_item_issuance (housekeeping_item_id, employee_id, quantity_issued, issuance_status, remarks) VALUES
(1, 2, 5, 'issued', 'Issued for Room 2 cleaning'),
(2, 2, 10, 'issued', 'Daily cleaning supplies'),
(3, 4, 8, 'pending', 'Pending approval for restocking'),
(5, 2, 2, 'issued', 'Bedsheets replacement for Room 1');

