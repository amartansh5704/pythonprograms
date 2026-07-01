class Patient:
    def __init__(self, name, age, patient_id):
        self.name = name
        self.__age = age
        self.patient_id = patient_id
        self.__blood_pressure = None
        self.__blood_sugar = None
        self.__medical_history = []
        self.__prescriptions = []

    def get_age(self):
        return self.__age
    
    def set_age(self, new_age):
        if new_age < 0 or new_age > 120:
            print("Invalid age. Age must be between 0 and 120.")
            return
        self.__age = new_age
        print(f"Age updated to {new_age}")
    
    def set_blood_pressure(self, systolic, diastolic):
        if systolic < 0 or diastolic < 0:
            print("Invalid blood pressure values")
            return
        self.__blood_pressure = f"{systolic}/ {diastolic}"
        print (f"Blood pressure updated to {self.__blood_pressure}")
    
    def set_blood_sugar(self, level):
        if level < 0:
            print("Invalid blood sugar level")
            return
        self.__blood_sugar = level
        status = self.__check_blood_sugar_status(level)
        print(f"Blood sugar level updated to {level}. Status: {status}")
    
    def __check_blood_sugar_status(self, level):
        if level < 70:
            return "Low"
        elif 70 <= level <= 140:
            return "Normal"
        else:
            return "High"
    
    def add_medical_history(self, condition):
        self.__medical_history.append(condition)
        print(f"Added to medical history: {condition}")
    
    def add_prescription(self, medicine, dosage, frequency):
        prescription = {
            "medicine": medicine,
            "dosage": dosage,
            "frequency": frequency
        }
        self.__prescriptions.append(prescription)
        print(f"Added prescription: {medicine}, Dosage: {dosage}, Frequency: {frequency}")
    
    def get_full_report(self):
        print(f"\n{'='*50}")
        print(f"  🏥 PATIENT HEALTH REPORT")
        print(f"{'='*50}")
        print(f"  Name          : {self.name}")
        print(f"  Patient ID    : {self.patient_id}")
        print(f"  Age           : {self.__age} years")
        print(f"  Blood Pressure: {self.__blood_pressure or 'Not recorded'}")
        print(f"  Blood Sugar   : {str(self.__blood_sugar) + ' mg/dL' if self.__blood_sugar else 'Not recorded'}")

        print(f"Medical History")
        if self.__medical_history:
            for i, condition in enumerate(self.__medical_history, start=1):
                print(f" {i}. {condition}")
            else:
                print("No medical history")

        print(f"Prescriptions")
        if self.__prescriptions:
            for i, prescription in enumerate(self.__prescriptions, start=1):
                print(f" {i}. Medicine: {prescription['medicine']}, Dosage: {prescription['dosage']}, Frequency: {prescription['frequency']}")
            else:
                print("No prescriptions")
        
    def __str__(self):
        return f"Patient(Name: {self.name}, Age: {self.__age}, Patient ID: {self.patient_id})"


print("Patient Management System")

patient1 = Patient("John Doe", 30, "P12345")
patient2 = Patient("Jane Smith", 25, "P67890")

print("Records for John Doe:")
patient1.set_blood_pressure(120, 80)
patient1.set_blood_sugar(90)
patient1.add_medical_history("Hypertension")
patient1.add_medical_history("Asthma")
patient1.add_prescription("Lisinopril", "10mg", "Once daily")

print("Records for Jane Smith:")
patient2.set_blood_pressure(110, 70)
patient2.set_blood_sugar(150)
patient2.add_medical_history("Diabetes")
patient2.add_prescription("Metformin", "500mg", "Twice daily")

print()
patient1.get_full_report()
patient2.get_full_report()

print("\n--- Testing Encapsulation ---")
print(f"Age (using getter): {patient1.get_age()}")
patient1.set_age(36)
patient1.set_age(-5)

print("\n--- Trying to access private variable directly ---")
try:
    print(patient1.__age)
except AttributeError as e:
    print(f"Cannot access: {e}")

print()
print(patient1)
print(patient2)