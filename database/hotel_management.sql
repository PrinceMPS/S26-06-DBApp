CREATE DATABASE Hotel_Management;
USE Hotel_Management;


CREATE TABLE guest(
    guest_id INT NOT NULL AUTO_INCREMENT,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    contact_number VARCHAR(15) NOT NULL,
    email_address VARCHAR(35) NOT NULL,
    nationality VARCHAR(20) DEFAULT 'Filipino',
    PRIMARY KEY (guest_id)
) AUTO_INCREMENT = 1001;

CREATE TABLE RoomType (
    room_type_id INT PRIMARY KEY,
    type_name VARCHAR(50) NOT NULL,
    rate_per_type DECIMAL(10,2) NOT NULL,
    capacity INT NOT NULL
);
 
CREATE TABLE room(
    room_id INT PRIMARY KEY,
    room_type_id INT NOT NULL,
    availability_status ENUM('Occupied', 'Reserved', 'Vacant') DEFAULT 'Vacant' NOT NULL,
   
   -- Foreign Key
    FOREIGN KEY (room_type_id) REFERENCES roomtype(room_type_id)
);

CREATE TABLE employee(
    employee_id INT NOT NULL AUTO_INCREMENT ,
	first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    emp_position ENUM ('Front Desk','Housekeeping','Admin') NOT NULL,
    emp_status ENUM('Active', 'Leave-vacation', 'Leave-sick', 'Leave-maternity') DEFAULT 'Active' NOT NULL,
    PRIMARY KEY (employee_id)
);

CREATE TABLE housekeeping_item(
    housekeeping_item_id INT NOT NULL AUTO_INCREMENT,
	item_name VARCHAR(20) NOT NULL UNIQUE,
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
    payment_status ENUM('Paid','Pending') NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    
    PRIMARY KEY (booking_id),
    
    -- Foreign Keys
    FOREIGN KEY (guest_id) REFERENCES guest(guest_id),
    FOREIGN KEY (room_id) REFERENCES room(room_id)
);

CREATE TABLE payment (
    payment_id INT NOT NULL AUTO_INCREMENT,
    booking_id INT NOT NULL UNIQUE,
    amount_paid DECIMAL(10,2) NOT NULL,
    payment_method ENUM('Cash','Credit Card','Debit Card') NOT NULL,
    payment_datetime DATETIME NOT NULL,
    
    PRIMARY KEY (payment_id),
    
    -- Foreign Keys
    FOREIGN KEY (booking_id) REFERENCES booking(booking_id)
);

CREATE TABLE GuestStay(
    transaction_id INT NOT NULL AUTO_INCREMENT,
    booking_id INT NOT NULL UNIQUE,
    checkin_employee_id INT NOT NULL,
    checkout_employee_id INT,
    check_in_time_date DATETIME,
    expected_check_out_time_date DATETIME,
    actual_check_out_time_date DATETIME,
    remarks VARCHAR(100),

    PRIMARY KEY (transaction_id),
    
    -- Foreign Keys
    FOREIGN KEY (booking_id) REFERENCES booking(booking_id),
    FOREIGN KEY (checkin_employee_id) REFERENCES employee(employee_id),
    FOREIGN KEY (checkout_employee_id) REFERENCES employee(employee_id)
);

CREATE TABLE housekeeping_item_issuance (
    issuance_id INT NOT NULL AUTO_INCREMENT,
    housekeeping_item_id INT NOT NULL,
    employee_id INT NOT NULL,
    issuer_id INT NOT NULL,
    quantity_issued INT NOT NULL,
    date_issued DATETIME DEFAULT CURRENT_TIMESTAMP,
    remarks TEXT NULL,

    PRIMARY KEY (issuance_id),

    -- Foreign Keys
    FOREIGN KEY (housekeeping_item_id) REFERENCES housekeeping_item(housekeeping_item_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id),
    FOREIGN KEY (issuer_id) REFERENCES employee(employee_id)
);


-- Guests
INSERT INTO guest (first_name, last_name, contact_number, email_address) VALUES
('Juan', 'Dela Cruz', '09171234567', 'juan.delacruz@example.com'),
('Maria', 'Santos', '09281234568', 'maria.santos@example.com'),
('Jose', 'Reyes', '09091234569', 'jose.reyes@example.com'),
('Ana', 'Lopez', '09351234570', 'ana.lopez@example.com'),
('Pedro', 'Garcia', '09181234571', 'pedro.garcia@example.com'),
('Carmen', 'Mendoza', '09291234572', 'carmen.mendoza@example.com'),
('Ramon', 'Castro', '09451234573', 'ramon.castro@example.com'),
('Lucia', 'Torres', '09191234574', 'lucia.torres@example.com'),
('Diego', 'Bautista', '09301234575', 'diego.bautista@example.com'),
('Elena', 'Cruz', '09221234576', 'elena.cruz@example.com'),
('Mark', 'Villanueva', '09170010001', 'mark.villanueva@example.com'),
('Jenny', 'Ramirez', '09280010002', 'jenny.ramirez@example.com'),
('Leo', 'Domingo', '09350010003', 'leo.domingo@example.com'),
('Faith', 'Soriano', '09450010004', 'faith.soriano@example.com'),
('John', 'Aquino', '09170010005', 'john.aquino@example.com'),
('Bianca', 'Panganiban', '09280010006', 'bianca.panganiban@example.com'),
('Arthur', 'Manalo', '09350010007', 'arthur.manalo@example.com'),
('Shiela', 'Vergara', '09450010008', 'shiela.vergara@example.com'),
('Adrian', 'Salazar', '09170010009', 'adrian.salazar@example.com'),
('Jasmine', 'Valdez', '09280010010', 'jasmine.valdez@example.com'),
('Calvin', 'Navarro', '09350010011', 'calvin.navarro@example.com'),
('Denise', 'Mercado', '09450010012', 'denise.mercado@example.com'),
('Kevin', 'Fuentes', '09170010013', 'kevin.fuentes@example.com'),
('Mika', 'Roxas', '09280010014', 'mika.roxas@example.com'),
('Nathan', 'Padilla', '09350010015', 'nathan.padilla@example.com'),
('Rhea', 'Sarmiento', '09450010016', 'rhea.sarmiento@example.com'),
('Felix', 'Rubio', '09170010017', 'felix.rubio@example.com'),
('Irish', 'Villar', '09280010018', 'irish.villar@example.com'),
('Gabriel', 'Lim', '09350010019', 'gabriel.lim@example.com'),
('Nicole', 'Uy', '09450010020', 'nicole.uy@example.com'),
('Victor', 'Chavez', '09170010021', 'victor.chavez@example.com'),
('Angela', 'Fabian', '09280010022', 'angela.fabian@example.com'),
('Marc', 'Santos', '09350010023', 'marc.santos2@example.com'),
('Kate', 'Jimenez', '09450010024', 'kate.jimenez@example.com'),
('Joshua', 'Tan', '09170010025', 'joshua.tan@example.com'),
('Bea', 'Go', '09280010026', 'bea.go@example.com'),
('Martin', 'Zabala', '09350010027', 'martin.zabala@example.com'),
('Hannah', 'Ferrer', '09450010028', 'hannah.ferrer@example.com'),
('Ronald', 'Silva', '09170010029', 'ronald.silva@example.com'),
('Louise', 'Cabrera', '09280010030', 'louise.cabrera@example.com'),
('Vince', 'Reyes', '09350010031', 'vince.reyes@example.com'),
('Andrea', 'Solis', '09450010032', 'andrea.solis@example.com'),
('Brandon', 'Santiago', '09170010033', 'brandon.santiago@example.com'),
('Elaine', 'Ramos', '09280010034', 'elaine.ramos@example.com'),
('Harold', 'Miranda', '09350010035', 'harold.miranda@example.com'),
('Kyla', 'Rivera', '09450010036', 'kyla.rivera@example.com'),
('Ricky', 'Ocampo', '09170010037', 'ricky.ocampo@example.com'),
('Patricia', 'Chua', '09280010038', 'patricia.chua@example.com'),
('Joel', 'Pineda', '09350010039', 'joel.pineda@example.com'),
('Melanie', 'Gonzales', '09450010040', 'melanie.gonzales@example.com'),
('Ivan', 'Aguila', '09170010041', 'ivan.aguila@example.com'),
('Layla', 'Bartolome', '09280010042', 'layla.bartolome@example.com'),
('Cyrus', 'Montenegro', '09350010043', 'cyrus.montenegro@example.com'),
('Toni', 'Ortega', '09450010044', 'toni.ortega@example.com'),
('Darren', 'Villamor', '09170010045', 'darren.villamor@example.com'),
('Paula', 'Espino', '09280010046', 'paula.espino@example.com'),
('Henry', 'Villena', '09350010047', 'henry.villena@example.com'),
('Ella', 'Pascual', '09450010048', 'ella.pascual@example.com'),
('Marco', 'Lorenzo', '09170010049', 'marco.lorenzo@example.com'),
('Clara', 'Francisco', '09280010050', 'clara.francisco@example.com'),
('Xander', 'Beltran', '09350010051', 'xander.beltran@example.com'),
('Leah', 'De Vera', '09450010052', 'leah.devera@example.com'),
('Owen', 'Yap', '09170010053', 'owen.yap@example.com'),
('Fiona', 'Chan', '09280010054', 'fiona.chan@example.com'),
('Zach', 'Gatdula', '09350010055', 'zach.gatdula@example.com'),
('Trisha', 'Nicolas', '09450010056', 'trisha.nicolas@example.com'),
('Dominic', 'Reyes', '09170010057', 'dominic.reyes@example.com'),
('Sheena', 'Salinas', '09280010058', 'sheena.salinas@example.com'),
('Ernest', 'Palma', '09350010059', 'ernest.palma@example.com'),
('Mae', 'Jacinto', '09450010060', 'mae.jacinto@example.com'),
('Kyle', 'Lagman', '09170010061', 'kyle.lagman@example.com'),
('Joanne', 'Licup', '09280010062', 'joanne.licup@example.com'),
('Harvey', 'Basa', '09350010063', 'harvey.basa@example.com'),
('Kristel', 'Benitez', '09450010064', 'kristel.benitez@example.com'),
('Wilson', 'Catapang', '09170010065', 'wilson.catapang@example.com'),
('Alyssa', 'Del Mundo', '09280010066', 'alyssa.delmundo@example.com'),
('Ralph', 'Escobar', '09350010067', 'ralph.escobar@example.com'),
('Camille', 'Fabella', '09450010068', 'camille.fabella@example.com'),
('Edgar', 'Francisco', '09170010069', 'edgar.francisco@example.com'),
('Mara', 'Gatchalian', '09280010070', 'mara.gatchalian@example.com'),
('Jerome', 'Hernandez', '09350010071', 'jerome.hernandez@example.com'),
('Rose', 'Ignacio', '09450010072', 'rose.ignacio@example.com'),
('Paul', 'Javier', '09170010073', 'paul.javier@example.com'),
('Gwen', 'Kayanan', '09280010074', 'gwen.kayanan@example.com'),
('Cedric', 'Laxamana', '09350010075', 'cedric.laxamana@example.com'),
('Aira', 'Macapagal', '09450010076', 'aira.macapagal@example.com'),
('Noel', 'Nery', '09170010077', 'noel.nery@example.com'),
('Pearl', 'Ong', '09280010078', 'pearl.ong@example.com'),
('Francis', 'Ponce', '09350010079', 'francis.ponce@example.com'),
('Janelle', 'Quezada', '09450010080', 'janelle.quezada@example.com'),
('Alvin', 'Rosales', '09170010081', 'alvin.rosales@example.com'),
('Cheska', 'San Juan', '09280010082', 'cheska.sanjuan@example.com'),
('Dylan', 'Tiongson', '09350010083', 'dylan.tiongson@example.com'),
('Rochelle', 'Ubaldo', '09450010084', 'rochelle.ubaldo@example.com'),
('Jeff', 'Velasco', '09170010085', 'jeff.velasco@example.com'),
('Kirsten', 'Wenceslao', '09280010086', 'kirsten.wenceslao@example.com'),
('Lawrence', 'Yumul', '09350010087', 'lawrence.yumul@example.com'),
('Nina', 'Zarate', '09450010088', 'nina.zarate@example.com'),
('Gio', 'Alcantara', '09170010089', 'gio.alcantara@example.com'),
('Sofia', 'Balagtas', '09280010090', 'sofia.balagtas@example.com'),
('Trevor', 'Callanta', '09350010091', 'trevor.callanta@example.com'),
('Denisse', 'De Chavez', '09450010092', 'denisse.dechavez@example.com'),
('Allan', 'Enriquez', '09170010093', 'allan.enriquez@example.com'),
('Lara', 'Flores', '09280010094', 'lara.flores@example.com'),
('Jude', 'Guerrero', '09350010095', 'jude.guerrero@example.com'),
('Megan', 'Hizon', '09450010096', 'megan.hizon@example.com'),
('Rey', 'Illustre', '09170010097', 'rey.illustre@example.com'),
('Phoebe', 'Joaquin', '09280010098', 'phoebe.joaquin@example.com'),
('Chris', 'Katigbak', '09350010099', 'chris.katigbak@example.com'),
('Aileen', 'Legaspi', '09450010100', 'aileen.legaspi@example.com');


