import numpy as np


# This algorithm is based on the hungarian algorithm found on wikipedia
# https://en.wikipedia.org/wiki/Hungarian_algorithm
# Modification is made to adjust for non-one-to-one doctor-patient-assignment
#
# Assumption 1: there are enough doctors for all the patients
# (num of doc * max num of patients a doctor can handle >= num of patient).
# Assumption 2: the patient's preference of doctors is strictly ranked from 1 to num of doctor,
# with no repeat in ranking
#
# The basic logic of this algorithm is that: if only one patient sees one doctor as the best option,
# then assigning this patient to the doctor is the best solution.
# If multiple patients see one doctor as the best option, then whether their next best options' availability is checked
# The patient whose next best option not available will get the best option.
def hungarian(patient_preference, max_num_patient):
    num_doctor = len(patient_preference[0])
    num_patient = len(patient_preference)
    doctor_to_patient = []
    zeros = []
    for i in range(num_doctor):
        doctor_to_patient.append([])
        zeros.append([])
    mat = patient_preference
    cover_rows = []
    cover_cols = []
    while len(cover_rows) != num_patient:
        adjust_matrix(mat, zeros, doctor_to_patient, cover_rows, cover_cols, max_num_patient)
        eliminate_new_zero_within_limit(zeros, doctor_to_patient, cover_rows, cover_cols, max_num_patient)
        mark_doc(zeros, cover_cols, max_num_patient)
    return doctor_to_patient


# adjust the matrix to identify each patient's favorite doctor within the free doctor list
def adjust_matrix(mat, zeros, doctor_to_patient, cover_rows, cover_cols, max_num_patient):
    # subtract 1 from all not-covered cell
    for patient in range(len(mat)):
        if patient not in cover_rows:
            for doc in range(len(mat[patient])):
                if doc not in cover_cols:
                    mat[patient][doc] = mat[patient][doc] - 1
                    # if there is new zero, find 0s in the same row and set the value to -1
                    # if the old zero's column has only one 0 left, assign it.
                    if mat[patient][doc] == 0:
                        for covered_doc in cover_cols:
                            if mat[patient][covered_doc] == 0:
                                mat[patient][covered_doc] = - 1
                                zeros[covered_doc].remove(patient)
                                if len(zeros[covered_doc]) == max_num_patient:
                                    for row in zeros[covered_doc]:
                                        doctor_to_patient[covered_doc].append(row)
                                        cover_rows.append(row)
                        zeros[doc].append(patient)


# assign the cell that has the under limit 0 in the column
def eliminate_new_zero_within_limit(zeros, doctor_to_patient, cover_rows, cover_cols, max_num_patient):
    for doc in range(len(zeros)):
        if len(zeros[doc]) <= max_num_patient:
            for patient in zeros[doc]:
                if patient not in cover_rows:
                    doctor_to_patient[doc].append(patient)
                    cover_rows.append(patient)
                    if len(doctor_to_patient[doc]) == max_num_patient:
                        cover_cols.append(doc)


# mark doc that has more than limit patients favoring
def mark_doc(zeros, cover_cols, max_num_patient):
    for doc in range(len(zeros)):
        if len(zeros[doc]) > max_num_patient:
            cover_cols.append(doc)


def main():
    # row as patient, column as doctor, the lower the number the higher the doctor ranked
    # patient_preference = np.array([[1, 2, 3, 4, 5, 6],
    #                               [1, 2, 3, 4, 5, 6],
    #                               [1, 3, 4, 6, 5, 2],
    #                               [3, 6, 1, 2, 4, 5],
    #                               [2, 6, 1, 3, 4, 5],
    #                               [6, 5, 4, 3, 2, 1]])

    patient_preference = np.array([[1, 1, 3],
                                  [1, 2, 3],
                                  [3, 2, 1]])

    # patient_preference = np.array([[1, 2, 3],
    #                                [1, 3, 2],
    #                                [1, 2, 3],
    #                                [2, 3, 1],
    #                                [2, 1, 3],
    #                                [3, 2, 1]])
    max_num_patient = 1  # the maximum number of patients that each doctor can be assigned to
    assignment = hungarian(patient_preference.copy(), max_num_patient)
    for doctor in range(len(assignment)):
        print('Doctor ', doctor, 'takes patient(s): ', assignment[doctor])

if __name__ == '__main__':
    main()
