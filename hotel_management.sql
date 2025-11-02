CREATE DATABASE Hotel_Management;
USE Hotel_Management;

CREATE TABLE guest(
    guest_id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    contact_number INT NOT NULL,
    email_address VARCHAR(35) NOT NULL,
    nationality VARCHAR(20) NOT NULL,
    age INT NOT NULL,
    PRIMARY KEY (guest_id)
);

CREATE TABLE room(
    room_id INT NOT NULL,
    room_type INT NOT NULL,
    availability ENUM('Booked', 'Vacant') DEFAULT 'Vacant' NOT NULL,
    housekeeping ENUM('For Cleaning', 'Under Maintainance', 'Ready') DEFAULT 'Ready' NOT NULL,
    capacity INT NOT NULL,
    rate INT NOT NULL,
    PRIMARY KEY (room_id)
);

CREATE TABLE employee(
    employee_id INT NOT NULL AUTO_INCREMENT,
	first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    position VARCHAR(10) NOT NULL,
    shift INT NOT NULL,
    emp_status ENUM('Active', 'Leave-vacation', 'Leave-sick', 'Leave-maternty') DEFAULT 'Active' NOT NULL,
    PRIMARY KEY (employee_id)
);

CREATE TABLE housekeeping(
    housekeeping_id INT NOT NULL AUTO_INCREMENT,
	item_name VARCHAR(20) NOT NULL,
    quantity INT NOT NULL,
    cost INT NOT NULL,
    stock INT NOT NULL,
    max VARCHAR(20) NOT NULL,
    PRIMARY KEY (housekeeping_id)
);

CREATE TABLE booking (
    booking_id INT NOT NULL AUTO_INCREMENT,
    guest_id INT NOT NULL,
    room_id INT NOT NULL,
    employee_id INT NOT NULL,
    booking_date DATE NOT NULL,
    
    PRIMARY KEY (booking_id),
    
    -- Foreign Keys
    FOREIGN KEY (guest_id) REFERENCES guest(guest_id),
    FOREIGN KEY (room_id) REFERENCES room(room_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
);

CREATE TABLE payment (
    payment_id INT NOT NULL AUTO_INCREMENT,
    guest_id INT NOT NULL,
    booking_id INT NOT NULL,
    amount_paid DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(20) NOT NULL,
    payment_date DATE NOT NULL,
    
    PRIMARY KEY (payment_id),
    
    -- Foreign Keys
    FOREIGN KEY (guest_id) REFERENCES guest(guest_id),
    FOREIGN KEY (booking_id) REFERENCES booking(booking_id)
);

CREATE TABLE check_in_out (
    transaction_id INT NOT NULL AUTO_INCREMENT,
    booking_id INT NOT NULL,
    check_in_date TIMESTAMP,
    check_out_date TIMESTAMP,
    room_status VARCHAR(15) NOT NULL,   
    remarks VARCHAR(100),

    PRIMARY KEY (transaction_id),
    
    -- Foreign Keys
    FOREIGN KEY (booking_id) REFERENCES booking(booking_id)
	
);

CREATE TABLE housekeeping_issuance (
    issuance_id INT NOT NULL AUTO_INCREMENT,
    housekeeping_id INT NOT NULL,
    room_id INT NOT NULL,
    employee_id INT NOT NULL,
    quantity_issued INT NOT NULL,
    date_issued DATETIME DEFAULT CURRENT_TIMESTAMP,
    remarks TEXT,

    PRIMARY KEY (issuance_id),

    -- Foreign Keys
    FOREIGN KEY (housekeeping_id) REFERENCES housekeeping(housekeeping_id),
    FOREIGN KEY (room_id) REFERENCES room(room_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id)
);