-- Room Types
INSERT INTO RoomType (room_type_id, type_name, rate_per_type, capacity) VALUES
(1, 'Single Room', 1500.00, 1),
(2, 'Double Room', 2500.00, 2),
(3, 'Deluxe Room', 3500.00, 3),
(4, 'Suite', 5000.00, 4);

-- Rooms
INSERT INTO room (room_id, room_type_id, availability_status) VALUES
(501, 1, 'Vacant'),
(502, 2, 'Vacant'),
(503, 3, 'Vacant'),
(504, 4, 'Vacant'),
(505, 1, 'Vacant'),
(506, 2, 'Vacant'),
(507, 3, 'Vacant'),
(508, 4, 'Vacant'),
(509, 1, 'Vacant'),
(510, 2, 'Vacant'),
(511, 3, 'Vacant'),
(512, 4, 'Vacant'),
(513, 1, 'Vacant'),
(514, 2, 'Vacant'),
(515, 3, 'Vacant'),
(516, 4, 'Vacant'),
(517, 1, 'Vacant'),
(518, 2, 'Vacant'),
(519, 3, 'Vacant'),
(520, 4, 'Vacant'),
(601, 1, 'Vacant'),
(602, 2, 'Vacant'),
(603, 3, 'Vacant'),
(604, 4, 'Vacant'),
(605, 1, 'Vacant'),
(606, 2, 'Vacant'),
(607, 3, 'Vacant'),
(608, 4, 'Vacant'),
(609, 1, 'Vacant'),
(610, 2, 'Vacant'),
(611, 3, 'Vacant'),
(612, 4, 'Vacant'),
(613, 1, 'Vacant'),
(614, 2, 'Vacant'),
(615, 3, 'Vacant'),
(616, 4, 'Vacant'),
(617, 1, 'Vacant'),
(618, 2, 'Vacant'),
(619, 3, 'Vacant'),
(620, 4, 'Vacant'),
(701, 1, 'Vacant'),
(702, 2, 'Vacant'),
(703, 3, 'Vacant'),
(704, 4, 'Vacant'),
(705, 1, 'Vacant'),
(706, 2, 'Vacant'),
(707, 3, 'Vacant'),
(708, 4, 'Vacant'),
(709, 1, 'Vacant'),
(710, 2, 'Vacant'),
(711, 3, 'Vacant'),
(712, 4, 'Vacant'),
(713, 1, 'Vacant'),
(714, 2, 'Vacant'),
(715, 3, 'Vacant'),
(716, 4, 'Vacant'),
(717, 1, 'Vacant'),
(718, 2, 'Vacant'),
(719, 3, 'Vacant'),
(720, 4, 'Vacant'),
(801, 1, 'Vacant'),
(802, 2, 'Vacant'),
(803, 3, 'Vacant'),
(804, 4, 'Vacant'),
(805, 1, 'Vacant'),
(806, 2, 'Vacant'),
(807, 3, 'Vacant'),
(808, 4, 'Vacant'),
(809, 1, 'Vacant'),
(810, 2, 'Vacant'),
(811, 3, 'Vacant'),
(812, 4, 'Vacant'),
(813, 1, 'Vacant'),
(814, 2, 'Vacant'),
(815, 3, 'Vacant'),
(816, 4, 'Vacant'),
(817, 1, 'Vacant'),
(818, 2, 'Vacant'),
(819, 3, 'Vacant'),
(820, 4, 'Vacant'),
(901, 1, 'Vacant'),
(902, 2, 'Vacant'),
(903, 3, 'Vacant'),
(904, 4, 'Vacant'),
(905, 1, 'Vacant'),
(906, 2, 'Vacant'),
(907, 3, 'Vacant'),
(908, 4, 'Vacant'),
(909, 1, 'Vacant'),
(910, 2, 'Vacant'),
(911, 3, 'Vacant'),
(912, 4, 'Vacant'),
(913, 1, 'Vacant'),
(914, 2, 'Vacant'),
(915, 3, 'Vacant'),
(916, 4, 'Vacant'),
(917, 1, 'Vacant'),
(918, 2, 'Vacant'),
(919, 3, 'Vacant'),
(920, 4, 'Vacant'),
(1001, 1, 'Vacant'),
(1002, 2, 'Vacant'),
(1003, 3, 'Vacant'),
(1004, 4, 'Vacant'),
(1005, 1, 'Vacant'),
(1006, 2, 'Vacant'),
(1007, 3, 'Vacant'),
(1008, 4, 'Vacant'),
(1009, 1, 'Vacant'),
(1010, 2, 'Vacant'),
(1011, 3, 'Vacant'),
(1012, 4, 'Vacant'),
(1013, 1, 'Vacant'),
(1014, 2, 'Vacant'),
(1015, 3, 'Vacant'),
(1016, 4, 'Vacant'),
(1017, 1, 'Vacant'),
(1018, 2, 'Vacant'),
(1019, 3, 'Vacant'),
(1020, 4, 'Vacant'),
(1101, 1, 'Vacant'),
(1102, 2, 'Vacant'),
(1103, 3, 'Vacant'),
(1104, 4, 'Vacant'),
(1105, 1, 'Vacant'),
(1106, 2, 'Vacant'),
(1107, 3, 'Vacant'),
(1108, 4, 'Vacant'),
(1109, 1, 'Vacant'),
(1110, 2, 'Vacant'),
(1111, 3, 'Vacant'),
(1112, 4, 'Vacant'),
(1113, 1, 'Vacant'),
(1114, 2, 'Vacant'),
(1115, 3, 'Vacant'),
(1116, 4, 'Vacant'),
(1117, 1, 'Vacant'),
(1118, 2, 'Vacant'),
(1119, 3, 'Vacant'),
(1120, 4, 'Vacant'),
(1201, 1, 'Vacant'),
(1202, 2, 'Vacant'),
(1203, 3, 'Vacant'),
(1204, 4, 'Vacant'),
(1205, 1, 'Vacant'),
(1206, 2, 'Vacant'),
(1207, 3, 'Vacant'),
(1208, 4, 'Vacant'),
(1209, 1, 'Vacant'),
(1210, 2, 'Vacant'),
(1211, 3, 'Vacant'),
(1212, 4, 'Vacant'),
(1213, 1, 'Vacant'),
(1214, 2, 'Vacant'),
(1215, 3, 'Vacant'),
(1216, 4, 'Vacant'),
(1217, 1, 'Vacant'),
(1218, 2, 'Vacant'),
(1219, 3, 'Vacant'),
(1220, 4, 'Vacant'),
(1301, 1, 'Vacant'),
(1302, 2, 'Vacant'),
(1303, 3, 'Vacant'),
(1304, 4, 'Vacant'),
(1305, 1, 'Vacant'),
(1306, 2, 'Vacant'),
(1307, 3, 'Vacant'),
(1308, 4, 'Vacant'),
(1309, 1, 'Vacant'),
(1310, 2, 'Vacant'),
(1311, 3, 'Vacant'),
(1312, 4, 'Vacant'),
(1313, 1, 'Vacant'),
(1314, 2, 'Vacant'),
(1315, 3, 'Vacant'),
(1316, 4, 'Vacant'),
(1317, 1, 'Vacant'),
(1318, 2, 'Vacant'),
(1319, 3, 'Vacant'),
(1320, 4, 'Vacant'),
(1401, 1, 'Vacant'),
(1402, 2, 'Vacant'),
(1403, 3, 'Vacant'),
(1404, 4, 'Vacant'),
(1405, 1, 'Vacant'),
(1406, 2, 'Vacant'),
(1407, 3, 'Vacant'),
(1408, 4, 'Vacant'),
(1409, 1, 'Vacant'),
(1410, 2, 'Vacant'),
(1411, 3, 'Vacant'),
(1412, 4, 'Vacant'),
(1413, 1, 'Vacant'),
(1414, 2, 'Vacant'),
(1415, 3, 'Vacant'),
(1416, 4, 'Vacant'),
(1417, 1, 'Vacant'),
(1418, 2, 'Vacant'),
(1419, 3, 'Vacant'),
(1420, 4, 'Vacant'),
(1501, 1, 'Vacant'),
(1502, 2, 'Vacant'),
(1503, 3, 'Vacant'),
(1504, 4, 'Vacant'),
(1505, 1, 'Vacant'),
(1506, 2, 'Vacant'),
(1507, 3, 'Vacant'),
(1508, 4, 'Vacant'),
(1509, 1, 'Vacant'),
(1510, 2, 'Vacant'),
(1511, 3, 'Vacant'),
(1512, 4, 'Vacant'),
(1513, 1, 'Vacant'),
(1514, 2, 'Vacant'),
(1515, 3, 'Vacant'),
(1516, 4, 'Vacant'),
(1517, 1, 'Vacant'),
(1518, 2, 'Vacant'),
(1519, 3, 'Vacant'),
(1520, 4, 'Vacant'),
(1601, 1, 'Vacant'),
(1602, 2, 'Vacant'),
(1603, 3, 'Vacant'),
(1604, 4, 'Vacant'),
(1605, 1, 'Vacant'),
(1606, 2, 'Vacant'),
(1607, 3, 'Vacant'),
(1608, 4, 'Vacant'),
(1609, 1, 'Vacant'),
(1610, 2, 'Vacant'),
(1611, 3, 'Vacant'),
(1612, 4, 'Vacant'),
(1613, 1, 'Vacant'),
(1614, 2, 'Vacant'),
(1615, 3, 'Vacant'),
(1616, 4, 'Vacant'),
(1617, 1, 'Vacant'),
(1618, 2, 'Vacant'),
(1619, 3, 'Vacant'),
(1620, 4, 'Vacant'),
(1701, 1, 'Vacant'),
(1702, 2, 'Vacant'),
(1703, 3, 'Vacant'),
(1704, 4, 'Vacant'),
(1705, 1, 'Vacant'),
(1706, 2, 'Vacant'),
(1707, 3, 'Vacant'),
(1708, 4, 'Vacant'),
(1709, 1, 'Vacant'),
(1710, 2, 'Vacant'),
(1711, 3, 'Vacant'),
(1712, 4, 'Vacant'),
(1713, 1, 'Vacant'),
(1714, 2, 'Vacant'),
(1715, 3, 'Vacant'),
(1716, 4, 'Vacant'),
(1717, 1, 'Vacant'),
(1718, 2, 'Vacant'),
(1719, 3, 'Vacant'),
(1720, 4, 'Vacant'),
(1801, 1, 'Vacant'),
(1802, 2, 'Vacant'),
(1803, 3, 'Vacant'),
(1804, 4, 'Vacant'),
(1805, 1, 'Vacant'),
(1806, 2, 'Vacant'),
(1807, 3, 'Vacant'),
(1808, 4, 'Vacant'),
(1809, 1, 'Vacant'),
(1810, 2, 'Vacant'),
(1811, 3, 'Vacant'),
(1812, 4, 'Vacant'),
(1813, 1, 'Vacant'),
(1814, 2, 'Vacant'),
(1815, 3, 'Vacant'),
(1816, 4, 'Vacant'),
(1817, 1, 'Vacant'),
(1818, 2, 'Vacant'),
(1819, 3, 'Vacant'),
(1820, 4, 'Vacant'),
(1901, 1, 'Vacant'),
(1902, 2, 'Vacant'),
(1903, 3, 'Vacant'),
(1904, 4, 'Vacant'),
(1905, 1, 'Vacant'),
(1906, 2, 'Vacant'),
(1907, 3, 'Vacant'),
(1908, 4, 'Vacant'),
(1909, 1, 'Vacant'),
(1910, 2, 'Vacant'),
(1911, 3, 'Vacant'),
(1912, 4, 'Vacant'),
(1913, 1, 'Vacant'),
(1914, 2, 'Vacant'),
(1915, 3, 'Vacant'),
(1916, 4, 'Vacant'),
(1917, 1, 'Vacant'),
(1918, 2, 'Vacant'),
(1919, 3, 'Vacant'),
(1920, 4, 'Vacant'),
(2001, 1, 'Vacant'),
(2002, 2, 'Vacant'),
(2003, 3, 'Vacant'),
(2004, 4, 'Vacant'),
(2005, 1, 'Vacant'),
(2006, 2, 'Vacant'),
(2007, 3, 'Vacant'),
(2008, 4, 'Vacant'),
(2009, 1, 'Vacant'),
(2010, 2, 'Vacant'),
(2011, 3, 'Vacant'),
(2012, 4, 'Vacant'),
(2013, 1, 'Vacant'),
(2014, 2, 'Vacant'),
(2015, 3, 'Vacant'),
(2016, 4, 'Vacant'),
(2017, 1, 'Vacant'),
(2018, 2, 'Vacant'),
(2019, 3, 'Vacant'),
(2020, 4, 'Vacant');


