# CCINFOM-DBApp
CCINFOM-S26-06 DBApp for Term 1, 2025-2026

# Hotel Management Simulation

 _Hotel Management Simulation_ |  _OOP Design Project_

## 📌 Project Overview

This project simulates a Hotel Management DB System. This Java and SQL application models:



**Key Features:**  
✅ Room reservation System  
✅ Housekeeping Items tracking  
✅ Guest Check-in and Check-out
✅ Guest Payment dashboard

## How to use

## Prerequisites

Before running the Hotel Management System, make sure the following are installed on your machine:

1. **Python 3.10+**  
   - [Download Python](https://www.python.org/downloads/) and install it.  
   - Verify installation:
     ```bash
     python --version
     ```

2. **pip (Python package manager)**  
   - Usually comes with Python.  
   - Verify installation:
     ```bash
     pip --version
     ```

3. **MySQL**  
   - [Download and install MySQL](https://dev.mysql.com/downloads/).  
   - Make sure the MySQL server is running and you know your username/password.  
   - Verify installation:
     ```bash
     mysql --version
     ```

4. **Python dependencies**  
   - Navigate to your project directory and install all required Python packages listed in `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```
   - This will install packages such as `Flask`, `PyMySQL`, and any other dependencies your project uses.



### Clone Repository

```
git clone https://github.com/PrinceMPS/S26-06-DBApp.git
```

### How to Run
```
cd .\S26-06-DBApp\
python app.py
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

