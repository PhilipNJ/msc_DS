# GlideVolt⚡
 
## Introduction
Glidevolt is aimed at providing a platform for people to rent e-vehicles such as e-bikes and e-cycles. It also provides means of managing a vehicle fleet efficiently. This system helps in tracking, charging, repairing, and moving vehicles, catering to the needs of both operators and managers. Glidevolt provides a user-friendly interface to manage various tasks related to the fleet.

---

## Prerequisites
#### Required python packages
```bash
pip install customtkinter==5.2.0
pip install matplotlib==3.8.0
pip install pandas==1.5.3
pip install Pillow==10.0.1
pip install Pillow==10.1.0
pip install seaborn==0.13.0
pip install wordcloud==1.9.2
pip install sqlite3
pip install gc
pip install tkinter
pip install datetime
pip install math
pip install random

```
---
## Installation
1. Copy the pip install commands from above and run them into Terminal 
 OR
2. Navigate to the project directory using: `cd`
3. Install required packages: `pip install -r requirements.txt`

---
## Usage
1. Run the `project_main.py` file: `python project_main.py`
2. Usage can be broadly categorised for an User as **Customer perspective**, **Operator Perspective** and **Manager perspective** which starts with the Login Page
![Alt text](/Screenshots/login_page.png?raw=true)

##### Customer Perspective 
1. Previously registered users can directly login while selecting **Customer** from dropdown. New users can register.
![Alt text](/Screenshots/register.png?raw=true)

2. Customer can then select the trip start location and end location 
![Alt text](/Screenshots/customerhomepage.png?raw=true)

    or topup their wallet using the **Wallet** Button.
![Alt text](/Screenshots/wallet.png?raw=true)

3. Customer can select the type of vehicle which will be shown only if there is atleast one (Bike/Cycle) available at the chosen start location
![Alt text](/Screenshots/tripcal.png?raw=true)

4. Customer then starts the trip if the wallet minimum balance is greater than the trip estimate cost or else they can top it up.
![Alt text](/Screenshots/Insufficientbal.png?raw=true)
![Alt text](/Screenshots/minbal.png?raw=true)

5. Upon adding the required amount, the trip will start and show real-time cost and trip time
![Alt text](/Screenshots/endtripcal.png?raw=true)

6. Once clicked on **End Trip**, Customer will be taken to another page where they can see the total cost of the trip
![Alt text](/Screenshots/endtrip.png?raw=true)

7. If the wallet doesnt have the required amount then the Customer will be asked to topup the required amount
![Alt text](/Screenshots/insufficientbal2.png?raw=true)

8. At the end, the Customer will be taken to optional page called **Feeback**, where they can share their opinion regarding the trip and report issues (if any)
![Alt text](/Screenshots/feedback.png?raw=true)

##### Operator Perspective 
1. Operators can track, charge, repair, and move vehicles.
2. Upon Logging in, Operator will be given the above choices as Button and can perform actions that follows
![Alt text](/Screenshots/operatormain.png?raw=true)

3. **Track Vehicle** Button will let Operator track all the vehicles
![Alt text](/Screenshots/optrack.png?raw=true)

4. **Charge Vehicle** Button will provide Operator with functionality to charge the vehicle. The user can select a vehicle from the dropdown and click "Charge" to charge it. Click "x" to go back to operator homepage.
![Alt text](/Screenshots/opcharge.png?raw=true)

5. **Repair Vehicle** Button will provide Operator with functionality to repair the vehicle. The user can select a vehicle from the dropdown and click "Repair" to repair it. Click "x" to go back to operator homepage.
![Alt text](/Screenshots/oprepair.png?raw=true)

6. **Move Vehicle** Button will provide Operator with functionality to move the vehicle. The operator can select the type of vehicle, move from and move to values from the dropdowns and click on "Move" to move the vehicles. Click "x" to go back to operator homepage.
![Alt text](/Screenshots/opmove.png?raw=true)

7. Once they **Logout**, they will be redirected to the Login Page

##### Manager Perspective
1. Managers can generate various reports based on user interactions and system data.

2. Once they Login, they will be presented with a dropdown to select the type of report they want to view
![Alt text](/Screenshots/mmain.png?raw=true)


3. Upon clicking **Generate Report**, the report will open in a separate window. On this window, there are button to interact with the hyperparameters of the report. Click "x" to go back and eventually logout.
![Alt text](/Screenshots/mreport.png?raw=true)
 

---
## Functionality
### Customer Page
- **Register:** Register as a user
- **Wallet:** Use wallet functionality to add money for trip
- **Rent Vehicle:** Rent Vehicle for trip (Bike/Cycle)
- **Feedback:** Provide feedback for the trip


### Operator Page
- **Track Vehicles:** View details of available bikes and cycles.
- **Charge Vehicles:** Charge vehicles and update their status.
- **Repair Vehicles:** Initiate repairs for damaged vehicles.
- **Move Vehicles:** Relocate vehicles to different locations.
 
### Manager Page
- **Generate Reports:** Choose from a list of reports to view insights about user interactions, vehicle statuses, and more.

---

## Contact
For any inquiries, please contact the project team at contactus@glidevolt.com.
 
---