-- Employees
INSERT INTO employee (first_name, last_name, emp_position, emp_status) VALUES
('Carla', 'Reyes', 'Front Desk', 'Active'),
('Mark', 'Villanueva', 'Housekeeping', 'Active'),
('Susan', 'Lim', 'Admin', 'Active'),
('Rico', 'Lopez', 'Housekeeping', 'Leave-sick'),
('Anna', 'Torres', 'Front Desk', 'Active'),
('James', 'Gomez', 'Housekeeping', 'Leave-vacation'),
('Liza', 'Santos', 'Admin', 'Leave-sick'),
('Marie', 'Diaz', 'Front Desk', 'Leave-maternity'),
('Maria', 'Cruz', 'Housekeeping', 'Active'),
('John', 'Reyes', 'Admin', 'Leave-vacation'),
('Nina', 'Valdez', 'Front Desk', 'Leave-sick'),
('Carla', 'Fernandez', 'Housekeeping', 'Leave-maternity'),
('Elaine', 'Morales', 'Admin', 'Active'),
('Victor', 'Alcantara', 'Front Desk', 'Leave-vacation'),
('Karol', 'Vigo', 'Front Desk', 'Active'),
('Daniel', 'Ortega', 'Front Desk', 'Active'),
('Patricia', 'Mendoza', 'Admin', 'Active'),
('Luis', 'Gatchalian', 'Housekeeping', 'Active'),
('Camille', 'Ramos', 'Front Desk', 'Leave-sick'),
('Ethan', 'Delgado', 'Admin', 'Leave-vacation');


/* =========================================
   2023-01 BOOKINGS / PAYMENTS / GUEST STAYS
   ========================================= */

-- Room types reminder:
-- type 1 (Single) = 1500
-- type 2 (Double) = 2500
-- type 3 (Deluxe) = 3500
-- type 4 (Suite)  = 5000

-- JAN Rooms used: 501(t1), 502(t2), 503(t3), 504(t4), 505(t1), 506(t2)

INSERT INTO booking (booking_id, guest_id, room_id, booking_date, payment_status, start_date, end_date) VALUES
    (1, 1001, 501, '2023-01-02', 'Paid', '2023-01-03', '2023-01-05'),  -- 2 nights, t1
    (2, 1002, 502, '2023-01-05', 'Paid', '2023-01-06', '2023-01-09'),  -- 3 nights, t2
    (3, 1003, 503, '2023-01-08', 'Paid', '2023-01-09', '2023-01-13'),  -- 4 nights, t3
    (4, 1004, 504, '2023-01-10', 'Paid', '2023-01-11', '2023-01-13'),  -- 2 nights, t4
    (5, 1005, 505, '2023-01-15', 'Paid', '2023-01-16', '2023-01-19'),  -- 3 nights, t1
    (6, 1006, 506, '2023-01-20', 'Paid', '2023-01-21', '2023-01-25');  -- 4 nights, t2

INSERT INTO payment (payment_id, booking_id, amount_paid, payment_method, payment_datetime) VALUES
    (1, 1,  3000.00,  'Cash',        '2023-01-02 10:00:00'),  -- 1500 * 2
    (2, 2,  7500.00,  'Credit Card', '2023-01-05 10:00:00'),  -- 2500 * 3
    (3, 3, 14000.00,  'Debit Card',  '2023-01-08 10:00:00'),  -- 3500 * 4
    (4, 4, 10000.00,  'Cash',        '2023-01-10 10:00:00'),  -- 5000 * 2
    (5, 5,  4500.00,  'Credit Card', '2023-01-15 10:00:00'),  -- 1500 * 3
    (6, 6, 10000.00,  'Debit Card',  '2023-01-20 10:00:00');  -- 2500 * 4

-- Allowed FD/Admin employees (by insert order):
-- FD: 1 Carla R, 5 Anna T, 8 Marie D, 11 Nina V, 14 Victor A, 15 Karol V, 16 Daniel O, 19 Camille R
-- Admin: 3 Susan L, 7 Liza S, 10 John R, 13 Elaine M, 17 Patricia M, 20 Ethan D

INSERT INTO GuestStay (
    transaction_id,
    booking_id,
    checkin_employee_id,
    checkout_employee_id,
    check_in_time_date,
    expected_check_out_time_date,
    actual_check_out_time_date,
    remarks
) VALUES
    (1, 1,  1,  3, '2023-01-03 15:00:00', '2023-01-05 12:00:00', '2023-01-05 12:00:00', 'On-time checkout.'),
    (2, 2,  5, 13, '2023-01-06 15:00:00', '2023-01-09 12:00:00', '2023-01-09 12:30:00', 'Slightly late checkout.'),
    (3, 3, 15, 17, '2023-01-09 15:00:00', '2023-01-13 12:00:00', '2023-01-13 13:15:00', 'Late checkout within 2 hours.'),
    (4, 4, 16, 10, '2023-01-11 15:00:00', '2023-01-13 12:00:00', '2023-01-13 12:00:00', 'On-time checkout.'),
    (5, 5, 11,  7, '2023-01-16 15:00:00', '2023-01-19 12:00:00', '2023-01-19 12:45:00', 'Slightly late checkout.'),
    (6, 6, 14, 20, '2023-01-21 15:00:00', '2023-01-25 12:00:00', '2023-01-25 12:00:00', 'On-time checkout.');


/* =========================================
   2023-02 BOOKINGS / PAYMENTS / GUEST STAYS
   ========================================= */

-- FEB Rooms used: 507(t3), 508(t4), 509(t1), 510(t2), 511(t3)

INSERT INTO booking (booking_id, guest_id, room_id, booking_date, payment_status, start_date, end_date) VALUES
    (7, 1007, 507, '2023-02-01', 'Paid', '2023-02-02', '2023-02-04'),  -- 2 nights, t3
    (8, 1008, 508, '2023-02-03', 'Paid', '2023-02-04', '2023-02-07'),  -- 3 nights, t4
    (9, 1009, 509, '2023-02-06', 'Paid', '2023-02-07', '2023-02-11'),  -- 4 nights, t1
    (10,1010, 510, '2023-02-10', 'Paid', '2023-02-11', '2023-02-13'),  -- 2 nights, t2
    (11,1011, 511, '2023-02-14', 'Paid', '2023-02-15', '2023-02-18');  -- 3 nights, t3

INSERT INTO payment (payment_id, booking_id, amount_paid, payment_method, payment_datetime) VALUES
    (7,  7,  7000.00,  'Cash',        '2023-02-01 10:00:00'),  -- 3500 * 2
    (8,  8, 15000.00,  'Credit Card', '2023-02-03 10:00:00'),  -- 5000 * 3
    (9,  9,  6000.00,  'Debit Card',  '2023-02-06 10:00:00'),  -- 1500 * 4
    (10,10,  5000.00,  'Cash',        '2023-02-10 10:00:00'),  -- 2500 * 2
    (11,11, 10500.00,  'Credit Card', '2023-02-14 10:00:00');  -- 3500 * 3

INSERT INTO GuestStay (
    transaction_id,
    booking_id,
    checkin_employee_id,
    checkout_employee_id,
    check_in_time_date,
    expected_check_out_time_date,
    actual_check_out_time_date,
    remarks
) VALUES
    (7,  7,  1,  3, '2023-02-02 15:00:00', '2023-02-04 12:00:00', '2023-02-04 12:00:00', 'On-time checkout.'),
    (8,  8,  5, 13, '2023-02-04 15:00:00', '2023-02-07 12:00:00', '2023-02-07 12:45:00', 'Slightly late checkout.'),
    (9,  9, 15, 17, '2023-02-07 15:00:00', '2023-02-11 12:00:00', '2023-02-11 13:30:00', 'Late checkout within 2 hours.'),
    (10,10, 16, 10, '2023-02-11 15:00:00', '2023-02-13 12:00:00', '2023-02-13 12:00:00', 'On-time checkout.'),
    (11,11, 11, 20, '2023-02-15 15:00:00', '2023-02-18 12:00:00', '2023-02-18 12:30:00', 'Slightly late checkout.');


/* =========================================
   2023-03 BOOKINGS / PAYMENTS / GUEST STAYS
   ========================================= */

-- MAR Rooms used: 512(t4), 513(t1), 514(t2), 515(t3), 516(t4)

INSERT INTO booking (booking_id, guest_id, room_id, booking_date, payment_status, start_date, end_date) VALUES
    (12,1012, 512, '2023-03-02', 'Paid', '2023-03-03', '2023-03-05'),  -- 2 nights, t4
    (13,1013, 513, '2023-03-05', 'Paid', '2023-03-06', '2023-03-09'),  -- 3 nights, t1
    (14,1014, 514, '2023-03-08', 'Paid', '2023-03-09', '2023-03-13'),  -- 4 nights, t2
    (15,1015, 515, '2023-03-12', 'Paid', '2023-03-13', '2023-03-15'),  -- 2 nights, t3
    (16,1016, 516, '2023-03-16', 'Paid', '2023-03-17', '2023-03-20');  -- 3 nights, t4

INSERT INTO payment (payment_id, booking_id, amount_paid, payment_method, payment_datetime) VALUES
    (12,12, 10000.00,  'Debit Card',  '2023-03-02 10:00:00'),  -- 5000 * 2
    (13,13,  4500.00,  'Cash',        '2023-03-05 10:00:00'),  -- 1500 * 3
    (14,14, 10000.00,  'Credit Card', '2023-03-08 10:00:00'),  -- 2500 * 4
    (15,15,  7000.00,  'Debit Card',  '2023-03-12 10:00:00'),  -- 3500 * 2
    (16,16, 15000.00,  'Cash',        '2023-03-16 10:00:00');  -- 5000 * 3


INSERT INTO GuestStay (
    transaction_id,
    booking_id,
    checkin_employee_id,
    checkout_employee_id,
    check_in_time_date,
    expected_check_out_time_date,
    actual_check_out_time_date,
    remarks
) VALUES
    (12,12,  1,  3, '2023-03-03 15:00:00', '2023-03-05 12:00:00', '2023-03-05 12:00:00', 'On-time checkout.'),
    (13,13,  5, 13, '2023-03-06 15:00:00', '2023-03-09 12:00:00', '2023-03-09 12:30:00', 'Slightly late checkout.'),
    (14,14, 15, 17, '2023-03-09 15:00:00', '2023-03-13 12:00:00', '2023-03-13 13:15:00', 'Late checkout within 2 hours.'),
    (15,15, 16, 10, '2023-03-13 15:00:00', '2023-03-15 12:00:00', '2023-03-15 12:00:00', 'On-time checkout.'),
    (16,16, 11, 20, '2023-03-17 15:00:00', '2023-03-20 12:00:00', '2023-03-20 12:45:00', 'Slightly late checkout.');


/* =========================================
   2023-04 BOOKINGS / PAYMENTS / GUEST STAYS
   ========================================= */

-- APR Rooms used: 517(t1), 518(t2), 519(t3), 520(t4), 601(t1)

INSERT INTO booking (booking_id, guest_id, room_id, booking_date, payment_status, start_date, end_date) VALUES
    (17, 1017, 517, '2023-04-01', 'Paid', '2023-04-02', '2023-04-04'),  -- 2 nights, t1
    (18, 1018, 518, '2023-04-05', 'Paid', '2023-04-06', '2023-04-09'),  -- 3 nights, t2
    (19, 1019, 519, '2023-04-10', 'Paid', '2023-04-11', '2023-04-15'),  -- 4 nights, t3
    (20, 1020, 520, '2023-04-16', 'Paid', '2023-04-17', '2023-04-19'),  -- 2 nights, t4
    (21, 1021, 601, '2023-04-20', 'Paid', '2023-04-21', '2023-04-24');  -- 3 nights, t1

-- Rates: t1=1500, t2=2500, t3=3500, t4=5000

INSERT INTO payment (payment_id, booking_id, amount_paid, payment_method, payment_datetime) VALUES
    (17, 17,  3000.00,  'Cash',        '2023-04-01 10:00:00'),  -- t1 * 2
    (18, 18,  7500.00,  'Credit Card', '2023-04-05 10:00:00'),  -- t2 * 3
    (19, 19, 14000.00,  'Debit Card',  '2023-04-10 10:00:00'),  -- t3 * 4
    (20, 20, 10000.00,  'Cash',        '2023-04-16 10:00:00'),  -- t4 * 2
    (21, 21,  4500.00,  'Credit Card', '2023-04-20 10:00:00');  -- t1 * 3

-- Allowed FD/Admin employees:
-- FD: 1,5,8,11,14,15,16,19  |  Admin: 3,7,10,13,17,20

INSERT INTO GuestStay (
    transaction_id,
    booking_id,
    checkin_employee_id,
    checkout_employee_id,
    check_in_time_date,
    expected_check_out_time_date,
    actual_check_out_time_date,
    remarks
) VALUES
    (17, 17,  1,  3, '2023-04-02 15:00:00', '2023-04-04 12:00:00', '2023-04-04 12:00:00', 'On-time checkout.'),
    (18, 18,  5, 13, '2023-04-06 15:00:00', '2023-04-09 12:00:00', '2023-04-09 12:30:00', 'Slightly late checkout.'),
    (19, 19, 15, 17, '2023-04-11 15:00:00', '2023-04-15 12:00:00', '2023-04-15 13:15:00', 'Late checkout within 2 hours.'),
    (20, 20, 16, 10, '2023-04-17 15:00:00', '2023-04-19 12:00:00', '2023-04-19 12:00:00', 'On-time checkout.'),
    (21, 21, 11, 20, '2023-04-21 15:00:00', '2023-04-24 12:00:00', '2023-04-24 12:45:00', 'Slightly late checkout.');


