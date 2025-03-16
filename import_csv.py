import csv

def write_to_csv(file_path, data):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Column1', 'Column2', 'Column3'])  # Escribir encabezados
        for row in data:
            writer.writerow(row)

# Ejemplo de uso
data = [
    [1, 'data1', 'data2'],
    [2, 'data3', 'data4'],
    [3, 'data5', 'data6']
]

write_to_csv('Salidas/analisis_postura.csv', data)