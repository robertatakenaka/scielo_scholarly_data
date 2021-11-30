import argparse
import csv
import scielo_scholarly_data.standardizer as standardizer
import tempfile
import os

from scielo_dltools.libs import gstorage


def create_table(rows, cols):
	table = []
	for row in range(rows):
		table.append([0]*cols)
	return table
	
	
def count_status(table_in, rows, cols):
	table_inter = create_table(len(rows), len(cols))
	for row in table_in:
		if row[2] == 'current':
			table_inter[rows.index(row[0])][cols.index(row[1])] = 1
		else:
			table_inter[rows.index(row[0])][cols.index(row[1])] = -1
	return table_inter
	
			
def accumulate_status(table_inter):
	for row in table_inter:
		for col in range(1,len(row)):
			if row[col] == 0:
				row[col] = row[col - 1]
	return table_inter
	
	
def classify_status(table_inter, cols):
	table_out = create_table(4, len(cols))
	for row in table_inter:
		for col in range(len(row)):
			table_out[0][col] = cols[col]
			if row[col] == 1: 
				table_out[1][col] += 1
			if row[col] == -1:
				table_out[2][col] += 1
			if row[col] != 0:
				table_out[3][col] += 1
	return table_out
					
	
def read_table(arq, cols_to_read):
	table_in = []
	cols = set()
	rows = set()
	with open(arq) as data:
		for row in csv.DictReader(data, delimiter=','):
			aux = []
			for col in cols_to_read:
				aux.append(row.get(col))
			table_in.append(aux)
			cols.add(aux[1])
			rows.add(aux[0])
			
	rows = sorted(rows)
	cols = sorted(cols)
	
	table_inter = count_status(table_in, rows, cols)
	
	table_inter = accumulate_status(table_inter)
			
	table_out = classify_status(table_inter, cols)
	
	return table_out
		
			
def write_table(arq, table, rows_to_write):
	table_to_write = []
	for item in range(len(rows_to_write)):
		table_to_write.append([rows_to_write[item]] + table[item])
	
	with open(arq, 'w') as data:   
		writer = csv.writer(data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for cols in table_to_write:
			writer.writerow(cols)


def main():
	parser = argparse.ArgumentParser(description='Creates a dataset to produce figure 1 of the FAPESP report with data from the Data Lake.')
	parser.add_argument('-d', '--file_to_download', dest='path_file_to_download', required=True, help='Path file to download from Data Lake.')
	parser.add_argument('-u', '--file_to_upload', dest='path_file_to_upload', required=True, help='Path file to upload to Data Lake.')
	arguments = parser.parse_args()
	
	temp, path = tempfile.mkstemp()
	
	BUCKET_NAME_DOWNLOAD = arguments.path_file_to_download.split('/')[0]
	SOURCE_FILE_DOWNLOAD = '/'.join(arguments.path_file_to_download.split('/')[1:])
	BUCKET_NAME_UPLOAD = arguments.path_file_to_upload.split('/')[0]
	DESTINATION_FILE_UPLOAD = '/'.join(arguments.path_file_to_upload.split('/')[1:])
		
	gstorage.download_file(
		BUCKET_NAME_DOWNLOAD, 
		SOURCE_FILE_DOWNLOAD, 
		path
		)
		
	cols_to_read = [
		'ISSN SciELO',
		'status change year',
		'status changed to'
	]

	rows_to_write = [
		'year',
		'current',
		'deindexed',
		'indexed'
	]
	
	table = read_table(path, cols_to_read)
	write_table(path, table, rows_to_write)
	
	gstorage.upload_file(
		BUCKET_NAME_UPLOAD, 
		path,
		DESTINATION_FILE_UPLOAD
		)
	
	os.remove(path)
	
	
if __name__ == '__main__':
	main()
