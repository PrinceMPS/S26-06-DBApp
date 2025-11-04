# CCINFOM-DBApp
CCINFOM-S26-06 DBApp for Term 1, 2025-2026

# Hotel Management Simulation

 _Hotel Management Simulation_ |  _OOP Design Project_

## 📌 Project Overview

This project simulates a Hotel Management DB System. This Java and SQL application models:

- **Regular Trucks (JavaJeep)** - Basic coffee service
- **Special Trucks (JavaJeep+)** - Custom drinks with extra features

**Key Features:**  
✅ Room reservation System  
✅ Housekeeping Items tracking  
✅ Guest Check-in and Check-out
✅ Guest Payment dashboard

## How to use

### Clone Repository

```
git clone https://github.com/PrinceMPS/S26-06-DBApp.git
```

### Compile and run (Java 17+ required)

```
cd S26-06-DBAPP
javac -d bin src/*.java src/view/*.java src/model/*.java src/controller/*.java
java -cp bin Driver
```
### How to generate javadoc

```
cd S26-06-DBAPP
javadoc -d doc -sourcepath src -subpackages model:view:controller
```

## Project organization

The MVC structure is in `src` folder. In it, there are three folders and one files.

### / (root)

| Name           | Type        | Function                        |
| -------------- | ----------- | ------------------------------- |
|                |             |                                 |
|                |           ` |                                 |
| &#46;gitignore | `File`      | Github generated file           |

### /src

| Name            | Type        | Function                                       |
| --------------- | ----------- | ---------------------------------------------- |
| assets          | `Directory` | Contains all application content files         |
| controller      | `Directory` | Contains all application controller classes    |
| model           | `Directory` | Contains all application model classes         |
| view            | `Directory` | Contains all application view classes          |
| Driver&#46;java | `File`      | Class responsible for starting the application |

