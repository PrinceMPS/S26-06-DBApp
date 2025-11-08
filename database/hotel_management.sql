CREATE DATABASE Hotel_Management;
USE Hotel_Management;


CREATE TABLE user_account(
	user_id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(20) NOT NULL UNIQUE,
    user_password VARCHAR(30) NOT NULL,
    user_role ENUM('Frontdesk','Admin','Housekeeping','Guest'),
    
	PRIMARY KEY (user_id)
    
    
    );
CREATE TABLE guest(
    guest_id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    contact_number INT NOT NULL,
    email_address VARCHAR(35) NOT NULL,
    nationality VARCHAR(20) NOT NULL,
    PRIMARY KEY (guest_id),
    FOREIGN KEY (user_id) REFERENCES user_account(user_id)
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
    user_id INT NOT NULL,
	first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    emp_position ENUM ('frontdesk','housekeeping','admin') NOT NULL,
    shift ENUM('Morning', 'Afternoon', 'Night') NOT NULL,
    emp_status ENUM('Active', 'Leave-vacation', 'Leave-sick', 'Leave-maternity') DEFAULT 'Active' NOT NULL,
    PRIMARY KEY (employee_id),
    FOREIGN KEY (user_id) REFERENCES user_account(user_id)
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