/* =========================================
   2023-05 BOOKINGS / PAYMENTS / GUEST STAYS
   ========================================= */

-- MAY Rooms used: 602(t2), 603(t3), 604(t4), 605(t1), 606(t2)

INSERT INTO booking (booking_id, guest_id, room_id, booking_date, payment_status, start_date, end_date) VALUES
    (22, 1022, 602, '2023-05-01', 'Paid', '2023-05-02', '2023-05-04'),  -- 2 nights, t2
    (23, 1023, 603, '2023-05-05', 'Paid', '2023-05-06', '2023-05-09'),  -- 3 nights, t3
    (24, 1024, 604, '2023-05-09', 'Paid', '2023-05-10', '2023-05-14'),  -- 4 nights, t4
    (25, 1025, 605, '2023-05-15', 'Paid', '2023-05-16', '2023-05-18'),  -- 2 nights, t1
    (26, 1026, 606, '2023-05-20', 'Paid', '2023-05-21', '2023-05-24');  -- 3 nights, t2

INSERT INTO payment (payment_id, booking_id, amount_paid, payment_method, payment_datetime) VALUES
    (22, 22,  5000.00,  'Debit Card',  '2023-05-01 10:00:00'),  -- 2500 * 2
    (23, 23, 10500.00,  'Cash',        '2023-05-05 10:00:00'),  -- 3500 * 3
    (24, 24, 20000.00,  'Credit Card', '2023-05-09 10:00:00'),  -- 5000 * 4
    (25, 25,  3000.00,  'Debit Card',  '2023-05-15 10:00:00'),  -- 1500 * 2
    (26, 26,  7500.00,  'Cash',        '2023-05-20 10:00:00');  -- 2500 * 3

INSERT INTO GuestStay (
    transaction_id,
    booking_id,
    checkin_employee_id,
    checkout_employee_id,
    check_in_time_date,
    expected_check_out_time_date,
    actual_check_out_time_date,
    remarks
) VALUES
    (22, 22,  1,  3, '2023-05-02 15:00:00', '2023-05-04 12:00:00', '2023-05-04 12:00:00', 'On-time checkout.'),
    (23, 23,  5, 13, '2023-05-06 15:00:00', '2023-05-09 12:00:00', '2023-05-09 12:45:00', 'Slightly late checkout.'),
    (24, 24, 15, 17, '2023-05-10 15:00:00', '2023-05-14 12:00:00', '2023-05-14 13:30:00', 'Late checkout within 2 hours.'),
    (25, 25, 16, 10, '2023-05-16 15:00:00', '2023-05-18 12:00:00', '2023-05-18 12:00:00', 'On-time checkout.'),
    (26, 26, 11, 20, '2023-05-21 15:00:00', '2023-05-24 12:00:00', '2023-05-24 12:30:00', 'Slightly late checkout.');


/* =========================================
   2023-06 BOOKINGS / PAYMENTS / GUEST STAYS
   ========================================= */

-- JUN Rooms used: 607(t3), 608(t4), 609(t1), 610(t2), 611(t3)

INSERT INTO booking (booking_id, guest_id, room_id, booking_date, payment_status, start_date, end_date) VALUES
    (27, 1027, 607, '2023-06-02', 'Paid', '2023-06-03', '2023-06-05'),  -- 2 nights, t3
    (28, 1028, 608, '2023-06-06', 'Paid', '2023-06-07', '2023-06-10'),  -- 3 nights, t4
    (29, 1029, 609, '2023-06-10', 'Paid', '2023-06-11', '2023-06-15'),  -- 4 nights, t1
    (30, 1030, 610, '2023-06-16', 'Paid', '2023-06-17', '2023-06-19'),  -- 2 nights, t2
    (31, 1031, 611, '2023-06-20', 'Paid', '2023-06-21', '2023-06-24');  -- 3 nights, t3

INSERT INTO payment (payment_id, booking_id, amount_paid, payment_method, payment_datetime) VALUES
    (27, 27,  7000.00,  'Cash',        '2023-06-02 10:00:00'),  -- 3500 * 2
    (28, 28, 15000.00,  'Credit Card', '2023-06-06 10:00:00'),  -- 5000 * 3
    (29, 29,  6000.00,  'Debit Card',  '2023-06-10 10:00:00'),  -- 1500 * 4
    (30, 30,  5000.00,  'Cash',        '2023-06-16 10:00:00'),  -- 2500 * 2
    (31, 31, 10500.00,  'Credit Card', '2023-06-20 10:00:00');  -- 3500 * 3

INSERT INTO GuestStay (
    transaction_id,
    booking_id,
    checkin_employee_id,
    checkout_employee_id,
    check_in_time_date,
    expected_check_out_time_date,
    actual_check_out_time_date,
    remarks
) VALUES
    (27, 27,  1,  3, '2023-06-03 15:00:00', '2023-06-05 12:00:00', '2023-06-05 12:00:00', 'On-time checkout.'),
    (28, 28,  5, 13, '2023-06-07 15:00:00', '2023-06-10 12:00:00', '2023-06-10 12:45:00', 'Slightly late checkout.'),
    (29, 29, 15, 17, '2023-06-11 15:00:00', '2023-06-15 12:00:00', '2023-06-15 13:30:00', 'Late checkout within 2 hours.'),
    (30, 30, 16, 10, '2023-06-17 15:00:00', '2023-06-19 12:00:00', '2023-06-19 12:00:00', 'On-time checkout.'),
    (31, 31, 11, 20, '2023-06-21 15:00:00', '2023-06-24 12:00:00', '2023-06-24 12:30:00', 'Slightly late checkout.');


/* =========================================
   2023-07 BOOKINGS / PAYMENTS / GUEST STAYS
   ========================================= */

-- JUL Rooms used: 612(t4), 613(t1), 614(t2), 615(t3), 616(t4)

INSERT INTO booking (booking_id, guest_id, room_id, booking_date, payment_status, start_date, end_date) VALUES
    (32, 1032, 612, '2023-07-01', 'Paid', '2023-07-02', '2023-07-04'),  -- 2 nights, t4
    (33, 1033, 613, '2023-07-04', 'Paid', '2023-07-05', '2023-07-08'),  -- 3 nights, t1
    (34, 1034, 614, '2023-07-08', 'Paid', '2023-07-09', '2023-07-13'),  -- 4 nights, t2
    (35, 1035, 615, '2023-07-14', 'Paid', '2023-07-15', '2023-07-17'),  -- 2 nights, t3
    (36, 1036, 616, '2023-07-18', 'Paid', '2023-07-19', '2023-07-22');  -- 3 nights, t4

INSERT INTO payment (payment_id, booking_id, amount_paid, payment_method, payment_datetime) VALUES
    (32, 32, 10000.00,  'Debit Card',  '2023-07-01 10:00:00'),  -- 5000 * 2
    (33, 33,  4500.00,  'Cash',        '2023-07-04 10:00:00'),  -- 1500 * 3
    (34, 34, 10000.00,  'Credit Card', '2023-07-08 10:00:00'),  -- 2500 * 4
    (35, 35,  7000.00,  'Debit Card',  '2023-07-14 10:00:00'),  -- 3500 * 2
    (36, 36, 15000.00,  'Cash',        '2023-07-18 10:00:00');  -- 5000 * 3

INSERT INTO GuestStay (
    transaction_id,
    booking_id,
    checkin_employee_id,
    checkout_employee_id,
    check_in_time_date,
    expected_check_out_time_date,
    actual_check_out_time_date,
    remarks
) VALUES
    (32, 32,  1,  3, '2023-07-02 15:00:00', '2023-07-04 12:00:00', '2023-07-04 12:00:00', 'On-time checkout.'),
    (33, 33,  5, 13, '2023-07-05 15:00:00', '2023-07-08 12:00:00', '2023-07-08 12:30:00', 'Slightly late checkout.'),
    (34, 34, 15, 17, '2023-07-09 15:00:00', '2023-07-13 12:00:00', '2023-07-13 13:15:00', 'Late checkout within 2 hours.'),
    (35, 35, 16, 10, '2023-07-15 15:00:00', '2023-07-17 12:00:00', '2023-07-17 12:00:00', 'On-time checkout.'),
    (36, 36, 11, 20, '2023-07-19 15:00:00', '2023-07-22 12:00:00', '2023-07-22 12:45:00', 'Slightly late checkout.');

/* =========================================
   2023-08 BOOKINGS / PAYMENTS / GUEST STAYS
   ========================================= */

-- AUG Rooms used: 617(t1), 618(t2), 619(t3), 620(t4), 701(t1)

INSERT INTO booking (booking_id, guest_id, room_id, booking_date, payment_status, start_date, end_date) VALUES
    (37, 1037, 617, '2023-08-01', 'Paid', '2023-08-02', '2023-08-04'),  -- 2 nights, t1
    (38, 1038, 618, '2023-08-05', 'Paid', '2023-08-06', '2023-08-09'),  -- 3 nights, t2
    (39, 1039, 619, '2023-08-09', 'Paid', '2023-08-10', '2023-08-14'),  -- 4 nights, t3
    (40, 1040, 620, '2023-08-15', 'Paid', '2023-08-16', '2023-08-18'),  -- 2 nights, t4
    (41, 1041, 701, '2023-08-20', 'Paid', '2023-08-21', '2023-08-24');  -- 3 nights, t1

-- Rates: t1=1500, t2=2500, t3=3500, t4=5000

INSERT INTO payment (payment_id, booking_id, amount_paid, payment_method, payment_datetime) VALUES
    (37, 37,  3000.00,  'Cash',        '2023-08-01 10:00:00'),  -- 1500 * 2
    (38, 38,  7500.00,  'Credit Card', '2023-08-05 10:00:00'),  -- 2500 * 3
    (39, 39, 14000.00,  'Debit Card',  '2023-08-09 10:00:00'),  -- 3500 * 4
    (40, 40, 10000.00,  'Cash',        '2023-08-15 10:00:00'),  -- 5000 * 2
    (41, 41,  4500.00,  'Credit Card', '2023-08-20 10:00:00');  -- 1500 * 3

-- Allowed FD/Admin employees:
-- FD: 1,5,8,11,14,15,16,19  |  Admin: 3,7,10,13,17,20

INSERT INTO GuestStay (
    transaction_id,
    booking_id,
    checkin_employee_id,
    checkout_employee_id,
    check_in_time_date,
    expected_check_out_time_date,
    actual_check_out_time_date,
    remarks
) VALUES
    (37, 37,  1,  3, '2023-08-02 15:00:00', '2023-08-04 12:00:00', '2023-08-04 12:00:00', 'On-time checkout.'),
    (38, 38,  5, 13, '2023-08-06 15:00:00', '2023-08-09 12:00:00', '2023-08-09 12:30:00', 'Slightly late checkout.'),
    (39, 39, 15, 17, '2023-08-10 15:00:00', '2023-08-14 12:00:00', '2023-08-14 13:15:00', 'Late checkout within 2 hours.'),
    (40, 40, 16, 10, '2023-08-16 15:00:00', '2023-08-18 12:00:00', '2023-08-18 12:00:00', 'On-time checkout.'),
    (41, 41, 11, 20, '2023-08-21 15:00:00', '2023-08-24 12:00:00', '2023-08-24 12:45:00', 'Slightly late checkout.');


/* =========================================
   2023-09 BOOKINGS / PAYMENTS / GUEST STAYS
   ========================================= */

-- SEP Rooms used: 702(t2), 703(t3), 704(t4), 705(t1), 706(t2)

INSERT INTO booking (booking_id, guest_id, room_id, booking_date, payment_status, start_date, end_date) VALUES
    (42, 1042, 702, '2023-09-01', 'Paid', '2023-09-02', '2023-09-04'),  -- 2 nights, t2
    (43, 1043, 703, '2023-09-05', 'Paid', '2023-09-06', '2023-09-09'),  -- 3 nights, t3
    (44, 1044, 704, '2023-09-09', 'Paid', '2023-09-10', '2023-09-14'),  -- 4 nights, t4
    (45, 1045, 705, '2023-09-15', 'Paid', '2023-09-16', '2023-09-18'),  -- 2 nights, t1
    (46, 1046, 706, '2023-09-20', 'Paid', '2023-09-21', '2023-09-24');  -- 3 nights, t2

INSERT INTO payment (payment_id, booking_id, amount_paid, payment_method, payment_datetime) VALUES
    (42, 42,  5000.00,  'Debit Card',  '2023-09-01 10:00:00'),  -- 2500 * 2
    (43, 43, 10500.00,  'Cash',        '2023-09-05 10:00:00'),  -- 3500 * 3
    (44, 44, 20000.00,  'Credit Card', '2023-09-09 10:00:00'),  -- 5000 * 4
    (45, 45,  3000.00,  'Debit Card',  '2023-09-15 10:00:00'),  -- 1500 * 2
    (46, 46,  7500.00,  'Cash',        '2023-09-20 10:00:00');  -- 2500 * 3

