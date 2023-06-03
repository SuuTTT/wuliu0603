# Warehouse Logistics Optimization System (WLOS)

## Description
WLOS is an intelligent system designed to optimize the logistics and distribution of goods from warehouses to users. It makes use of advanced optimization algorithms to find the best distribution scheme that minimizes the total transportation cost while meeting all users' needs.

This project was my first experience with GPT-4, OpenAI's latest language model. It was an interesting journey with 50+ rounds of questions to the AI, which took around 6 hours to get to the first commit. I will upload the chat history with GPT-4 later to share more about this exciting journey.

## System Structure
```
.
├── data_read_module/
│   ├── __init__.py
│   └── data_reader.py
├── data_preprocessing_module/
│   ├── __init__.py
│   └── data_preprocessor.py
├── optimization_model_module/
│   ├── __init__.py
│   └── model_builder.py
├── optimization_solver_module/
│   ├── __init__.py
│   └── solver.py
├── result_output_module/
│   ├── __init__.py
│   └── result_output.py
└── update_monitor_module/
    ├── __init__.py
    └── update_monitor.py
```

### 1. Data Read Module
This module interacts with databases to fetch data, including customer demand, warehouse inventory, transport cost functions, warehouse and customer location information, customer priority information, and warehouse coverage.

### 2. Data Preprocessing Module
This module validates the integrity and consistency of input data, handles missing and outlier values, calculates and verifies the coverage of each warehouse, generates the relationship between customers and warehouses, and calculates and generates transportation cost functions.

### 3. Optimization Model Module
This module constructs the corresponding models according to different optimization algorithms, which includes integer programming models, genetic algorithm models, and other optimization models like linear programming and mixed integer programming.

### 4. Optimization Solver Module
This module calls the appropriate solver to solve the model according to the selected optimization algorithm, for example, CPLEX or Gurobi for integer programming model, and DEAP for genetic algorithm model.
### 5. Result Output Module
This module processes the results returned by the solver and outputs or stores them in the database in an appropriate format.

### 6. Update Monitor Module
Monitors real-time changes in user demand and warehouse inventory and updates the data and model accordingly.


## Database Setup

1. **Open MySQL command line client or MySQL Shell.**

2. **Log in to your MySQL server:**

    ```
    mysql -u root -p
    ```

    This command will prompt you for your MySQL password. Replace `root` with your MySQL username if it's not `root`.

3. **Create the database (if it does not already exist):**

    ```sql
    CREATE DATABASE IF NOT EXISTS your_database_name;
    ```

    Replace `your_database_name` with the name of your database.

4. **Use the database:**

    ```sql
    USE your_database_name;
    ```

5. **Create the tables:**

    To run the SQL script contained in `create-database.sql`, exit the MySQL Shell and navigate to the directory containing the `create-database.sql` file. Then, execute the following command:

    ```
    mysql -u root -p your_database_name < create-database.sql
    ```

    This command will prompt you for your MySQL password. Replace `root` with your MySQL username if it's not `root` and `your_database_name` with the name of your database.



You're all set! The database and necessary tables have been created and are ready to be used by the application.



Remember to replace `your_database_name` with the actual name of your database.
## Getting Started


1. **Clone the repository:**

   ```
   git clone https://github.com/SuuTTT/wuliu0603.git
   ```

2. **Navigate to the project directory:**

   ```
   cd PROJECT_NAME
   ```

3. **Create a virtual environment:**

   - On Unix or MacOS:

     ```bash
     python3 -m venv env
     source env/bin/activate
     ```

   - On Windows:

     ```bash
     python -m venv env
     .\env\Scripts\activate
     ```

4. **Install the dependencies:**

   ```
   pip install -r requirements.txt
   ```

5. **Run the test script:**

   ```
   python test_algo.py
   ```

Now you're ready to run the project!





## Documentation
Further documentation on the modules and their workings will be added soon.

## Contributing
 me with GPT4.
 We welcome contributions from everyone. Please read the Contributing Guide for more details on how to contribute.

## License
This project is licensed under [MIT License](https://opensource.org/licenses/MIT).

