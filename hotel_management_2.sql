CREATE DATABASE Hotel_Management_2;
USE Hotel_Management_2;

CREATE TABLE guest(
    guest_id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    contact_number INT NOT NULL,
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
    room_type INT NOT NULL,
    availability_status ENUM('Booked', 'Vacant') DEFAULT 'Vacant' NOT NULL,
    housekeeping_status ENUM('For Cleaning', 'Under Maintainance', 'Ready') DEFAULT 'Ready' NOT NULL,
    room_type_id INT,
   
   -- Foreign Key
    FOREIGN KEY (room_type_id) REFERENCES roomtype(room_type_id)
);

CREATE TABLE employee(
    employee_id INT NOT NULL AUTO_INCREMENT,
	first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    position VARCHAR(10) NOT NULL,
    shift ENUM('Morning', 'Afternoon', 'Night') NOT NULL,
    emp_status ENUM('Active', 'Leave-vacation', 'Leave-sick', 'Leave-maternty') DEFAULT 'Active' NOT NULL,
    PRIMARY KEY (employee_id)
);

CREATE TABLE housekeeping_item(
    housekeeping_item_id INT NOT NULL AUTO_INCREMENT,
	item_name VARCHAR(20) NOT NULL,
    quantity INT NOT NULL,
    cost_per_unit INT NOT NULL,
    stock INT NOT NULL,
	max_stock_storage VARCHAR(20) NOT NULL,
    PRIMARY KEY (housekeeping_item_id)
);

CREATE TABLE booking (
    booking_id INT NOT NULL AUTO_INCREMENT,
    guest_id INT NOT NULL,
    room_id INT NOT NULL,
    booking_date DATE NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    total_amount_topay DECIMAL(10,2),
    
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

CREATE TABLE check_in_out (
    transaction_id INT NOT NULL AUTO_INCREMENT,
    booking_id INT NOT NULL,
    check_in_time_date DATETIME,
    check_out_time_date DATETIME,
    remarks VARCHAR(100),

    PRIMARY KEY (transaction_id),
    
    -- Foreign Keys
    FOREIGN KEY (booking_id) REFERENCES booking(booking_id)
	
);
ALTER TABLE check_in_out
ADD COLUMN employee_id INT NOT NULL AFTER booking_id,
ADD FOREIGN KEY (employee_id) REFERENCES employee(employee_id);


CREATE TABLE housekeeping_item_issuance (
    issuance_id INT NOT NULL AUTO_INCREMENT,
	housekeeping_item_id  INT NOT NULL,
    employee_id INT NOT NULL,
    quantity_issued INT NOT NULL,
    date_issued DATETIME DEFAULT CURRENT_TIMESTAMP,
    remarks TEXT,

    PRIMARY KEY (issuance_id),

    -- Foreign Keys
    FOREIGN KEY (housekeeping_item_id ) REFERENCES housekeeping_item(housekeeping_item_id ),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
);

RENAME TABLE booking TO reservation;
RENAME TABLE check_in_out TO booking;