INSERT INTO GuestStay (
    transaction_id,
    booking_id,
    checkin_employee_id,
    checkout_employee_id,
    check_in_time_date,
    expected_check_out_time_date,
    actual_check_out_time_date,
    remarks
) VALUES
    (42, 42,  1,  3, '2023-09-02 15:00:00', '2023-09-04 12:00:00', '2023-09-04 12:00:00', 'On-time checkout.'),
    (43, 43,  5, 13, '2023-09-06 15:00:00', '2023-09-09 12:00:00', '2023-09-09 12:45:00', 'Slightly late checkout.'),
    (44, 44, 15, 17, '2023-09-10 15:00:00', '2023-09-14 12:00:00', '2023-09-14 13:30:00', 'Late checkout within 2 hours.'),
    (45, 45, 16, 10, '2023-09-16 15:00:00', '2023-09-18 12:00:00', '2023-09-18 12:00:00', 'On-time checkout.'),
    (46, 46, 11, 20, '2023-09-21 15:00:00', '2023-09-24 12:00:00', '2023-09-24 12:30:00', 'Slightly late checkout.');


/* =========================================
   2023-10 BOOKINGS / PAYMENTS / GUEST STAYS
   ========================================= */

-- OCT Rooms used: 707(t3), 708(t4), 709(t1), 710(t2), 711(t3)

INSERT INTO booking (booking_id, guest_id, room_id, booking_date, payment_status, start_date, end_date) VALUES
    (47, 1047, 707, '2023-10-01', 'Paid', '2023-10-02', '2023-10-04'),  -- 2 nights, t3
    (48, 1048, 708, '2023-10-05', 'Paid', '2023-10-06', '2023-10-09'),  -- 3 nights, t4
    (49, 1049, 709, '2023-10-09', 'Paid', '2023-10-10', '2023-10-14'),  -- 4 nights, t1
    (50, 1050, 710, '2023-10-15', 'Paid', '2023-10-16', '2023-10-18'),  -- 2 nights, t2
    (51, 1051, 711, '2023-10-20', 'Paid', '2023-10-21', '2023-10-24');  -- 3 nights, t3

INSERT INTO payment (payment_id, booking_id, amount_paid, payment_method, payment_datetime) VALUES
    (47, 47,  7000.00,  'Cash',        '2023-10-01 10:00:00'),  -- 3500 * 2
    (48, 48, 15000.00,  'Credit Card', '2023-10-05 10:00:00'),  -- 5000 * 3
    (49, 49,  6000.00,  'Debit Card',  '2023-10-09 10:00:00'),  -- 1500 * 4
    (50, 50,  5000.00,  'Cash',        '2023-10-15 10:00:00'),  -- 2500 * 2
    (51, 51, 10500.00,  'Credit Card', '2023-10-20 10:00:00');  -- 3500 * 3

INSERT INTO GuestStay (
    transaction_id,
    booking_id,
    checkin_employee_id,
    checkout_employee_id,
    check_in_time_date,
    expected_check_out_time_date,
    actual_check_out_time_date,
    remarks
) VALUES
    (47, 47,  1,  3, '2023-10-02 15:00:00', '2023-10-04 12:00:00', '2023-10-04 12:00:00', 'On-time checkout.'),
    (48, 48,  5, 13, '2023-10-06 15:00:00', '2023-10-09 12:00:00', '2023-10-09 12:45:00', 'Slightly late checkout.'),
    (49, 49, 15, 17, '2023-10-10 15:00:00', '2023-10-14 12:00:00', '2023-10-14 13:30:00', 'Late checkout within 2 hours.'),
    (50, 50, 16, 10, '2023-10-16 15:00:00', '2023-10-18 12:00:00', '2023-10-18 12:00:00', 'On-time checkout.'),
    (51, 51, 11, 20, '2023-10-21 15:00:00', '2023-10-24 12:00:00', '2023-10-24 12:30:00', 'Slightly late checkout.');


/* =========================================
   2023-11 BOOKINGS / PAYMENTS / GUEST STAYS
   ========================================= */

-- NOV Rooms used: 712(t4), 713(t1), 714(t2), 715(t3), 716(t4)

INSERT INTO booking (booking_id, guest_id, room_id, booking_date, payment_status, start_date, end_date) VALUES
    (52, 1052, 712, '2023-11-01', 'Paid', '2023-11-02', '2023-11-04'),  -- 2 nights, t4
    (53, 1053, 713, '2023-11-04', 'Paid', '2023-11-05', '2023-11-08'),  -- 3 nights, t1
    (54, 1054, 714, '2023-11-08', 'Paid', '2023-11-09', '2023-11-13'),  -- 4 nights, t2
    (55, 1055, 715, '2023-11-14', 'Paid', '2023-11-15', '2023-11-17'),  -- 2 nights, t3
    (56, 1056, 716, '2023-11-18', 'Paid', '2023-11-19', '2023-11-22');  -- 3 nights, t4

INSERT INTO payment (payment_id, booking_id, amount_paid, payment_method, payment_datetime) VALUES
    (52, 52, 10000.00,  'Debit Card',  '2023-11-01 10:00:00'),  -- 5000 * 2
    (53, 53,  4500.00,  'Cash',        '2023-11-04 10:00:00'),  -- 1500 * 3
    (54, 54, 10000.00,  'Credit Card', '2023-11-08 10:00:00'),  -- 2500 * 4
    (55, 55,  7000.00,  'Debit Card',  '2023-11-14 10:00:00'),  -- 3500 * 2
    (56, 56, 15000.00,  'Cash',        '2023-11-18 10:00:00');  -- 5000 * 3

INSERT INTO GuestStay (
    transaction_id,
    booking_id,
    checkin_employee_id,
    checkout_employee_id,
    check_in_time_date,
    expected_check_out_time_date,
    actual_check_out_time_date,
    remarks
) VALUES
    (52, 52,  1,  3, '2023-11-02 15:00:00', '2023-11-04 12:00:00', '2023-11-04 12:00:00', 'On-time checkout.'),
    (53, 53,  5, 13, '2023-11-05 15:00:00', '2023-11-08 12:00:00', '2023-11-08 12:30:00', 'Slightly late checkout.'),
    (54, 54, 15, 17, '2023-11-09 15:00:00', '2023-11-13 12:00:00', '2023-11-13 13:15:00', 'Late checkout within 2 hours.'),
    (55, 55, 16, 10, '2023-11-15 15:00:00', '2023-11-17 12:00:00', '2023-11-17 12:00:00', 'On-time checkout.'),
    (56, 56, 11, 20, '2023-11-19 15:00:00', '2023-11-22 12:00:00', '2023-11-22 12:45:00', 'Slightly late checkout.');


/* =========================================
   2023-12 BOOKINGS / PAYMENTS / GUEST STAYS
   ========================================= */

-- DEC Rooms used: 717(t1), 718(t2), 719(t3), 720(t4), 801(t1)

INSERT INTO booking (booking_id, guest_id, room_id, booking_date, payment_status, start_date, end_date) VALUES
    (57, 1057, 717, '2023-12-01', 'Paid', '2023-12-02', '2023-12-04'),  -- 2 nights, t1
    (58, 1058, 718, '2023-12-05', 'Paid', '2023-12-06', '2023-12-09'),  -- 3 nights, t2
    (59, 1059, 719, '2023-12-09', 'Paid', '2023-12-10', '2023-12-14'),  -- 4 nights, t3
    (60, 1060, 720, '2023-12-15', 'Paid', '2023-12-16', '2023-12-18'),  -- 2 nights, t4
    (61, 1061, 801, '2023-12-20', 'Paid', '2023-12-21', '2023-12-24');  -- 3 nights, t1

INSERT INTO payment (payment_id, booking_id, amount_paid, payment_method, payment_datetime) VALUES
    (57, 57,  3000.00,  'Debit Card',  '2023-12-01 10:00:00'),  -- 1500 * 2
    (58, 58,  7500.00,  'Cash',        '2023-12-05 10:00:00'),  -- 2500 * 3
    (59, 59, 14000.00,  'Credit Card', '2023-12-09 10:00:00'),  -- 3500 * 4
    (60, 60, 10000.00,  'Debit Card',  '2023-12-15 10:00:00'),  -- 5000 * 2
    (61, 61,  4500.00,  'Cash',        '2023-12-20 10:00:00');  -- 1500 * 3

INSERT INTO GuestStay (
    transaction_id,
    booking_id,
    checkin_employee_id,
    checkout_employee_id,
    check_in_time_date,
    expected_check_out_time_date,
    actual_check_out_time_date,
    remarks
) VALUES
    (57, 57,  1,  3, '2023-12-02 15:00:00', '2023-12-04 12:00:00', '2023-12-04 12:00:00', 'On-time checkout.'),
    (58, 58,  5, 13, '2023-12-06 15:00:00', '2023-12-09 12:00:00', '2023-12-09 12:30:00', 'Slightly late checkout.'),
    (59, 59, 15, 17, '2023-12-10 15:00:00', '2023-12-14 12:00:00', '2023-12-14 13:15:00', 'Late checkout within 2 hours.'),
    (60, 60, 16, 10, '2023-12-16 15:00:00', '2023-12-18 12:00:00', '2023-12-18 12:00:00', 'On-time checkout.'),
    (61, 61, 11, 20, '2023-12-21 15:00:00', '2023-12-24 12:00:00', '2023-12-24 12:45:00', 'Slightly late checkout.');

/* =========================================
   2024-01 BOOKINGS / PAYMENTS / GUEST STAYS
   ========================================= */

-- JAN 2024 Rooms: 802(t2), 803(t3), 804(t4), 805(t1), 806(t2)
-- Rates: t1=1500, t2=2500, t3=3500, t4=5000

INSERT INTO booking (booking_id, guest_id, room_id, booking_date, payment_status, start_date, end_date) VALUES
    (62, 1062, 802, '2024-01-02', 'Paid', '2024-01-03', '2024-01-05'),  -- 2 nights, t2
    (63, 1063, 803, '2024-01-05', 'Paid', '2024-01-06', '2024-01-09'),  -- 3 nights, t3
    (64, 1064, 804, '2024-01-09', 'Paid', '2024-01-10', '2024-01-14'),  -- 4 nights, t4
    (65, 1065, 805, '2024-01-15', 'Paid', '2024-01-16', '2024-01-18'),  -- 2 nights, t1
    (66, 1066, 806, '2024-01-20', 'Paid', '2024-01-21', '2024-01-24');  -- 3 nights, t2

INSERT INTO payment (payment_id, booking_id, amount_paid, payment_method, payment_datetime) VALUES
    (62, 62,  5000.00,  'Cash',        '2024-01-02 10:00:00'),  -- 2500 * 2
    (63, 63, 10500.00,  'Credit Card', '2024-01-05 10:00:00'),  -- 3500 * 3
    (64, 64, 20000.00,  'Debit Card',  '2024-01-09 10:00:00'),  -- 5000 * 4
    (65, 65,  3000.00,  'Cash',        '2024-01-15 10:00:00'),  -- 1500 * 2
    (66, 66,  7500.00,  'Credit Card', '2024-01-20 10:00:00');  -- 2500 * 3

-- FD: 1,5,8,11,14,15,16,19  |  Admin: 3,7,10,13,17,20

INSERT INTO GuestStay (
    transaction_id,
    booking_id,
    checkin_employee_id,
    checkout_employee_id,
    check_in_time_date,
    expected_check_out_time_date,
    actual_check_out_time_date,
    remarks
) VALUES
    (62, 62,  1,  3, '2024-01-03 15:00:00', '2024-01-05 12:00:00', '2024-01-05 12:00:00', 'On-time checkout.'),
    (63, 63,  5, 13, '2024-01-06 15:00:00', '2024-01-09 12:00:00', '2024-01-09 12:30:00', 'Slightly late checkout.'),
    (64, 64, 15, 17, '2024-01-10 15:00:00', '2024-01-14 12:00:00', '2024-01-14 13:15:00', 'Late checkout within 2 hours.'),
    (65, 65, 16, 10, '2024-01-16 15:00:00', '2024-01-18 12:00:00', '2024-01-18 12:00:00', 'On-time checkout.'),
    (66, 66, 11, 20, '2024-01-21 15:00:00', '2024-01-24 12:00:00', '2024-01-24 12:45:00', 'Slightly late checkout.');


/* =========================================
   2024-02 BOOKINGS / PAYMENTS / GUEST STAYS
   ========================================= */

-- FEB 2024 Rooms: 807(t3), 808(t4), 809(t1), 810(t2), 811(t3)

INSERT INTO booking (booking_id, guest_id, room_id, booking_date, payment_status, start_date, end_date) VALUES
    (67, 1067, 807, '2024-02-01', 'Paid', '2024-02-02', '2024-02-04'),  -- 2 nights, t3
    (68, 1068, 808, '2024-02-04', 'Paid', '2024-02-05', '2024-02-08'),  -- 3 nights, t4
    (69, 1069, 809, '2024-02-08', 'Paid', '2024-02-09', '2024-02-13'),  -- 4 nights, t1
    (70, 1070, 810, '2024-02-14', 'Paid', '2024-02-15', '2024-02-17'),  -- 2 nights, t2
    (71, 1071, 811, '2024-02-18', 'Paid', '2024-02-19', '2024-02-22');  -- 3 nights, t3

