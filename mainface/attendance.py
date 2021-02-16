

def attendance_reg(faces):
    
    # all csa students list
    all_students = ["Aarsha VS","Abhijith J","Abhinav V V", "Abhiram S", "Abin Shaji Philip", "Adith Ajay", "Ajay Ben", "Ajay Thomas", "Akhil Mathew", "Akhil P Dominic", "Akshay Ganesh", "Alan Biju George", "Alan James", "Alan Maria", "Alan Scaria", "Aleena Thomas", "Allen Roy", "Aloyise Biju Mathew", "Ameen Zubair", "Anandu Sunil Kumar", "Andrew Frederick Jones", "Aneena Thankachan", "Aneeta Shajan", "Angela Ann Varghese", "Anjana S Nair", "Anna Tennyson", "Ann Maria Jaimon", "Ann Maria Johnson", "Ann Mary Johnson", "Annu Rose Shaji", "Anson Benny", "Anto K Thomas", "Antony Thomas", "Anu P Nair", "Arathy Baby", "Arif Mohammed", "Aryakrishnan C R", "Arya Shinod", "Ashna Mariet Shaji", "Ashwin Raj", "Ashwin Sasikumar", "Ashwin Sebastian", "Asif Shereef", "Athul Saji", "Athulya Anilkumar", "Befin K Lalu", "Ben Jacob Bobby", "Chetan Manoj", "Christy Chacko", "Christy K Mathews", "Christy Maria Eappen", "Cyril Thomas", "Daan Jacob", "Denna Joseph", "Devanandan R", "Devarsh Damodaran", "Diya Merene Thomas", "Diya Shaji", "Elena Maria Varghese", "Emal George", "Emal John Manuel", "Emil Liz George", "Febin K Dominic", "Felix Kurian", "Gaby Joseph", "Gauthami S", "Glen Vipin Pereira", "Gopika S", "Gowripriya S", "Grace Maria Bino"]

    attendance_registry = []

    for student in all_students:
        if student in faces:
            attendance_registry.append("Present")
            # print(student)
            # print("present")
        else:
            attendance_registry.append("Absent")
            # print(student)
            # print("absent")
  
    return attendance_registry