INSERT INTO payment (payment_id, booking_id, amount_paid, payment_method, payment_datetime) VALUES
    (67, 67,  7000.00,  'Debit Card',  '2024-02-01 10:00:00'),  -- 3500 * 2
    (68, 68, 15000.00,  'Cash',        '2024-02-04 10:00:00'),  -- 5000 * 3
    (69, 69,  6000.00,  'Credit Card', '2024-02-08 10:00:00'),  -- 1500 * 4
    (70, 70,  5000.00,  'Debit Card',  '2024-02-14 10:00:00'),  -- 2500 * 2
    (71, 71, 10500.00,  'Cash',        '2024-02-18 10:00:00');  -- 3500 * 3

INSERT INTO GuestStay (
    transaction_id,
    booking_id,
    checkin_employee_id,
    checkout_employee_id,
    check_in_time_date,
    expected_check_out_time_date,
    actual_check_out_time_date,
    remarks
) VALUES
    (67, 67,  1,  3, '2024-02-02 15:00:00', '2024-02-04 12:00:00', '2024-02-04 12:00:00', 'On-time checkout.'),
    (68, 68,  5, 13, '2024-02-05 15:00:00', '2024-02-08 12:00:00', '2024-02-08 12:45:00', 'Slightly late checkout.'),
    (69, 69, 15, 17, '2024-02-09 15:00:00', '2024-02-13 12:00:00', '2024-02-13 13:30:00', 'Late checkout within 2 hours.'),
    (70, 70, 16, 10, '2024-02-15 15:00:00', '2024-02-17 12:00:00', '2024-02-17 12:00:00', 'On-time checkout.'),
    (71, 71, 11, 20, '2024-02-19 15:00:00', '2024-02-22 12:00:00', '2024-02-22 12:30:00', 'Slightly late checkout.');


/* =========================================
   2024-03 BOOKINGS / PAYMENTS / GUEST STAYS
   ========================================= */

-- MAR 2024 Rooms: 812(t4), 813(t1), 814(t2), 815(t3), 816(t4)

INSERT INTO booking (booking_id, guest_id, room_id, booking_date, payment_status, start_date, end_date) VALUES
    (72, 1072, 812, '2024-03-01', 'Paid', '2024-03-02', '2024-03-04'),  -- 2 nights, t4
    (73, 1073, 813, '2024-03-04', 'Paid', '2024-03-05', '2024-03-08'),  -- 3 nights, t1
    (74, 1074, 814, '2024-03-08', 'Paid', '2024-03-09', '2024-03-13'),  -- 4 nights, t2
    (75, 1075, 815, '2024-03-14', 'Paid', '2024-03-15', '2024-03-17'),  -- 2 nights, t3
    (76, 1076, 816, '2024-03-18', 'Paid', '2024-03-19', '2024-03-22');  -- 3 nights, t4

INSERT INTO payment (payment_id, booking_id, amount_paid, payment_method, payment_datetime) VALUES
    (72, 72, 10000.00,  'Cash',        '2024-03-01 10:00:00'),  -- 5000 * 2
    (73, 73,  4500.00,  'Credit Card', '2024-03-04 10:00:00'),  -- 1500 * 3
    (74, 74, 10000.00,  'Debit Card',  '2024-03-08 10:00:00'),  -- 2500 * 4
    (75, 75,  7000.00,  'Cash',        '2024-03-14 10:00:00'),  -- 3500 * 2
    (76, 76, 15000.00,  'Credit Card', '2024-03-18 10:00:00');  -- 5000 * 3

INSERT INTO GuestStay (
    transaction_id,
    booking_id,
    checkin_employee_id,
    checkout_employee_id,
    check_in_time_date,
    expected_check_out_time_date,
    actual_check_out_time_date,
    remarks
) VALUES
    (72, 72,  1,  3, '2024-03-02 15:00:00', '2024-03-04 12:00:00', '2024-03-04 12:00:00', 'On-time checkout.'),
    (73, 73,  5, 13, '2024-03-05 15:00:00', '2024-03-08 12:00:00', '2024-03-08 12:30:00', 'Slightly late checkout.'),
    (74, 74, 15, 17, '2024-03-09 15:00:00', '2024-03-13 12:00:00', '2024-03-13 13:15:00', 'Late checkout within 2 hours.'),
    (75, 75, 16, 10, '2024-03-15 15:00:00', '2024-03-17 12:00:00', '2024-03-17 12:00:00', 'On-time checkout.'),
    (76, 76, 11, 20, '2024-03-19 15:00:00', '2024-03-22 12:00:00', '2024-03-22 12:45:00', 'Slightly late checkout.');


/* =========================================
   2024-04 BOOKINGS / PAYMENTS / GUEST STAYS
   ========================================= */

-- APR 2024 Rooms: 817(t1), 818(t2), 819(t3), 820(t4), 821(t1)

INSERT INTO booking (booking_id, guest_id, room_id, booking_date, payment_status, start_date, end_date) VALUES
    (77, 1077, 817, '2024-04-01', 'Paid', '2024-04-02', '2024-04-04'),  -- 2 nights, t1
    (78, 1078, 818, '2024-04-04', 'Paid', '2024-04-05', '2024-04-08'),  -- 3 nights, t2
    (79, 1079, 819, '2024-04-08', 'Paid', '2024-04-09', '2024-04-13'),  -- 4 nights, t3
    (80, 1080, 820, '2024-04-14', 'Paid', '2024-04-15', '2024-04-17'), -- 2 nights, t4
	 (81, 1081, 820, '2024-04-14', 'Paid', '2024-04-15', '2024-04-17');

INSERT INTO payment (payment_id, booking_id, amount_paid, payment_method, payment_datetime) VALUES
    (77, 77,  3000.00,  'Debit Card',  '2024-04-01 10:00:00'),  -- 1500 * 2
    (78, 78,  7500.00,  'Cash',        '2024-04-04 10:00:00'),  -- 2500 * 3
    (79, 79, 14000.00,  'Credit Card', '2024-04-08 10:00:00'),  -- 3500 * 4
    (80, 80, 10000.00,  'Debit Card',  '2024-04-14 10:00:00'), -- 5000 * 2
	 (81, 81, 10000.00,  'Debit Card',  '2024-04-14 10:00:01');

INSERT INTO GuestStay (
    transaction_id,
    booking_id,
    checkin_employee_id,
    checkout_employee_id,
    check_in_time_date,
    expected_check_out_time_date,
    actual_check_out_time_date,
    remarks
) VALUES
    (77, 77,  1,  3, '2024-04-02 15:00:00', '2024-04-04 12:00:00', '2024-04-04 12:00:00', 'On-time checkout.'),
    (78, 78,  5, 13, '2024-04-05 15:00:00', '2024-04-08 12:00:00', '2024-04-08 12:30:00', 'Slightly late checkout.'),
    (79, 79, 15, 17, '2024-04-09 15:00:00', '2024-04-13 12:00:00', '2024-04-13 13:15:00', 'Late checkout within 2 hours.'),
    (80, 80, 16, 10, '2024-04-15 15:00:00', '2024-04-17 12:00:00', '2024-04-17 12:00:00', 'On-time checkout.'),
      (81, 81, 16, 10, '2024-04-15 15:00:00', '2024-04-17 12:00:00', '2024-04-17 12:00:00', 'On-time checkout.');
   


/* =========================================
   2024-05 BOOKINGS / PAYMENTS / GUEST STAYS
   ========================================= */

-- MAY 2024 Rooms: 901(t1), 902(t2), 903(t3), 904(t4), 905(t1)
-- Rates: t1=1500, t2=2500, t3=3500, t4=5000

INSERT INTO booking (booking_id, guest_id, room_id, booking_date, payment_status, start_date, end_date) VALUES
    (82, 1082, 901, '2024-05-01', 'Paid', '2024-05-02', '2024-05-04'),  -- 2 nights, t1
    (83, 1083, 902, '2024-05-04', 'Paid', '2024-05-05', '2024-05-08'),  -- 3 nights, t2
    (84, 1084, 903, '2024-05-08', 'Paid', '2024-05-09', '2024-05-13'),  -- 4 nights, t3
    (85, 1085, 904, '2024-05-14', 'Paid', '2024-05-15', '2024-05-17'),  -- 2 nights, t4
    (86, 1086, 905, '2024-05-18', 'Paid', '2024-05-19', '2024-05-22');  -- 3 nights, t1

INSERT INTO payment (payment_id, booking_id, amount_paid, payment_method, payment_datetime) VALUES
    (82, 82,  3000.00,  'Cash',        '2024-05-01 10:00:00'),  -- 1500 * 2
    (83, 83,  7500.00,  'Credit Card', '2024-05-04 10:00:00'),  -- 2500 * 3
    (84, 84, 14000.00,  'Debit Card',  '2024-05-08 10:00:00'),  -- 3500 * 4
    (85, 85, 10000.00,  'Cash',        '2024-05-14 10:00:00'),  -- 5000 * 2
    (86, 86,  4500.00,  'Credit Card', '2024-05-18 10:00:00');  -- 1500 * 3

-- FD: 1,5,8,11,14,15,16,19 | Admin: 3,7,10,13,17,20

INSERT INTO GuestStay (
    transaction_id,
    booking_id,
    checkin_employee_id,
    checkout_employee_id,
    check_in_time_date,
    expected_check_out_time_date,
    actual_check_out_time_date,
    remarks
) VALUES
    (82, 82,  1,  3, '2024-05-02 15:00:00', '2024-05-04 12:00:00', '2024-05-04 12:00:00', 'On-time checkout.'),
    (83, 83,  5, 13, '2024-05-05 15:00:00', '2024-05-08 12:00:00', '2024-05-08 12:30:00', 'Slightly late checkout.'),
    (84, 84, 15, 17, '2024-05-09 15:00:00', '2024-05-13 12:00:00', '2024-05-13 13:15:00', 'Late checkout within 2 hours.'),
    (85, 85, 16, 10, '2024-05-15 15:00:00', '2024-05-17 12:00:00', '2024-05-17 12:00:00', 'On-time checkout.'),
    (86, 86, 11, 20, '2024-05-19 15:00:00', '2024-05-22 12:00:00', '2024-05-22 12:45:00', 'Slightly late checkout.');


/* =========================================
   2024-06 BOOKINGS / PAYMENTS / GUEST STAYS
   ========================================= */

-- JUN 2024 Rooms: 906(t2), 907(t3), 908(t4), 909(t1), 910(t2)

INSERT INTO booking (booking_id, guest_id, room_id, booking_date, payment_status, start_date, end_date) VALUES
    (87, 1087, 906, '2024-06-01', 'Paid', '2024-06-02', '2024-06-04'),  -- 2 nights, t2
    (88, 1088, 907, '2024-06-04', 'Paid', '2024-06-05', '2024-06-08'),  -- 3 nights, t3
    (89, 1089, 908, '2024-06-08', 'Paid', '2024-06-09', '2024-06-13'),  -- 4 nights, t4
    (90, 1090, 909, '2024-06-14', 'Paid', '2024-06-15', '2024-06-17'),  -- 2 nights, t1
    (91, 1091, 910, '2024-06-18', 'Paid', '2024-06-19', '2024-06-22');  -- 3 nights, t2

INSERT INTO payment (payment_id, booking_id, amount_paid, payment_method, payment_datetime) VALUES
    (87, 87,  5000.00,  'Debit Card',  '2024-06-01 10:00:00'),  -- 2500 * 2
    (88, 88, 10500.00,  'Cash',        '2024-06-04 10:00:00'),  -- 3500 * 3
    (89, 89, 20000.00,  'Credit Card', '2024-06-08 10:00:00'),  -- 5000 * 4
    (90, 90,  3000.00,  'Debit Card',  '2024-06-14 10:00:00'),  -- 1500 * 2
    (91, 91,  7500.00,  'Cash',        '2024-06-18 10:00:00');  -- 2500 * 3

INSERT INTO GuestStay (
    transaction_id,
    booking_id,
    checkin_employee_id,
    checkout_employee_id,
    check_in_time_date,
    expected_check_out_time_date,
    actual_check_out_time_date,
    remarks
) VALUES
    (87, 87,  1,  3, '2024-06-02 15:00:00', '2024-06-04 12:00:00', '2024-06-04 12:00:00', 'On-time checkout.'),
    (88, 88,  5, 13, '2024-06-05 15:00:00', '2024-06-08 12:00:00', '2024-06-08 12:45:00', 'Slightly late checkout.'),
    (89, 89, 15, 17, '2024-06-09 15:00:00', '2024-06-13 12:00:00', '2024-06-13 13:30:00', 'Late checkout within 2 hours.'),
    (90, 90, 16, 10, '2024-06-15 15:00:00', '2024-06-17 12:00:00', '2024-06-17 12:00:00', 'On-time checkout.'),
    (91, 91, 11, 20, '2024-06-19 15:00:00', '2024-06-22 12:00:00', '2024-06-22 12:30:00', 'Slightly late checkout.');


/* =========================================
   2024-07 BOOKINGS / PAYMENTS / GUEST STAYS
   ========================================= */

-- JUL 2024 Rooms: 911(t3), 912(t4), 913(t1), 914(t2), 915(t3)

INSERT INTO booking (booking_id, guest_id, room_id, booking_date, payment_status, start_date, end_date) VALUES
    (92, 1092, 911, '2024-07-01', 'Paid', '2024-07-02', '2024-07-04'),  -- 2 nights, t3
    (93, 1093, 912, '2024-07-04', 'Paid', '2024-07-05', '2024-07-08'),  -- 3 nights, t4
    (94, 1094, 913, '2024-07-08', 'Paid', '2024-07-09', '2024-07-13'),  -- 4 nights, t1
    (95, 1095, 914, '2024-07-14', 'Paid', '2024-07-15', '2024-07-17'),  -- 2 nights, t2
    (96, 1096, 915, '2024-07-18', 'Paid', '2024-07-19', '2024-07-22');  -- 3 nights, t3

INSERT INTO payment (payment_id, booking_id, amount_paid, payment_method, payment_datetime) VALUES
    (92, 92,  7000.00,  'Cash',        '2024-07-01 10:00:00'),  -- 3500 * 2
    (93, 93, 15000.00,  'Credit Card', '2024-07-04 10:00:00'),  -- 5000 * 3
    (94, 94,  6000.00,  'Debit Card',  '2024-07-08 10:00:00'),  -- 1500 * 4
    (95, 95,  5000.00,  'Cash',        '2024-07-14 10:00:00'),  -- 2500 * 2
    (96, 96, 10500.00,  'Credit Card', '2024-07-18 10:00:00');  -- 3500 * 3

INSERT INTO GuestStay (
    transaction_id,
    booking_id,
    checkin_employee_id,
    checkout_employee_id,
    check_in_time_date,
    expected_check_out_time_date,
    actual_check_out_time_date,
    remarks
) VALUES
    (92, 92,  1,  3, '2024-07-02 15:00:00', '2024-07-04 12:00:00', '2024-07-04 12:00:00', 'On-time checkout.'),
    (93, 93,  5, 13, '2024-07-05 15:00:00', '2024-07-08 12:00:00', '2024-07-08 12:45:00', 'Slightly late checkout.'),
    (94, 94, 15, 17, '2024-07-09 15:00:00', '2024-07-13 12:00:00', '2024-07-13 13:15:00', 'Late checkout within 2 hours.'),
    (95, 95, 16, 10, '2024-07-15 15:00:00', '2024-07-17 12:00:00', '2024-07-17 12:00:00', 'On-time checkout.'),
    (96, 96, 11, 20, '2024-07-19 15:00:00', '2024-07-22 12:00:00', '2024-07-22 12:30:00', 'Slightly late checkout.');


/* =========================================
   2024-08 BOOKINGS / PAYMENTS / GUEST STAYS
   ========================================= */

-- AUG 2024 Rooms: 916(t4), 917(t1), 918(t2), 919(t3), 920(t4)

INSERT INTO booking (booking_id, guest_id, room_id, booking_date, payment_status, start_date, end_date) VALUES
    (97, 1097, 916, '2024-08-01', 'Paid', '2024-08-02', '2024-08-04'),  -- 2 nights, t4
    (98, 1098, 917, '2024-08-04', 'Paid', '2024-08-05', '2024-08-08'),  -- 3 nights, t1
    (99, 1099, 918, '2024-08-08', 'Paid', '2024-08-09', '2024-08-13'),  -- 4 nights, t2
    (100,1100, 919, '2024-08-14', 'Paid', '2024-08-15', '2024-08-17'),  -- 2 nights, t3
    (101,1001, 920, '2024-08-18', 'Paid', '2024-08-19', '2024-08-22');  -- 3 nights, t4 (reuses guest 1001, allowed)

INSERT INTO payment (payment_id, booking_id, amount_paid, payment_method, payment_datetime) VALUES
    (97,  97, 10000.00,  'Debit Card',  '2024-08-01 10:00:00'),  -- 5000 * 2
    (98,  98,  4500.00,  'Cash',        '2024-08-04 10:00:00'),  -- 1500 * 3
    (99,  99, 10000.00,  'Credit Card', '2024-08-08 10:00:00'),  -- 2500 * 4
    (100,100,  7000.00,  'Debit Card',  '2024-08-14 10:00:00'),  -- 3500 * 2
    (101,101, 15000.00,  'Cash',        '2024-08-18 10:00:00');  -- 5000 * 3

INSERT INTO GuestStay (
    transaction_id,
    booking_id,
    checkin_employee_id,
    checkout_employee_id,
    check_in_time_date,
    expected_check_out_time_date,
    actual_check_out_time_date,
    remarks
) VALUES
    (97,  97,  1,  3, '2024-08-02 15:00:00', '2024-08-04 12:00:00', '2024-08-04 12:00:00', 'On-time checkout.'),
    (98,  98,  5, 13, '2024-08-05 15:00:00', '2024-08-08 12:00:00', '2024-08-08 12:30:00', 'Slightly late checkout.'),
    (99,  99, 15, 17, '2024-08-09 15:00:00', '2024-08-13 12:00:00', '2024-08-13 13:15:00', 'Late checkout within 2 hours.'),
    (100,100, 16, 10, '2024-08-15 15:00:00', '2024-08-17 12:00:00', '2024-08-17 12:00:00', 'On-time checkout.'),
    (101,101, 11, 20, '2024-08-19 15:00:00', '2024-08-22 12:00:00', '2024-08-22 12:45:00', 'Slightly late checkout.');



/* ===============================
   2024-09 BOOKINGS / PAYMENTS / GUEST STAY
   =============================== */

-- BOOKINGS
INSERT INTO booking (booking_id, guest_id, room_id, booking_date, payment_status, start_date, end_date) VALUES
(102, 1102, 801, '2024-09-01', 'Paid', '2024-09-02', '2024-09-04'), -- 2 nights, t1
(103, 1103, 802, '2024-09-05', 'Paid', '2024-09-06', '2024-09-09'), -- 3 nights, t2
(104, 1104, 803, '2024-09-10', 'Paid', '2024-09-11', '2024-09-13'), -- 2 nights, t3
(105, 1105, 804, '2024-09-15', 'Paid', '2024-09-16', '2024-09-19'); -- 3 nights, t4

INSERT INTO payment (payment_id, booking_id, amount_paid, payment_method, payment_datetime) VALUES
(102, 102, 3000,  'Cash',        '2024-09-01 09:00:00'),   -- 1500×2
(103, 103, 7500,  'Debit Card',  '2024-09-05 09:00:00'),   -- 2500×3
(104, 104, 7000,  'Credit Card', '2024-09-10 09:00:00'),   -- 3500×2
(105, 105,15000,  'Cash',        '2024-09-15 09:00:00');   -- 5000×3

INSERT INTO GuestStay (
transaction_id, booking_id, checkin_employee_id, checkout_employee_id,
check_in_time_date, expected_check_out_time_date, actual_check_out_time_date, remarks
) VALUES
(102,102, 1, 13, '2024-09-02 15:00:00','2024-09-04 12:00:00','2024-09-04 12:10:00',''),
(103,103, 5, 16, '2024-09-06 15:00:00','2024-09-09 12:00:00','2024-09-09 12:30:00','Late 30 mins'),
(104,104,15, 8, '2024-09-11 15:00:00','2024-09-13 12:00:00','2024-09-13 12:00:00',''),
(105,105,17, 3, '2024-09-16 15:00:00','2024-09-19 12:00:00','2024-09-19 13:15:00','Late checkout (1 hr)');



-- Housekeeping Items
INSERT INTO housekeeping_item (item_name, cost_per_unit, current_stock, minimum_stock, max_stock_storage) VALUES
('Toilet Paper', 25.50, 100, 20, 200),
('Hand Soap', 18.75, 120, 25, 250),
('Shampoo', 45.25, 80, 15, 180),
('Conditioner', 42.00, 75, 15, 160),
('Bath Towel', 120.00, 60, 12, 120),
('Hand Towel', 65.00, 80, 16, 150),
('Bath Mat', 85.50, 40, 8, 80),
('Bedsheet Set', 320.00, 35, 7, 70),
('Pillow Case', 45.00, 90, 18, 180),
('Blanket', 280.75, 30, 6, 60),
('Pillow', 180.25, 25, 5, 50),
('Toilet Seat Cover', 12.50, 150, 30, 300),
('Tissue Box', 35.00, 100, 20, 200),
('Glass Cleaner', 68.00, 40, 8, 80),
('Floor Cleaner', 95.50, 35, 7, 70);



-- Housekeeping Item Issuance
INSERT INTO housekeeping_item_issuance (housekeeping_item_id, employee_id, issuer_id, quantity_issued, date_issued, remarks) VALUES
-- January 2023
(1, 2, 3, 10, '2023-01-10 09:00:00', 'Monthly restock for floors 1-3'),
(2, 4, 3, 15, '2023-01-12 10:30:00', 'Hand soap for guest rooms'),
(3, 2, 13, 8, '2023-01-15 14:15:00', 'Shampoo for VIP suites'),
(4, 9, 3, 7, '2023-01-18 11:00:00', 'Conditioner restock'),
(5, 2, 13, 4, '2023-01-20 08:45:00', 'Bath towel replacement'),

-- February 2023
(6, 4, 3, 12, '2023-02-05 13:20:00', 'Hand towels for all floors'),
(7, 9, 13, 3, '2023-02-08 10:00:00', 'Bath mat replacement'),
(8, 2, 3, 2, '2023-02-12 15:30:00', 'Bedsheet set for suite rooms'),
(9, 4, 13, 8, '2023-02-18 11:10:00', 'Pillow case rotation'),
(10, 2, 3, 2, '2023-02-22 09:45:00', 'Blankets for winter season'),

-- March 2023
(11, 9, 13, 3, '2023-03-10 16:20:00', 'Pillow replacement'),
(12, 2, 3, 20, '2023-03-15 14:00:00', 'Toilet seat covers bulk'),
(13, 4, 13, 15, '2023-03-20 10:15:00', 'Tissue box restock'),
(14, 9, 3, 5, '2023-03-25 13:45:00', 'Glass cleaner for windows'),
(15, 2, 13, 4, '2023-03-28 15:00:00', 'Floor cleaner monthly'),

-- April 2023
(1, 4, 3, 12, '2023-04-05 11:30:00', 'Toilet paper for high occupancy'),
(2, 9, 13, 18, '2023-04-10 09:15:00', 'Hand soap spring cleaning'),
(3, 2, 3, 6, '2023-04-15 12:30:00', 'Shampoo regular supply'),
(4, 4, 13, 5, '2023-04-20 14:45:00', 'Conditioner restock'),
(5, 9, 3, 3, '2023-04-25 16:00:00', 'Bath towel replacement'),

-- May 2023
(6, 2, 13, 10, '2023-05-03 09:00:00', 'Hand towels monthly'),
(7, 4, 3, 2, '2023-05-08 10:30:00', 'Bath mat damaged replacement'),
(8, 9, 13, 1, '2023-05-12 14:15:00', 'Bedsheet set for new room'),
(9, 2, 3, 6, '2023-05-18 11:00:00', 'Pillow case standard'),
(10, 4, 13, 1, '2023-05-22 08:45:00', 'Blanket for special request'),

-- June 2023
(11, 9, 3, 2, '2023-06-05 13:20:00', 'Pillow guest complaint'),
(12, 2, 13, 25, '2023-06-10 10:00:00', 'Toilet seat covers bulk'),
(13, 4, 3, 12, '2023-06-15 15:30:00', 'Tissue box summer stock'),
(14, 9, 13, 4, '2023-06-20 11:10:00', 'Glass cleaner maintenance'),
(15, 2, 3, 3, '2023-06-25 09:45:00', 'Floor cleaner quarterly'),

-- July 2023
(1, 4, 13, 8, '2023-07-08 16:20:00', 'Toilet paper mid-year'),
(2, 9, 3, 14, '2023-07-12 14:00:00', 'Hand soap summer'),
(3, 2, 13, 7, '2023-07-18 10:15:00', 'Shampoo peak season'),
(4, 4, 3, 6, '2023-07-22 13:45:00', 'Conditioner restock'),
(5, 9, 13, 2, '2023-07-28 15:00:00', 'Bath towel replacement'),

-- August 2023
(6, 2, 3, 8, '2023-08-05 11:30:00', 'Hand towels August'),
(7, 4, 13, 1, '2023-08-10 09:15:00', 'Bath mat replacement'),
(8, 9, 3, 2, '2023-08-15 12:30:00', 'Bedsheet set upgrade'),
(9, 2, 13, 7, '2023-08-20 14:45:00', 'Pillow case rotation'),
(10, 4, 3, 2, '2023-08-25 16:00:00', 'Blanket stock'),

-- September 2023
(11, 9, 13, 1, '2023-09-03 09:00:00', 'Pillow replacement'),
(12, 2, 3, 18, '2023-09-08 10:30:00', 'Toilet seat covers'),
(13, 4, 13, 10, '2023-09-12 14:15:00', 'Tissue box autumn'),
(14, 9, 3, 3, '2023-09-18 11:00:00', 'Glass cleaner windows'),
(15, 2, 13, 2, '2023-09-22 08:45:00', 'Floor cleaner monthly'),

-- October 2023
(1, 4, 3, 15, '2023-10-05 13:20:00', 'Toilet paper October'),
(2, 9, 13, 16, '2023-10-10 10:00:00', 'Hand soap fall season'),
(3, 2, 3, 8, '2023-10-15 15:30:00', 'Shampoo regular'),
(4, 4, 13, 7, '2023-10-20 11:10:00', 'Conditioner restock'),
(5, 9, 3, 3, '2023-10-25 09:45:00', 'Bath towel replacement'),

-- November 2023
(6, 2, 13, 9, '2023-11-03 16:20:00', 'Hand towels November'),
(7, 4, 3, 2, '2023-11-08 14:00:00', 'Bath mat maintenance'),
(8, 9, 13, 1, '2023-11-12 10:15:00', 'Bedsheet set replacement'),
(9, 2, 3, 8, '2023-11-18 13:45:00', 'Pillow case standard'),
(10, 4, 13, 3, '2023-11-22 15:00:00', 'Blanket winter prep'),

-- December 2023
(11, 9, 3, 2, '2023-12-05 11:30:00', 'Pillow holiday season'),
(12, 2, 13, 22, '2023-12-10 09:15:00', 'Toilet seat covers bulk'),
(13, 4, 3, 18, '2023-12-15 12:30:00', 'Tissue box December'),
(14, 9, 13, 6, '2023-12-20 14:45:00', 'Glass cleaner year-end'),
(15, 2, 3, 5, '2023-12-27 16:00:00', 'Floor cleaner deep clean'),

-- January 2024
(1, 2, 3, 12, '2024-01-08 09:00:00', 'Toilet paper new year stock'),
(2, 4, 13, 17, '2024-01-12 10:30:00', 'Hand soap January'),
(3, 9, 3, 9, '2024-01-16 14:15:00', 'Shampoo VIP rooms'),
(4, 2, 13, 8, '2024-01-20 11:00:00', 'Conditioner restock'),
(5, 4, 3, 4, '2024-01-24 08:45:00', 'Bath towel replacement'),

-- February 2024
(6, 9, 13, 11, '2024-02-05 13:20:00', 'Hand towels February'),
(7, 2, 3, 3, '2024-02-09 10:00:00', 'Bath mat replacement'),
(8, 4, 13, 2, '2024-02-14 15:30:00', 'Bedsheet set valentine'),
(9, 9, 3, 9, '2024-02-19 11:10:00', 'Pillow case rotation'),
(10, 2, 13, 2, '2024-02-23 09:45:00', 'Blanket winter'),

-- March 2024
(11, 4, 3, 3, '2024-03-07 16:20:00', 'Pillow replacement'),
(12, 9, 13, 23, '2024-03-12 14:00:00', 'Toilet seat covers'),
(13, 2, 3, 16, '2024-03-17 10:15:00', 'Tissue box spring'),
(14, 4, 13, 5, '2024-03-22 13:45:00', 'Glass cleaner windows'),
(15, 9, 3, 4, '2024-03-28 15:00:00', 'Floor cleaner monthly'),

-- April 2024
(1, 2, 13, 14, '2024-04-04 11:30:00', 'Toilet paper April'),
(2, 4, 3, 19, '2024-04-09 09:15:00', 'Hand soap spring'),
(3, 9, 13, 7, '2024-04-14 12:30:00', 'Shampoo regular'),
(4, 2, 3, 6, '2024-04-19 14:45:00', 'Conditioner restock'),
(5, 4, 13, 3, '2024-04-24 16:00:00', 'Bath towel replacement'),

-- May 2024
(6, 9, 3, 10, '2024-05-03 09:00:00', 'Hand towels May'),
(7, 2, 13, 2, '2024-05-08 10:30:00', 'Bath mat maintenance'),
(8, 4, 3, 1, '2024-05-13 14:15:00', 'Bedsheet set new'),
(9, 9, 13, 8, '2024-05-18 11:00:00', 'Pillow case standard'),
(10, 2, 3, 1, '2024-05-23 08:45:00', 'Blanket stock'),

-- June 2024
(11, 4, 13, 2, '2024-06-05 13:20:00', 'Pillow summer'),
(12, 9, 3, 26, '2024-06-10 10:00:00', 'Toilet seat covers bulk'),
(13, 2, 13, 14, '2024-06-15 15:30:00', 'Tissue box June'),
(14, 4, 3, 4, '2024-06-20 11:10:00', 'Glass cleaner maintenance'),
(15, 9, 13, 3, '2024-06-25 09:45:00', 'Floor cleaner quarterly'),

-- July 2024
(1, 2, 3, 11, '2024-07-08 16:20:00', 'Toilet paper July'),
(2, 4, 13, 15, '2024-07-12 14:00:00', 'Hand soap summer'),
(3, 9, 3, 8, '2024-07-18 10:15:00', 'Shampoo peak season'),
(4, 2, 13, 7, '2024-07-22 13:45:00', 'Conditioner restock'),
(5, 4, 3, 2, '2024-07-28 15:00:00', 'Bath towel replacement'),

-- August 2024
(6, 9, 13, 9, '2024-08-05 11:30:00', 'Hand towels August'),
(7, 2, 3, 1, '2024-08-10 09:15:00', 'Bath mat replacement'),
(8, 4, 13, 2, '2024-08-15 12:30:00', 'Bedsheet set upgrade'),
(9, 9, 3, 7, '2024-08-20 14:45:00', 'Pillow case rotation'),
(10, 2, 13, 2, '2024-08-25 16:00:00', 'Blanket stock'),

-- September 2024
(11, 4, 3, 1, '2024-09-03 09:00:00', 'Pillow replacement'),
(12, 9, 13, 20, '2024-09-08 10:30:00', 'Toilet seat covers'),
(13, 2, 3, 12, '2024-09-12 14:15:00', 'Tissue box autumn'),
(14, 4, 13, 3, '2024-09-18 11:00:00', 'Glass cleaner windows'),
(15, 9, 3, 2, '2024-09-22 08:45:00', 'Floor cleaner monthly'),

-- October 2024
(1, 2, 13, 16, '2024-10-05 13:20:00', 'Toilet paper October'),
(2, 4, 3, 18, '2024-10-10 10:00:00', 'Hand soap fall'),
(3, 9, 13, 9, '2024-10-15 15:30:00', 'Shampoo regular'),
(4, 2, 3, 8, '2024-10-20 11:10:00', 'Conditioner restock'),
(5, 4, 13, 4, '2024-10-25 09:45:00', 'Bath towel replacement'),

-- November 2024
(6, 9, 3, 10, '2024-11-03 16:20:00', 'Hand towels November'),
(7, 2, 13, 2, '2024-11-08 14:00:00', 'Bath mat maintenance'),
(8, 4, 3, 1, '2024-11-12 10:15:00', 'Bedsheet set replacement'),
(9, 9, 13, 9, '2024-11-18 13:45:00', 'Pillow case standard'),
(10, 2, 3, 3, '2024-11-22 15:00:00', 'Blanket winter prep'),

-- December 2024
(11, 4, 13, 2, '2024-12-05 11:30:00', 'Pillow holiday'),
(12, 9, 3, 24, '2024-12-10 09:15:00', 'Toilet seat covers bulk'),
(13, 2, 13, 20, '2024-12-15 12:30:00', 'Tissue box December'),
(14, 4, 3, 7, '2024-12-20 14:45:00', 'Glass cleaner year-end'),
(15, 9, 13, 6, '2024-12-27 16:00:00', 'Floor cleaner deep clean'),

-- January 2025
(1, 2, 3, 13, '2025-01-07 09:00:00', 'Toilet paper new year'),
(2, 4, 13, 16, '2025-01-11 10:30:00', 'Hand soap January'),
(3, 9, 3, 10, '2025-01-15 14:15:00', 'Shampoo VIP rooms'),
(4, 2, 13, 9, '2025-01-19 11:00:00', 'Conditioner restock'),
(5, 4, 3, 5, '2025-01-23 08:45:00', 'Bath towel replacement'),

-- February 2025
(6, 9, 13, 12, '2025-02-04 13:20:00', 'Hand towels February'),
(7, 2, 3, 4, '2025-02-08 10:00:00', 'Bath mat replacement'),
(8, 4, 13, 3, '2025-02-13 15:30:00', 'Bedsheet set valentine'),
(9, 9, 3, 10, '2025-02-18 11:10:00', 'Pillow case rotation'),
(10, 2, 13, 3, '2025-02-22 09:45:00', 'Blanket winter'),

-- March 2025
(11, 4, 3, 4, '2025-03-06 16:20:00', 'Pillow replacement'),
(12, 9, 13, 25, '2025-03-11 14:00:00', 'Toilet seat covers'),
(13, 2, 3, 18, '2025-03-16 10:15:00', 'Tissue box spring'),
(14, 4, 13, 6, '2025-03-21 13:45:00', 'Glass cleaner windows'),
(15, 9, 3, 5, '2025-03-27 15:00:00', 'Floor cleaner monthly'),

-- April 2025
(1, 2, 13, 15, '2025-04-03 11:30:00', 'Toilet paper April stock'),
(2, 4, 3, 20, '2025-04-08 09:15:00', 'Hand soap spring season'),
(3, 9, 13, 8, '2025-04-13 12:30:00', 'Shampoo regular supply'),
(4, 2, 3, 7, '2025-04-18 14:45:00', 'Conditioner restock'),
(5, 4, 13, 4, '2025-04-23 16:00:00', 'Bath towel replacement'),

-- May 2025
(6, 9, 3, 11, '2025-05-02 09:00:00', 'Hand towels May distribution'),
(7, 2, 13, 3, '2025-05-07 10:30:00', 'Bath mat maintenance'),
(8, 4, 3, 2, '2025-05-12 14:15:00', 'Bedsheet set new rooms'),
(9, 9, 13, 9, '2025-05-17 11:00:00', 'Pillow case standard rotation'),
(10, 2, 3, 2, '2025-05-22 08:45:00', 'Blanket light stock'),

-- June 2025
(11, 4, 13, 3, '2025-06-04 13:20:00', 'Pillow summer replacement'),
(12, 9, 3, 28, '2025-06-09 10:00:00', 'Toilet seat covers bulk order'),
(13, 2, 13, 16, '2025-06-14 15:30:00', 'Tissue box June summer'),
(14, 4, 3, 5, '2025-06-19 11:10:00', 'Glass cleaner maintenance'),
(15, 9, 13, 4, '2025-06-24 09:45:00', 'Floor cleaner quarterly'),

-- July 2025
(1, 2, 3, 14, '2025-07-07 16:20:00', 'Toilet paper peak season'),
(2, 4, 13, 18, '2025-07-11 14:00:00', 'Hand soap summer high usage'),
(3, 9, 3, 9, '2025-07-16 10:15:00', 'Shampoo VIP and regular'),
(4, 2, 13, 8, '2025-07-21 13:45:00', 'Conditioner restock'),
(5, 4, 3, 3, '2025-07-26 15:00:00', 'Bath towel replacement'),

-- August 2025
(6, 9, 13, 10, '2025-08-04 11:30:00', 'Hand towels August'),
(7, 2, 3, 2, '2025-08-09 09:15:00', 'Bath mat replacement'),
(8, 4, 13, 2, '2025-08-14 12:30:00', 'Bedsheet set room upgrade'),
(9, 9, 3, 8, '2025-08-19 14:45:00', 'Pillow case rotation'),
(10, 2, 13, 2, '2025-08-24 16:00:00', 'Blanket stock preparation'),

-- September 2025
(11, 4, 3, 2, '2025-09-02 09:00:00', 'Pillow replacement autumn'),
(12, 9, 13, 22, '2025-09-07 10:30:00', 'Toilet seat covers'),
(13, 2, 3, 14, '2025-09-12 14:15:00', 'Tissue box back to school'),
(14, 4, 13, 4, '2025-09-17 11:00:00', 'Glass cleaner windows'),
(15, 9, 3, 3, '2025-09-22 08:45:00', 'Floor cleaner monthly'),

-- October 2025
(1, 2, 13, 17, '2025-10-05 13:20:00', 'Toilet paper October busy'),
(2, 4, 3, 19, '2025-10-10 10:00:00', 'Hand soap fall season'),
(3, 9, 13, 10, '2025-10-15 15:30:00', 'Shampoo regular supply'),
(4, 2, 3, 9, '2025-10-20 11:10:00', 'Conditioner restock'),
(5, 4, 13, 5, '2025-10-25 09:45:00', 'Bath towel replacement'),

-- November 2025
(6, 9, 3, 11, '2025-11-03 16:20:00', 'Hand towels November'),
(7, 2, 13, 3, '2025-11-08 14:00:00', 'Bath mat maintenance'),
(8, 4, 3, 2, '2025-11-13 10:15:00', 'Bedsheet set replacement'),
(9, 9, 13, 10, '2025-11-18 13:45:00', 'Pillow case standard'),
(10, 2, 3, 4, '2025-11-23 15:00:00', 'Blanket winter preparation'),

(11, 4, 13, 3, '2025-11-28 11:30:00', 'Pillow pre-winter'),
(12, 9, 3, 26, '2025-11-05 09:15:00', 'Toilet seat covers bulk'),
(13, 2, 13, 19, '2025-11-10 12:30:00', 'Tissue box November'),
(14, 4, 3, 5, '2025-11-15 14:45:00', 'Glass cleaner maintenance'),
(15, 9, 13, 4, '2025-11-20 16:00:00', 'Floor cleaner monthly');


